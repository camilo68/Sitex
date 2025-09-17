from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from app_factory import db

class Empleado(UserMixin, db.Model):
    __tablename__ = 'empleado'
    
    idEmpleados = db.Column(db.Integer, primary_key=True)
    nombre_empleado = db.Column(db.String(20))
    apellido_empleado = db.Column(db.String(20))
    numero_documento = db.Column(db.String(20))
    tipo_documento = db.Column(db.String(20))
    email = db.Column(db.String(45))
    telefono = db.Column(db.String(15))
    direccion = db.Column(db.String(45))
    cargo_establecido = db.Column(db.String(45))
    contrasena = db.Column(db.String(255))
    usuario = db.Column(db.String(15))
    temporal = db.Column(db.Boolean, default=True)
    confirmado = db.Column(db.Boolean, default=False)
    rol = db.Column(db.String(20), default='usuario')
    
    # Flask-Login required methods
    def get_id(self):
        return str(self.idEmpleados)
    
    # Relationships
    descargues = db.relationship('Descargue', backref='empleado', lazy=True)
    mediciones_cargue = db.relationship('MedicionCargue', backref='empleado', lazy=True)
    registro_medidas = db.relationship('RegistroMedida', backref='empleado', lazy=True)
    pedidos_combustible = db.relationship('PedidoCombustible', backref='empleado', lazy=True)
    documentos = db.relationship('Documento', backref='empleado', lazy=True)
    
    def __repr__(self):
        return f'<Empleado {self.nombre_empleado} {self.apellido_empleado}>'

class Tanque(db.Model):
    __tablename__ = 'tanques'
    
    idTanques = db.Column(db.Integer, primary_key=True)
    tipo_combustible = db.Column(db.String(45))
    contenido = db.Column(db.Integer)
    capacidad_gal = db.Column(db.Numeric(10, 2), nullable=False)
    volumen_m3 = db.Column(db.Numeric(10, 2), nullable=False)
    diametro_m = db.Column(db.Numeric(10, 2), nullable=False)
    altura_m = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Relationships
    mediciones_cargue = db.relationship('MedicionCargue', backref='tanque', lazy=True)
    registro_medidas = db.relationship('RegistroMedida', backref='tanque', lazy=True)
    ventas = db.relationship('Venta', backref='tanque', lazy=True)
    
    def __repr__(self):
        return f'<Tanque {self.tipo_combustible} - {self.capacidad_gal} gal>'

class Descargue(db.Model):
    __tablename__ = 'descargues'
    
    idDescargue = db.Column(db.Integer, primary_key=True)
    idEmpleados = db.Column(db.Integer, db.ForeignKey('empleado.idEmpleados'), nullable=False)
    medida_inicial_cm = db.Column(db.Numeric(10, 2))
    medida_inicial_gl = db.Column(db.Numeric(10, 2))
    descargue_cm = db.Column(db.Numeric(10, 2))
    descargue_gl = db.Column(db.Numeric(10, 2))
    medida_final_cm = db.Column(db.Numeric(10, 2))
    medida_final_gl = db.Column(db.Numeric(10, 2))
    diferencia = db.Column(db.Numeric(10, 2))
    tanque = db.Column(db.String(50))
    observaciones1 = db.Column(db.String(255))
    observaciones2 = db.Column(db.String(255))
    kit_derrames = db.Column(db.String(5))
    extintores = db.Column(db.String(5))
    conos = db.Column(db.String(5))
    boquillas = db.Column(db.String(5))
    botas = db.Column(db.String(5))
    gafas = db.Column(db.String(5))
    tapaoidos = db.Column(db.String(5))
    guantes = db.Column(db.String(5))
    brillante = db.Column(db.String(5))
    traslucido = db.Column(db.String(5))
    claro = db.Column(db.String(5))
    solidos = db.Column(db.String(5))
    separacion = db.Column(db.String(50))
    fecha = db.Column(db.Date)
    
    def __repr__(self):
        return f'<Descargue {self.tanque} - {self.fecha}>'

class MedicionCargue(db.Model):
    __tablename__ = 'medicion_cargue'
    
    idMedicion_cargue = db.Column(db.Integer, primary_key=True)
    idEmpleados = db.Column(db.Integer, db.ForeignKey('empleado.idEmpleados'), nullable=False)
    medicion_anterior = db.Column(db.String(45))
    medicion_posterior = db.Column(db.String(45))
    formato_de_entrega = db.Column(db.String(45))
    galones_totales = db.Column(db.String(45))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    idTanques = db.Column(db.Integer, db.ForeignKey('tanques.idTanques'))
    
    def __repr__(self):
        return f'<MedicionCargue {self.galones_totales} - {self.fecha}>'

