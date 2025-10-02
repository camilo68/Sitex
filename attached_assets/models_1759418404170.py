# models.py - CORREGIDO con alias de compatibilidad
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from app_factory import db

class Empleado(db.Model, UserMixin):
    __tablename__ = 'empleado'
    id_empleados = db.Column(db.Integer, primary_key=True)
    nombre_empleado = db.Column(db.String(30), nullable=False)
    apellido_empleado = db.Column(db.String(30), nullable=False)
    numero_documento = db.Column(db.String(20), unique=True, nullable=False)
    tipo_documento = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(45), unique=True, nullable=False)
    telefono = db.Column(db.String(15))
    direccion = db.Column(db.String(45))
    cargo_establecido = db.Column(db.String(45))
    usuario = db.Column(db.String(15), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    temporal = db.Column(db.Boolean, default=True)

    # Relaciones
    descargues = db.relationship("Descargue", back_populates="empleado", lazy=True)
    mediciones_cargue = db.relationship("MedicionCargue", back_populates="empleado", lazy=True)
    registro_medidas = db.relationship("RegistroMedida", back_populates="empleado", lazy=True)
    pedidos_combustible = db.relationship("PedidoCombustible", back_populates="empleado", lazy=True)
    documentos = db.relationship("Documento", back_populates="empleado", lazy=True)

    # Alias de compatibilidad
    @property
    def idEmpleados(self):
        return self.id_empleados

    # Flask-Login
    def get_id(self):
        return str(self.id_empleados)

    @property
    def rol(self):
        return self.cargo_establecido

    @property
    def confirmado(self):
        return not self.temporal

    def __repr__(self):
        return f'<Empleado {self.nombre_empleado} {self.apellido_empleado}>'

    def check_password(self, raw_password):
        import bcrypt
        if not getattr(self, 'contrasena', None):
            return False
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.contrasena.encode('utf-8'))

    @property
    def is_locked(self):
        return False


class Tanque(db.Model):
    __tablename__ = 'tanques'
    id_tanques = db.Column(db.Integer, primary_key=True)
    tipo_combustible = db.Column(db.String(45))
    capacidad = db.Column(db.Integer)

    # Relaciones
    mediciones_cargue = db.relationship("MedicionCargue", back_populates="tanque", lazy=True)
    registro_medidas = db.relationship("RegistroMedida", back_populates="tanque", lazy=True)
    ventas = db.relationship("Venta", back_populates="tanque", lazy=True)

    # Alias de compatibilidad
    @property
    def idTanques(self):
        return self.id_tanques

    @property
    def capacidad_gal(self):
        return self.capacidad

    @property
    def contenido(self):
        ultima_medicion = RegistroMedida.query.filter_by(
            id_tanques=self.id_tanques
        ).order_by(RegistroMedida.fecha_hora_registro.desc()).first()
        return ultima_medicion.galones if ultima_medicion else 0

    @property
    def volumen_m3(self):
        return round(self.capacidad * 3.78541 / 1000, 2) if self.capacidad else 0

    @property
    def diametro_m(self):
        return 2.5

    @property
    def altura_m(self):
        return 4.6

    def __repr__(self):
        return f'<Tanque {self.tipo_combustible} - {self.capacidad} gal>'


class Descargue(db.Model):
    __tablename__ = 'descargues'
    idDescargue = db.Column(db.Integer, primary_key=True)
    id_empleados = db.Column(db.Integer, db.ForeignKey('empleado.id_empleados'), nullable=False)

    empleado = db.relationship("Empleado", back_populates="descargues")

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
    id_medicion_cargue = db.Column(db.Integer, primary_key=True)
    medida_anterior = db.Column(db.String(45))
    medida_posterior = db.Column(db.String(45))
    formato_de_entrega = db.Column(db.String(45))
    galones_totales = db.Column(db.String(45))
    id_tanques = db.Column(db.Integer, db.ForeignKey('tanques.id_tanques'))
    id_empleados = db.Column(db.Integer, db.ForeignKey('empleado.id_empleados'))
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    empleado = db.relationship("Empleado", back_populates="mediciones_cargue")
    tanque = db.relationship("Tanque", back_populates="mediciones_cargue")

    # Alias
    @property
    def idMedicion_cargue(self):
        return self.id_medicion_cargue

    @property
    def idEmpleados(self):
        return self.id_empleados

    @property
    def idTanques(self):
        return self.id_tanques

    def __repr__(self):
        return f'<MedicionCargue {self.galones_totales} - {self.fecha}>'


