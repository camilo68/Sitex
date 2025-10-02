# routes.py - ACTUALIZADO CON TODAS LAS MEJORAS
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from flask_mail import Message
from werkzeug.utils import secure_filename
from datetime import date, datetime, timedelta
from sqlalchemy import func, extract
import bcrypt
import os
import secrets
import pandas as pd

from extensions import db, mail
from models import Empleado, Tanque, Descargue, RegistroMedida, MedicionCargue, SesionActiva, Auditoria, Venta
from forms import (LoginForm, RegisterForm, MedicionForm, DescargueForm, ChangePasswordForm, 
                  ResetPasswordForm, RequestPasswordResetForm, PasswordResetForm, TanqueForm,
                  CargaMasivaForm, FiltroMedicionesForm)
from utils import (islero_or_encargado_required, admin_or_encargado_required, admin_required,
                  registrar_auditoria, allowed_file)

# Blueprints
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
main_bp = Blueprint("main", __name__)
dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")
medicion_bp = Blueprint("medicion", __name__, url_prefix="/medicion")
admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# ============= AUTH ROUTES =============
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = LoginForm()
    if form.validate_on_submit():
        usuario = form.username.data.strip()
        contrasena = form.password.data

        empleado = Empleado.query.filter(
            (Empleado.usuario == usuario) | (Empleado.numero_documento == usuario)
        ).first()

        if empleado and empleado.check_password(contrasena):
            if not empleado.activo:
                flash("Su cuenta ha sido deshabilitada. Contacte al administrador.", "danger")
                return redirect(url_for("auth.login"))

            login_user(empleado, remember=form.remember_me.data)
            
            # Crear sesión activa
            session_id = secrets.token_urlsafe(32)
            sesion = SesionActiva(
                id_empleados=empleado.id_empleados,
                session_id=session_id,
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent', '')[:255]
            )
            db.session.add(sesion)
            db.session.commit()

            flash(f"Bienvenido {empleado.nombre_empleado}!", "success")
            return redirect(url_for("dashboard.index"))
        else:
            flash("Usuario o contraseña incorrectos", "danger")

    return render_template("auth/login.html", form=form)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Verificar duplicados
        if Empleado.query.filter_by(numero_documento=form.numero_documento.data).first():
            flash("El número de documento ya está registrado", "danger")
            return render_template("auth/register.html", form=form)
        
        if Empleado.query.filter_by(email=form.email.data).first():
            flash("El email ya está registrado", "danger")
            return render_template("auth/register.html", form=form)
        
        if Empleado.query.filter_by(usuario=form.usuario.data).first():
            flash("El nombre de usuario ya está en uso", "danger")
            return render_template("auth/register.html", form=form)

        # Crear contraseña temporal
        num_doc = form.numero_documento.data
        contrasena_temporal = num_doc[-4:] if len(num_doc) >= 4 else num_doc
        hash_cifrado = bcrypt.hashpw(contrasena_temporal.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        nuevo_empleado = Empleado(
            usuario=form.usuario.data,
            nombre_empleado=form.nombre_empleado.data,
            apellido_empleado=form.apellido_empleado.data,
            numero_documento=form.numero_documento.data,
            tipo_documento=form.tipo_documento.data,
            email=form.email.data,
            telefono=form.telefono.data,
            direccion=form.direccion.data,
            cargo_establecido=form.cargo_establecido.data,
            contrasena=hash_cifrado,
            temporal=True,
            activo=True,
            aceptado_terminos=form.aceptar_terminos.data
        )
        
        db.session.add(nuevo_empleado)
        db.session.commit()
        
        registrar_auditoria('CREATE', 'empleado', nuevo_empleado.id_empleados, None, {
            'usuario': nuevo_empleado.usuario,
            'nombre': nuevo_empleado.nombre_empleado
        })

        flash(f"¡Registro exitoso! Tu contraseña temporal es: {contrasena_temporal}", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    # Cerrar sesión activa
    SesionActiva.query.filter_by(
        id_empleados=current_user.id_empleados,
        activa=True
    ).update({'activa': False})
    db.session.commit()
    
    logout_user()
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for("auth.login"))

@auth_bp.route("/logout_all", methods=["POST"])
@login_required
def logout_all():
    """Cerrar sesión en todos los dispositivos"""
    SesionActiva.query.filter_by(id_empleados=current_user.id_empleados).update({'activa': False})
    db.session.commit()
    logout_user()
    flash("Se han cerrado todas las sesiones activas", "success")
    return redirect(url_for("auth.login"))

@auth_bp.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            hash_nuevo = bcrypt.hashpw(form.new_password.data.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            current_user.contrasena = hash_nuevo
            current_user.temporal = False
            db.session.commit()
            
            registrar_auditoria('UPDATE', 'empleado', current_user.id_empleados, 
                              {'temporal': True}, {'temporal': False})
            
            flash("Contraseña actualizada exitosamente", "success")
            return redirect(url_for("dashboard.index"))
        else:
            flash("Contraseña actual incorrecta", "danger")
    
    return render_template("auth/change_password.html", form=form)

@auth_bp.route("/request_reset", methods=["GET", "POST"])
def request_password_reset():
    form = RequestPasswordResetForm()
    if form.validate_on_submit():
        empleado = Empleado.query.filter_by(email=form.email.data).first()
        if empleado:
            token = empleado.generate_reset_token()
            db.session.commit()
            
            # Enviar email
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            msg = Message("Recuperación de Contraseña - Hayuelos",
                        recipients=[empleado.email])
            msg.body = f"""Hola {empleado.nombre_empleado},

Has solicitado restablecer tu contraseña. Haz clic en el siguiente enlace:

{reset_url}

Este enlace expira en 1 hora.

Si no solicitaste este cambio, ignora este correo.

Saludos,
Sistema Hayuelos
"""
            try:
                mail.send(msg)
                flash("Se ha enviado un enlace de recuperación a tu email", "success")
            except:
                flash("Error al enviar el email. Contacta al administrador.", "danger")
        else:
            flash("Email no encontrado", "danger")
    
    return render_template("auth/request_reset.html", form=form)

@auth_bp.route("/reset/<token>", methods=["GET", "POST"])
def reset_password(token):
    empleado = Empleado.query.filter_by(reset_token=token).first()
    if not empleado or not empleado.verify_reset_token(token):
        flash("Token inválido o expirado", "danger")
        return redirect(url_for("auth.request_password_reset"))
    
    form = PasswordResetForm()
    if form.validate_on_submit():
        hash_nuevo = bcrypt.hashpw(form.password.data.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        empleado.contrasena = hash_nuevo
        empleado.reset_token = None
        empleado.reset_token_expiry = None
        empleado.temporal = False
        db.session.commit()
        
        flash("Contraseña restablecida exitosamente", "success")
        return redirect(url_for("auth.login"))
    
    return render_template("auth/reset_password.html", form=form)

@auth_bp.route("/reset_password/<int:empleado_id>", methods=["POST"])
@login_required
@admin_or_encargado_required
def reset_password_admin(empleado_id):
    empleado = Empleado.query.get_or_404(empleado_id)
    
    contrasena_temporal = empleado.numero_documento[-4:] if len(empleado.numero_documento) >= 4 else empleado.numero_documento
    hash_cifrado = bcrypt.hashpw(contrasena_temporal.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    empleado.contrasena = hash_cifrado
    empleado.temporal = True
    db.session.commit()
    
    registrar_auditoria('UPDATE', 'empleado', empleado_id, None, {'reset_password': True})
    
    flash(f"Contraseña restablecida para {empleado.nombre_empleado}. Nueva contraseña: {contrasena_temporal}", "success")
    return redirect(url_for("dashboard.empleados"))

# ============= MAIN ROUTES =============
@main_bp.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    return redirect(url_for("auth.login"))

@main_bp.route("/terminos")
def terminos():
    return render_template("terminos.html")

@main_bp.route("/privacidad")
def privacidad():
    return render_template("privacidad.html")

# ============= DASHBOARD ROUTES =============
@dashboard_bp.route("/")
@login_required
def index():
    tanques = Tanque.query.filter_by(activo=True).all()
    total_capacity = sum(float(t.capacidad) for t in tanques) if tanques else 0
    mediciones_recientes = RegistroMedida.query.order_by(
        RegistroMedida.fecha_hora_registro.desc()
    ).limit(5).all()
    descargues_hoy = Descargue.query.filter_by(fecha=date.today()).all()

    tanques_por_tipo = {}
    for tanque in tanques:
        tipo = tanque.tipo_combustible
        if tipo not in tanques_por_tipo:
            tanques_por_tipo[tipo] = {"count": 0, "capacity": 0, "current": 0}
        tanques_por_tipo[tipo]["count"] += 1
        tanques_por_tipo[tipo]["capacity"] += float(tanque.capacidad)
        tanques_por_tipo[tipo]["current"] += tanque.contenido or 0

    # Estadísticas de ventas
    combustible_mas_vendido = db.session.query(
        Tanque.tipo_combustible,
        func.sum(Venta.cantidad_galones).label('total')
    ).join(Venta).group_by(Tanque.tipo_combustible).order_by(func.sum(Venta.cantidad_galones).desc()).first()

    # Época del año con más ventas
    ventas_por_mes = db.session.query(
        extract('month', Venta.fecha).label('mes'),
        func.sum(Venta.cantidad_galones).label('total')
    ).group_by('mes').order_by(func.sum(Venta.cantidad_galones).desc()).all()

    context = {
        "tanques": tanques,
        "total_capacity": total_capacity,
        "mediciones_recientes": mediciones_recientes,
        "descargues_hoy": descargues_hoy,
        "tanques_por_tipo": tanques_por_tipo,
        "total_tanques": len(tanques),
        "combustible_mas_vendido": combustible_mas_vendido,
        "ventas_por_mes": ventas_por_mes
    }
    return render_template("dashboard/index.html", **context)

@dashboard_bp.route("/tanques")
@login_required
def tanques():
    tanques = Tanque.query.filter_by(activo=True).all()
    return render_template("dashboard/tanques.html", tanques=tanques)

@dashboard_bp.route("/empleados")
@login_required
@admin_or_encargado_required
def empleados():
    empleados = Empleado.query.all()
    return render_template("dashboard/empleados.html", empleados=empleados)

# ============= MEDICION ROUTES =============
@medicion_bp.route("/registro", methods=["GET", "POST"])
@login_required
@islero_or_encargado_required
def registro():
    form = MedicionForm()
    tanques = Tanque.query.filter_by(activo=True).all()
    form.tanque.choices = [(t.id_tanques, f"{t.tipo_combustible} - Tanque {t.id_tanques}") for t in tanques]

    if form.validate_on_submit():
        # Guardar imagen si existe
        imagen_path = None
        if form.imagen.data:
            file = form.imagen.data
            if allowed_file(file.filename):
                filename = secure_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                filepath = os.path.join('static/uploads', filename)
                os.makedirs('static/uploads', exist_ok=True)
                file.save(filepath)
                imagen_path = filename

        medicion = RegistroMedida(
            medida_combustible=form.medida_combustible.data,
            id_empleados=current_user.id_empleados,
            fecha_hora_registro=datetime.now(),
            galones=form.galones.data,
            id_tanques=form.tanque.data,
            tipo_medida=form.tipo_medida.data,
            novedad=form.novedad.data,
            imagen_path=imagen_path
        )
        db.session.add(medicion)
        db.session.commit()
        
        registrar_auditoria('CREATE', 'registro_medidas', medicion.id_registro_medidas, None, {
            'tanque': form.tanque.data,
            'galones': form.galones.data
        })

        flash("Medición registrada exitosamente", "success")
        return redirect(url_for("medicion.historial"))

    return render_template("medicion/registro.html", form=form)

@medicion_bp.route("/historial")
@login_required
def historial():
    page = request.args.get("page", 1, type=int)
    
    # Filtros
    query = RegistroMedida.query
    
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    tanque_id = request.args.get('tanque', type=int)
    tipo = request.args.get('tipo')
    
    if fecha_desde:
        query = query.filter(RegistroMedida.fecha_hora_registro >= fecha_desde)
    if fecha_hasta:
        query = query.filter(RegistroMedida.fecha_hora_registro <= fecha_hasta)
    if tanque_id:
        query = query.filter_by(id_tanques=tanque_id)
    if tipo:
        query = query.filter_by(tipo_medida=tipo)
    
    mediciones = query.order_by(
        RegistroMedida.fecha_hora_registro.desc()
    ).paginate(page=page, per_page=20, error_out=False)
    
    tanques = Tanque.query.filter_by(activo=True).all()
    return render_template("medicion/historial.html", mediciones=mediciones, tanques=tanques)

@medicion_bp.route("/descargue", methods=["GET", "POST"])
@login_required
@islero_or_encargado_required
def descargue():
    form = DescargueForm()
    if form.validate_on_submit():
        # Guardar imagen
        imagen_path = None
        if form.imagen.data:
            file = form.imagen.data
            if allowed_file(file.filename):
                filename = secure_filename(f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
                filepath = os.path.join('static/uploads', filename)
                os.makedirs('static/uploads', exist_ok=True)
                file.save(filepath)
                imagen_path = filename

        descargue_obj = Descargue(
            id_empleados=current_user.id_empleados,
            medida_inicial_cm=form.medida_inicial_cm.data,
            medida_inicial_gl=form.medida_inicial_gl.data,
            descargue_cm=form.descargue_cm.data,
            descargue_gl=form.descargue_gl.data,
            medida_final_cm=form.medida_final_cm.data,
            medida_final_gl=form.medida_final_gl.data,
            diferencia=form.diferencia.data,
            tanque=form.tanque.data,
            observaciones1=form.observaciones1.data,
            observaciones2=form.observaciones2.data,
            kit_derrames=form.kit_derrames.data,
            extintores=form.extintores.data,
            conos=form.conos.data,
            boquillas=form.boquillas.data,
            botas=form.botas.data,
            gafas=form.gafas.data,
            tapaoidos=form.tapaoidos.data,
            guantes=form.guantes.data,
            brillante=form.brillante.data,
            traslucido=form.traslucido.data,
            claro=form.claro.data,
            solidos=form.solidos.data,
            separacion=form.separacion.data,
            fecha=form.fecha.data or date.today(),
            imagen_path=imagen_path
        )
        db.session.add(descargue_obj)
        db.session.commit()
        
        registrar_auditoria('CREATE', 'descargues', descargue_obj.idDescargue, None, {
            'tanque': form.tanque.data
        })

        flash("Descargue registrado exitosamente", "success")
        return redirect(url_for("medicion.historial_descargues"))

    return render_template("medicion/descargue.html", form=form)

@medicion_bp.route("/historial_descargues")
@login_required
def historial_descargues():
    page = request.args.get("page", 1, type=int)
    descargues = Descargue.query.order_by(Descargue.fecha.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template("medicion/historial_descargues.html", descargues=descargues)

# ============= ADMIN ROUTES =============
@admin_bp.route("/toggle_empleado/<int:empleado_id>", methods=["POST"])
@login_required
@admin_required
def toggle_empleado(empleado_id):
    empleado = Empleado.query.get_or_404(empleado_id)
    empleado.activo = not empleado.activo
    db.session.commit()
    
    registrar_auditoria('UPDATE', 'empleado', empleado_id, 
                      {'activo': not empleado.activo}, {'activo': empleado.activo})
    
    estado = "habilitado" if empleado.activo else "deshabilitado"
    flash(f"Empleado {empleado.nombre_empleado} {estado}", "success")
    return redirect(url_for("dashboard.empleados"))

@admin_bp.route("/carga_masiva", methods=["GET", "POST"])
@login_required
@admin_required
def carga_masiva():
    form = CargaMasivaForm()
    if form.validate_on_submit():
        file = form.archivo.data
        tipo_carga = form.tipo_carga.data
        
        if file and allowed_file(file.filename, {'csv', 'xlsx', 'xls'}):
            try:
                # Leer archivo
                if file.filename.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)
                
                count = 0
                if tipo_carga == 'empleados':
                    for _, row in df.iterrows():
                        if not Empleado.query.filter_by(numero_documento=row['numero_documento']).first():
                            hash_pwd = bcrypt.hashpw(str(row['numero_documento'])[-4:].encode(), bcrypt.gensalt()).decode()
                            empleado = Empleado(
                                nombre_empleado=row['nombre'],
                                apellido_empleado=row['apellido'],
                                numero_documento=row['numero_documento'],
                                tipo_documento=row.get('tipo_documento', 'CC'),
                                email=row['email'],
                                telefono=row.get('telefono', ''),
                                direccion=row.get('direccion', ''),
                                cargo_establecido=row.get('cargo', 'islero'),
                                usuario=row['usuario'],
                                contrasena=hash_pwd,
                                activo=True
                            )
                            db.session.add(empleado)
                            count += 1
                
                elif tipo_carga == 'tanques':
                    for _, row in df.iterrows():
                        tanque = Tanque(
                            tipo_combustible=row['tipo_combustible'],
                            capacidad=int(row['capacidad']),
                            activo=row.get('activo', True)
                        )
                        db.session.add(tanque)
                        count += 1
                
                db.session.commit()
                registrar_auditoria('CREATE_BULK', tipo_carga, None, None, {'count': count})
                flash(f"Se cargaron {count} registros exitosamente", "success")
                
            except Exception as e:
                flash(f"Error al procesar archivo: {str(e)}", "danger")
    
    return render_template("admin/carga_masiva.html", form=form)

@admin_bp.route("/tanques/nuevo", methods=["GET", "POST"])
@login_required
@admin_or_encargado_required
def nuevo_tanque():
    form = TanqueForm()
    if form.validate_on_submit():
        tanque = Tanque(
            tipo_combustible=form.tipo_combustible.data,
            capacidad=form.capacidad.data,
            activo=form.activo.data
        )
        db.session.add(tanque)
        db.session.commit()
        
        registrar_auditoria('CREATE', 'tanques', tanque.id_tanques, None, {
            'tipo': form.tipo_combustible.data,
            'capacidad': form.capacidad.data
        })
        
        flash("Tanque creado exitosamente", "success")
        return redirect(url_for("dashboard.tanques"))
    
    return render_template("admin/tanque_form.html", form=form, titulo="Nuevo Tanque")

@admin_bp.route("/tanques/<int:tanque_id>/toggle", methods=["POST"])
@login_required
@admin_or_encargado_required
def toggle_tanque(tanque_id):
    tanque = Tanque.query.get_or_404(tanque_id)
    tanque.activo = not tanque.activo
    db.session.commit()
    
    registrar_auditoria('UPDATE', 'tanques', tanque_id, 
                      {'activo': not tanque.activo}, {'activo': tanque.activo})
    
    estado = "activado" if tanque.activo else "desactivado"
    flash(f"Tanque {estado}", "success")
    return redirect(url_for("dashboard.tanques"))
