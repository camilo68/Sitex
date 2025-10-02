# routes.py - CORREGIDO
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from datetime import date, datetime
import bcrypt
from app_factory import db
from models import Empleado, Tanque, Descargue, RegistroMedida
from forms import LoginForm, RegisterForm, MedicionForm, DescargueForm, ChangePasswordForm, UpdatePasswordForm
from utils import islero_required, admin_or_encargado_required


# =======================
# Blueprints
# =======================
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
main_bp = Blueprint("main", __name__)
dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")
medicion_bp = Blueprint("medicion", __name__, url_prefix="/medicion")

# ----------------------------
# 🔹 LOGIN CORREGIDO
# ----------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = LoginForm()  # ✅ Crear instancia del formulario
    msg = ""
    text = "Bienvenido al sistema Hayuelos"

    if request.method == "POST":
        usuario = request.form.get("usuario_inicio") or request.form.get("username")
        contrasena = request.form.get("contrasena") or request.form.get("password")

        if usuario and contrasena:
            # CORREGIDO: usar campos correctos de la BD
            empleado = Empleado.query.filter_by(usuario=usuario).first()
            if empleado and bcrypt.checkpw(contrasena.encode("utf-8"), empleado.contrasena.encode("utf-8")):
                login_user(empleado)
                flash("Inicio de sesión exitoso", "success")
                return redirect(url_for("dashboard.index"))
            else:
                msg = "Usuario o contraseña incorrectos"
        else:
            msg = "Debe completar todos los campos"

    return render_template("auth/login.html", form=form, msg=msg, text=text)  # ✅ Pasar form