class RegistroMedida(db.Model):
    __tablename__ = 'registro_medidas'
    id_registro_medidas = db.Column(db.Integer, primary_key=True)
    medida_combustible = db.Column(db.String(45))
    id_empleados = db.Column(db.Integer, db.ForeignKey('empleado.id_empleados'))
    fecha_hora_registro = db.Column(db.DateTime)
    galones = db.Column(db.Integer)
    id_tanques = db.Column(db.Integer, db.ForeignKey('tanques.id_tanques'))
    novedad = db.Column(db.String(255))
    tipo_medida = db.Column(db.String(30), default='rutinario')

    empleado = db.relationship("Empleado", back_populates="registro_medidas")
    tanque = db.relationship("Tanque", back_populates="registro_medidas")

    # Alias
    @property
    def idRegistro_medidas(self):
        return self.id_registro_medidas

    @property
    def idEmpleados(self):
        return self.id_empleados

    @property
    def idTanques(self):
        return self.id_tanques

    def __repr__(self):
        return f'<RegistroMedida {self.galones} gal - {self.fecha_hora_registro}>'


class PedidoCombustible(db.Model):
    __tablename__ = 'pedido_combustible'
    idPedido_Combustible = db.Column(db.Integer, primary_key=True)
    galones_acpm = db.Column(db.String(45))
    galones_corriente = db.Column(db.String(45))
    galones_extra = db.Column(db.String(45))
    total_galones = db.Column(db.String(45))
    id_empleados = db.Column(db.Integer, db.ForeignKey('empleado.id_empleados'))

    empleado = db.relationship("Empleado", back_populates="pedidos_combustible")

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
    id_empleados = db.Column(db.Integer, db.ForeignKey('empleado.id_empleados'))
    revision_vehiculo = db.Column(db.String(3))
    revision_conductor = db.Column(db.String(3))
    medida_inicial = db.Column(db.String(45))
    cantidad_descargue = db.Column(db.String(45))
    medida_final = db.Column(db.String(45))
    diferencias = db.Column(db.String(45))
    id_registro_medidas = db.Column(db.Integer, db.ForeignKey('registro_medidas.id_registro_medidas'))

    empleado = db.relationship("Empleado", back_populates="documentos")
    adjuntos = db.relationship("DocumentoAdjunto", backref="documento", lazy=True)
    historial = db.relationship("DocumentoHistorial", backref="documento", lazy=True)

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
    id_tanques = db.Column(db.Integer, db.ForeignKey('tanques.id_tanques'))
    cantidad_galones = db.Column(db.Integer)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    tanque = db.relationship("Tanque", back_populates="ventas")

    def __repr__(self):
        return f'<Venta {self.cantidad_galones} gal - {self.fecha}>'


class InicioSesion(db.Model):
    __tablename__ = 'inicio_de_sesion'
    userNumDoc = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(255))
    temporal = db.Column(db.Boolean, default=False)


class InicioSesionEmpleado(db.Model):
    __tablename__ = 'inicio_de_sesion_has_empleado'
    id_empleados = db.Column(db.Integer, db.ForeignKey('empleado.id_empleados'), primary_key=True)
    userNumDoc = db.Column(db.String(20), db.ForeignKey('inicio_de_sesion.userNumDoc'), primary_key=True)


class RegistroMedidaMedicionCargue(db.Model):
    __tablename__ = 'registro_medidas_has_medicion_cargue'
    id_registro_medidas = db.Column(db.Integer, db.ForeignKey('registro_medidas.id_registro_medidas'), primary_key=True)
    id_medicion_cargue = db.Column(db.Integer, db.ForeignKey('medicion_cargue.id_medicion_cargue'), primary_key=True)
