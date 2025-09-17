from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, TextAreaField, DecimalField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange
from datetime import date

class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')

class EmpleadoForm(FlaskForm):
    nombre_empleado = StringField('Nombre', validators=[DataRequired(), Length(max=20)])
    apellido_empleado = StringField('Apellido', validators=[DataRequired(), Length(max=20)])
    numero_documento = StringField('Número de Documento', validators=[DataRequired(), Length(max=20)])
    tipo_documento = SelectField('Tipo de Documento', 
                                choices=[('CC', 'Cédula de Ciudadanía'), ('CE', 'Cédula de Extranjería'), ('PAS', 'Pasaporte')],
                                validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), Length(max=45)])
    telefono = StringField('Teléfono', validators=[Length(max=15)])
    direccion = StringField('Dirección', validators=[Length(max=45)])
    cargo_establecido = SelectField('Cargo', 
                                  choices=[('islero', 'Islero'), ('encargado', 'Encargado'), ('admin', 'Administrador')],
                                  validators=[DataRequired()])
    rol = SelectField('Rol', 
                     choices=[('usuario', 'Usuario'), ('admin', 'Administrador')],
                     validators=[DataRequired()])

class MedicionForm(FlaskForm):
    medida_combustible = StringField('Medida (cm)', validators=[DataRequired()])
    galones = IntegerField('Galones', validators=[DataRequired(), NumberRange(min=0)])
    tanque = SelectField('Tanque', coerce=int, validators=[DataRequired()])
    tipo_medida = SelectField('Tipo de Medición',
                             choices=[('rutinario', 'Rutinario'), ('cargue', 'Cargue'), ('descargue', 'Descargue')],
                             default='rutinario',
                             validators=[DataRequired()])
    novedad = TextAreaField('Novedad', validators=[Optional(), Length(max=255)])

class DescargueForm(FlaskForm):
    tanque = StringField('Tanque', validators=[DataRequired(), Length(max=50)])
    medida_inicial_cm = DecimalField('Medida Inicial (cm)', validators=[DataRequired()], places=2)
    medida_inicial_gl = DecimalField('Medida Inicial (gl)', validators=[DataRequired()], places=2)
    descargue_cm = DecimalField('Descargue (cm)', validators=[DataRequired()], places=2)
    descargue_gl = DecimalField('Descargue (gl)', validators=[DataRequired()], places=2)
    medida_final_cm = DecimalField('Medida Final (cm)', validators=[DataRequired()], places=2)
    medida_final_gl = DecimalField('Medida Final (gl)', validators=[DataRequired()], places=2)
    diferencia = DecimalField('Diferencia', validators=[Optional()], places=2)
    
    # Safety equipment checkboxes
    kit_derrames = SelectField('Kit Derrames', choices=[('si', 'Sí'), ('no', 'No')], default='si')
    extintores = SelectField('Extintores', choices=[('si', 'Sí'), ('no', 'No')], default='si')
    conos = SelectField('Conos', choices=[('si', 'Sí'), ('no', 'No')], default='si')
    boquillas = SelectField('Boquillas', choices=[('si', 'Sí'), ('no', 'No')], default='si')
    botas = SelectField('Botas', choices=[('si', 'Sí'), ('no', 'No')], default='si')
    gafas = SelectField('Gafas', choices=[('si', 'Sí'), ('no', 'No')], default='si')
    tapaoidos = SelectField('Tapaoídos', choices=[('si', 'Sí'), ('no', 'No')], default='si')
    guantes = SelectField('Guantes', choices=[('si', 'Sí'), ('no', 'No')], default='si')
    
    # Fuel quality checks
    brillante = SelectField('Brillante', choices=[('si', 'Sí'), ('no', 'No')], default='si')
    traslucido = SelectField('Traslúcido', choices=[('si', 'Sí'), ('no', 'No')], default='si')
    claro = SelectField('Claro', choices=[('si', 'Sí'), ('no', 'No')], default='si')
    solidos = SelectField('Sólidos', choices=[('si', 'Sí'), ('no', 'No')], default='no')
    
    separacion = StringField('Separación', validators=[Optional(), Length(max=50)])
    observaciones1 = TextAreaField('Observaciones 1', validators=[Optional(), Length(max=255)])
    observaciones2 = TextAreaField('Observaciones 2', validators=[Optional(), Length(max=255)])
    fecha = DateField('Fecha', validators=[Optional()], default=date.today)

class CargueForm(FlaskForm):
    tanque = SelectField('Tanque', coerce=int, validators=[DataRequired()])
    medicion_anterior = StringField('Medición Anterior', validators=[DataRequired()])
    medicion_posterior = StringField('Medición Posterior', validators=[DataRequired()])
    formato_de_entrega = StringField('Formato de Entrega', validators=[DataRequired()])
    galones_totales = StringField('Galones Totales', validators=[DataRequired()])

class PedidoCombustibleForm(FlaskForm):
    galones_acpm = StringField('Galones ACPM', validators=[Optional()])
    galones_corriente = StringField('Galones Corriente', validators=[Optional()])
    galones_extra = StringField('Galones Extra', validators=[Optional()])
    total_galones = StringField('Total Galones', validators=[DataRequired()])