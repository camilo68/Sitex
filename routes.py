from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from datetime import datetime, date
import bcrypt
from app_factory import db
from models import Empleado, Tanque, Descargue, RegistroMedida, MedicionCargue, PedidoCombustible, Venta
from forms import LoginForm, DescargueForm, MedicionForm, EmpleadoForm
from utils import roles_required, islero_required, admin_or_encargado_required

# Blueprint definitions
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
main_bp = Blueprint('main', __name__)
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
medicion_bp = Blueprint('medicion', __name__, url_prefix='/medicion')

# Authentication routes
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = Empleado.query.filter_by(usuario=form.username.data).first()
        
        if user and user.contrasena:
            password_bytes = form.password.data.encode('utf-8') if form.password.data else b''
            if password_bytes and bcrypt.checkpw(password_bytes, user.contrasena.encode('utf-8')):
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get('next')
                flash(f'Bienvenido {user.nombre_empleado}!', 'success')
                return redirect(next_page) if next_page else redirect(url_for('dashboard.index'))
        
        flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada exitosamente', 'info')
    return redirect(url_for('auth.login'))

# Main routes
@main_bp.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('auth.login'))

# Dashboard routes
@dashboard_bp.route('/')
@login_required
def index():
    # Get tank statistics
    tanques = Tanque.query.all()
    total_capacity = sum(float(t.capacidad_gal) for t in tanques)
    
    # Get recent measurements
    mediciones_recientes = RegistroMedida.query.order_by(RegistroMedida.fecha_hora_registro.desc()).limit(5).all()
    
    # Get today's discharges
    descargues_hoy = Descargue.query.filter_by(fecha=date.today()).all()
    
    # Get fuel type distribution
    tanques_por_tipo = {}
    for tanque in tanques:
        tipo = tanque.tipo_combustible
        if tipo not in tanques_por_tipo:
            tanques_por_tipo[tipo] = {
                'count': 0,
                'capacity': 0,
                'current': 0
            }
        tanques_por_tipo[tipo]['count'] += 1
        tanques_por_tipo[tipo]['capacity'] += float(tanque.capacidad_gal)
        tanques_por_tipo[tipo]['current'] += tanque.contenido or 0
    
    context = {
        'tanques': tanques,
        'total_capacity': total_capacity,
        'mediciones_recientes': mediciones_recientes,
        'descargues_hoy': descargues_hoy,
        'tanques_por_tipo': tanques_por_tipo,
        'total_tanques': len(tanques)
    }
    
    return render_template('dashboard/index.html', **context)

@dashboard_bp.route('/tanques')
@login_required
def tanques():
    tanques = Tanque.query.all()
    return render_template('dashboard/tanques.html', tanques=tanques)

@dashboard_bp.route('/empleados')
@login_required
@admin_or_encargado_required
def empleados():
    empleados = Empleado.query.all()
    return render_template('dashboard/empleados.html', empleados=empleados)

# Medicion routes - Solo isleros pueden registrar mediciones
@medicion_bp.route('/registro', methods=['GET', 'POST'])
@login_required
@islero_required
def registro():
    form = MedicionForm()
    tanques = Tanque.query.all()
    form.tanque.choices = [(t.idTanques, f'{t.tipo_combustible} - Tanque {t.idTanques}') for t in tanques]
    
    if form.validate_on_submit():
        medicion = RegistroMedida()
        medicion.medida_combustible = form.medida_combustible.data
        medicion.idEmpleados = current_user.idEmpleados
        medicion.fecha_hora_registro = datetime.now()
        medicion.galones = form.galones.data
        medicion.idTanques = form.tanque.data
        medicion.tipo_medida = form.tipo_medida.data
        medicion.novedad = form.novedad.data
        
        db.session.add(medicion)
        db.session.commit()
        
        flash('Medición registrada exitosamente', 'success')
        return redirect(url_for('medicion.historial'))
    
    return render_template('medicion/registro.html', form=form)

@medicion_bp.route('/historial')
@login_required
def historial():
    page = request.args.get('page', 1, type=int)
    mediciones = RegistroMedida.query.order_by(RegistroMedida.fecha_hora_registro.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('medicion/historial.html', mediciones=mediciones)

@medicion_bp.route('/descargue', methods=['GET', 'POST'])
@login_required
@islero_required
def descargue():
    form = DescargueForm()
    
    if form.validate_on_submit():
        descargue = Descargue()
        descargue.idEmpleados = current_user.idEmpleados
        descargue.medida_inicial_cm = form.medida_inicial_cm.data
        descargue.medida_inicial_gl = form.medida_inicial_gl.data
        descargue.descargue_cm = form.descargue_cm.data
        descargue.descargue_gl = form.descargue_gl.data
        descargue.medida_final_cm = form.medida_final_cm.data
        descargue.medida_final_gl = form.medida_final_gl.data
        descargue.diferencia = form.diferencia.data
        descargue.tanque = form.tanque.data
        descargue.observaciones1 = form.observaciones1.data
        descargue.observaciones2 = form.observaciones2.data
        descargue.kit_derrames = form.kit_derrames.data
        descargue.extintores = form.extintores.data
        descargue.conos = form.conos.data
        descargue.boquillas = form.boquillas.data
        descargue.botas = form.botas.data
        descargue.gafas = form.gafas.data
        descargue.tapaoidos = form.tapaoidos.data
        descargue.guantes = form.guantes.data
        descargue.brillante = form.brillante.data
        descargue.traslucido = form.traslucido.data
        descargue.claro = form.claro.data
        descargue.solidos = form.solidos.data
        descargue.separacion = form.separacion.data
        descargue.fecha = form.fecha.data or date.today()
        
        db.session.add(descargue)
        db.session.commit()
        
        flash('Descargue registrado exitosamente', 'success')
        return redirect(url_for('medicion.historial_descargues'))
    
    return render_template('medicion/descargue.html', form=form)

@medicion_bp.route('/historial_descargues')
@login_required
def historial_descargues():
    page = request.args.get('page', 1, type=int)
    descargues = Descargue.query.order_by(Descargue.fecha.desc()).paginate(
        page=page, per_page=20, error_out=False)
    return render_template('medicion/historial_descargues.html', descargues=descargues)

# API routes
@main_bp.route('/api/tanques_stats')
@login_required
def api_tanques_stats():
    tanques = Tanque.query.all()
    stats = []
    
    for tanque in tanques:
        # Get latest measurement for this tank
        ultima_medicion = RegistroMedida.query.filter_by(idTanques=tanque.idTanques)\
            .order_by(RegistroMedida.fecha_hora_registro.desc()).first()
        
        current_level = ultima_medicion.galones if ultima_medicion else 0
        percentage = (current_level / float(tanque.capacidad_gal)) * 100 if tanque.capacidad_gal else 0
        
        stats.append({
            'id': tanque.idTanques,
            'tipo': tanque.tipo_combustible,
            'capacidad': float(tanque.capacidad_gal),
            'actual': current_level,
            'porcentaje': round(percentage, 1),
            'estado': 'normal' if percentage > 25 else 'bajo' if percentage > 10 else 'critico'
        })
    
    return jsonify(stats)