# ----------------------------
# 🔹 REGISTRO CORREGIDO
# ----------------------------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()  # ✅ crear el formulario
    msg = ""

    if form.validate_on_submit():
        usuario = form.usuario.data.strip()
        nombre = form.nombre_empleado.data.strip()
        apellido = form.apellido_empleado.data.strip()
        num_doc = form.numero_documento.data.strip()
        email = form.email.data.strip()
        cargo = form.cargo_establecido.data  # ✅ corregido

        # Crear contraseña temporal
        contrasena_temporal = num_doc[-4:] if len(num_doc) >= 4 else num_doc
        hash_cifrado = bcrypt.hashpw(
            contrasena_temporal.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        # Validar existencia
        existente = Empleado.query.filter(
            (Empleado.numero_documento == num_doc) | (Empleado.email == email)
        ).first()

        if existente:
            msg = "La cuenta ya existe"
        else:
            nuevo = Empleado(
                usuario=usuario,
                nombre_empleado=nombre,
                apellido_empleado=apellido,
                numero_documento=num_doc,
                tipo_documento=form.tipo_documento.data,  # ✅ tomado del form
                email=email,
                telefono=form.telefono.data,
                direccion=form.direccion.data,
                cargo_establecido=cargo,  # ✅ corregido
                contrasena=hash_cifrado,
                temporal=True,
            )
            db.session.add(nuevo)
            db.session.commit()
            msg = "¡Registro exitoso! Se creó una contraseña temporal."

    return render_template("auth/register.html", form=form, msg=msg)




# ----------------------------
# 🔹 RESET PASSWORD - AGREGAR
# ----------------------------
@auth_bp.route("/reset_password/<int:empleado_id>", methods=["POST"])
@login_required
@admin_or_encargado_required
def reset_password(empleado_id):
    empleado = Empleado.query.get_or_404(empleado_id)
    
    # Crear contraseña temporal con últimos 4 dígitos del documento
    contrasena_temporal = empleado.numero_documento[-4:] if len(empleado.numero_documento) >= 4 else empleado.numero_documento
    hash_cifrado = bcrypt.hashpw(contrasena_temporal.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    empleado.contrasena = hash_cifrado
    empleado.temporal = True
    db.session.commit()
    
    flash(f"Contraseña restablecida para {empleado.nombre_empleado}. Nueva contraseña: {contrasena_temporal}", "success")
    return redirect(url_for("dashboard.empleados"))


# ----------------------------
# 🔹 CHANGE PASSWORD - AGREGAR
# ----------------------------
@auth_bp.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if bcrypt.checkpw(form.current_password.data.encode("utf-8"), current_user.contrasena.encode("utf-8")):
            hash_nuevo = bcrypt.hashpw(form.new_password.data.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            current_user.contrasena = hash_nuevo
            current_user.temporal = False
            db.session.commit()
            flash("Contraseña actualizada exitosamente", "success")
            return redirect(url_for("dashboard.index"))
        else:
            flash("Contraseña actual incorrecta", "danger")
    
    return render_template("auth/change_password.html", form=form)


# ----------------------------
# 🔹 UPDATE PASSWORD - AGREGAR
# ----------------------------
@auth_bp.route("/update_password", methods=["GET", "POST"])
@login_required
def update_password():
    if request.method == "POST":
        nueva_contrasena = request.form.get("nueva_contrasena")
        confirmar_contrasena = request.form.get("confirmar_contrasena")
        
        if nueva_contrasena and nueva_contrasena == confirmar_contrasena:
            if len(nueva_contrasena) >= 6:
                hash_nuevo = bcrypt.hashpw(nueva_contrasena.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
                current_user.contrasena = hash_nuevo
                current_user.temporal = False
                db.session.commit()
                flash("Contraseña actualizada exitosamente", "success")
                return redirect(url_for("dashboard.index"))
            else:
                flash("La contraseña debe tener al menos 6 caracteres", "danger")
        else:
            flash("Las contraseñas no coinciden", "danger")
    
    return render_template("auth/update_password.html")


# ----------------------------
# 🔹 LOGOUT
# ----------------------------
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for("auth.login"))

# =======================
# MAIN
# =======================
@main_bp.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))
    return redirect(url_for("auth.login"))

# =======================
# DASHBOARD CORREGIDO
# =======================
@dashboard_bp.route("/")
@login_required
def index():
    tanques = Tanque.query.all()
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

    context = {
        "tanques": tanques,
        "total_capacity": total_capacity,
        "mediciones_recientes": mediciones_recientes,
        "descargues_hoy": descargues_hoy,
        "tanques_por_tipo": tanques_por_tipo,
        "total_tanques": len(tanques),
    }
    return render_template("dashboard/index.html", **context)

@dashboard_bp.route("/tanques")
@login_required
def tanques():
    tanques = Tanque.query.all()
    return render_template("dashboard/tanques.html", tanques=tanques)

@dashboard_bp.route("/empleados")
@login_required
@admin_or_encargado_required
def empleados():
    empleados = Empleado.query.all()
    return render_template("dashboard/empleados.html", empleados=empleados)

# =======================
# MEDICIÓN CORREGIDO
# =======================
@medicion_bp.route("/registro", methods=["GET", "POST"])
@login_required
@islero_required
def registro():
    form = MedicionForm()
    tanques = Tanque.query.all()
    form.tanque.choices = [
        (t.id_tanques, f"{t.tipo_combustible} - Tanque {t.id_tanques}") for t in tanques
    ]

    if form.validate_on_submit():
        medicion = RegistroMedida(
            medida_combustible=form.medida_combustible.data,
            id_empleados=current_user.id_empleados,  # CORREGIDO: usar campo correcto
            fecha_hora_registro=datetime.now(),
            galones=form.galones.data,
            id_tanques=form.tanque.data,  # CORREGIDO: usar campo correcto
            tipo_medida=form.tipo_medida.data,
            novedad=form.novedad.data,
        )
        db.session.add(medicion)
        db.session.commit()
        flash("Medición registrada exitosamente", "success")
        return redirect(url_for("medicion.historial"))

    return render_template("medicion/registro.html", form=form)

@medicion_bp.route("/historial")
@login_required
def historial():
    page = request.args.get("page", 1, type=int)
    mediciones = RegistroMedida.query.order_by(
        RegistroMedida.fecha_hora_registro.desc()
    ).paginate(page=page, per_page=20, error_out=False)
    return render_template("medicion/historial.html", mediciones=mediciones)

@medicion_bp.route("/descargue", methods=["GET", "POST"])
@login_required
@islero_required
def descargue():
    form = DescargueForm()
    if form.validate_on_submit():
        descargue = Descargue(
            id_empleados=current_user.id_empleados,  # CORREGIDO: usar campo correcto
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
        )
        db.session.add(descargue)
        db.session.commit()
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