class RegistroMedida(db.Model):
    __tablename__ = 'registro_medidas'
    
    idRegistro_medidas = db.Column(db.Integer, primary_key=True)
    medida_combustible = db.Column(db.String(45))
    idEmpleados = db.Column(db.Integer, db.ForeignKey('empleado.idEmpleados'))
    fecha_hora_registro = db.Column(db.DateTime)
    galones = db.Column(db.Integer)
    idTanques = db.Column(db.Integer, db.ForeignKey('tanques.idTanques'))
    tipo_medida = db.Column(db.String(30), default='rutinario')
    novedad = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<RegistroMedida {self.galones} gal - {self.fecha_hora_registro}>'

class PedidoCombustible(db.Model):
    __tablename__ = 'pedido_combustible'
    
    idPedido_Combustible = db.Column(db.Integer, primary_key=True)
    galones_acpm = db.Column(db.String(45))
    galones_corriente = db.Column(db.String(45))
    galones_extra = db.Column(db.String(45))
    total_galones = db.Column(db.String(45))
    idEmpleados = db.Column(db.Integer, db.ForeignKey('empleado.idEmpleados'))
    
    def __repr__(self):
        return f'<PedidoCombustible {self.total_galones} gal>'

class Documento(db.Model):
    __tablename__ = 'documento'
    
    idDocumento = db.Column(db.Integer, primary_key=True)
    nombre_documento = db.Column(db.String(100))
    fecha_informe = db.Column(db.Date)
    tipo_documento_informe = db.Column(db.String(45))
    tipo_medicion = db.Column(db.String(45))
    fecha_descargue = db.Column(db.Date)
    id_empleado = db.Column(db.String(45))
    idEmpleados = db.Column(db.Integer, db.ForeignKey('empleado.idEmpleados'))
    revision_vehiculo = db.Column(db.String(3))
    revision_conductor = db.Column(db.String(3))
    medida_inicial = db.Column(db.String(45))
    cantidad_descargue = db.Column(db.String(45))
    medida_final = db.Column(db.String(45))
    diferencias = db.Column(db.String(45))
    idRegistro_medidas = db.Column(db.Integer, db.ForeignKey('registro_medidas.idRegistro_medidas'))
    
    # Relationships
    adjuntos = db.relationship('DocumentoAdjunto', backref='documento', lazy=True)
    historial = db.relationship('DocumentoHistorial', backref='documento', lazy=True)
    
    def __repr__(self):
        return f'<Documento {self.nombre_documento}>'

class DocumentoAdjunto(db.Model):
    __tablename__ = 'documento_adjunto'
    
    idAdjunto = db.Column(db.Integer, primary_key=True)
    idDocumento = db.Column(db.Integer, db.ForeignKey('documento.idDocumento'))
    nombre_archivo = db.Column(db.String(100))
    url_archivo = db.Column(db.Text)
    fecha_subida = db.Column(db.DateTime)

class DocumentoHistorial(db.Model):
    __tablename__ = 'documento_historial'
    
    idHistorial = db.Column(db.Integer, primary_key=True)
    idDocumento = db.Column(db.Integer, db.ForeignKey('documento.idDocumento'))
    fecha_evento = db.Column(db.DateTime)
    descripcion_evento = db.Column(db.String(255))
    usuario_responsable = db.Column(db.String(45))

class DocumentoTipo(db.Model):
    __tablename__ = 'documento_tipo'
    
    idTipoDocumento = db.Column(db.Integer, primary_key=True)
    nombre_tipo = db.Column(db.String(45))

class Venta(db.Model):
    __tablename__ = 'ventas'
    
    idVenta = db.Column(db.Integer, primary_key=True)
    idTanque = db.Column(db.Integer, db.ForeignKey('tanques.idTanques'))
    cantidad_galones = db.Column(db.Integer)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Venta {self.cantidad_galones} gal - {self.fecha}>'

class InicioSesion(db.Model):
    __tablename__ = 'inicio_de_sesion'
    
    userNumDoc = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(255))
    temporal = db.Column(db.Boolean, default=False)

class InicioSesionEmpleado(db.Model):
    __tablename__ = 'inicio_de_sesion_has_empleado'
    
    idEmpleados = db.Column(db.Integer, db.ForeignKey('empleado.idEmpleados'), primary_key=True)
    userNumDoc = db.Column(db.String(20), db.ForeignKey('inicio_de_sesion.userNumDoc'), primary_key=True)

class RegistroMedidaMedicionCargue(db.Model):
    __tablename__ = 'registro_medidas_has_medicion_cargue'
    
    idRegistro_medidas = db.Column(db.Integer, db.ForeignKey('registro_medidas.idRegistro_medidas'), primary_key=True)
    idMedicion_cargue = db.Column(db.Integer, db.ForeignKey('medicion_cargue.idMedicion_cargue'), primary_key=True)