import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase
import bcrypt

class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    # Create Flask app
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'fallback-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Login manager configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicie sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        from models import Empleado
        return db.session.get(Empleado, int(user_id))
    
    # Import models to ensure they are registered
    import models
    
    # Import and register blueprints
    from routes import auth_bp, main_bp, dashboard_bp, medicion_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(medicion_bp)
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Create default users if none exist
        from models import Empleado, Tanque
        existing_users = db.session.query(Empleado).count()
        if existing_users == 0:
            # Create admin user
            admin_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            admin = Empleado()
            admin.nombre_empleado = 'Administrador'
            admin.apellido_empleado = 'Hayuelos'
            admin.numero_documento = '00000000'
            admin.tipo_documento = 'CC'
            admin.email = 'admin@hayuelos.com'
            admin.telefono = '0000000000'
            admin.direccion = 'Estación de Servicios'
            admin.cargo_establecido = 'admin'
            admin.contrasena = admin_password
            admin.usuario = 'admin'
            admin.temporal = False
            admin.confirmado = True
            admin.rol = 'admin'
            
            # Create islero user
            islero_password = bcrypt.hashpw('islero123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            islero = Empleado()
            islero.nombre_empleado = 'Juan Carlos'
            islero.apellido_empleado = 'Rodriguez'
            islero.numero_documento = '12345678'
            islero.tipo_documento = 'CC'
            islero.email = 'islero@hayuelos.com'
            islero.telefono = '3001234567'
            islero.direccion = 'Bogotá'
            islero.cargo_establecido = 'islero'
            islero.contrasena = islero_password
            islero.usuario = 'islero'
            islero.temporal = False
            islero.confirmado = True
            islero.rol = 'islero'
            
            # Create encargado user
            encargado_password = bcrypt.hashpw('encargado123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            encargado = Empleado()
            encargado.nombre_empleado = 'Maria Elena'
            encargado.apellido_empleado = 'Gutierrez'
            encargado.numero_documento = '87654321'
            encargado.tipo_documento = 'CC'
            encargado.email = 'encargado@hayuelos.com'
            encargado.telefono = '3007654321'
            encargado.direccion = 'Bogotá'
            encargado.cargo_establecido = 'encargado'
            encargado.contrasena = encargado_password
            encargado.usuario = 'encargado'
            encargado.temporal = False
            encargado.confirmado = True
            encargado.rol = 'encargado'
            
            db.session.add(admin)
            db.session.add(islero)
            db.session.add(encargado)
            db.session.commit()
            print("Usuarios creados:")
            print("- admin / admin123 (Administrador)")
            print("- islero / islero123 (Islero)")
            print("- encargado / encargado123 (Encargado)")
        
        # Create default tanks if none exist
        existing_tanks = db.session.query(Tanque).count()
        if existing_tanks == 0:
            # Tanque 1 - Diesel
            tanque1 = Tanque()
            tanque1.tipo_combustible = 'Diesel'
            tanque1.contenido = 4500
            tanque1.capacidad_gal = 6000
            tanque1.volumen_m3 = 22.71
            tanque1.diametro_m = 2.50
            tanque1.altura_m = 4.63
            
            # Tanque 2 - Diesel
            tanque2 = Tanque()
            tanque2.tipo_combustible = 'Diesel'
            tanque2.contenido = 8000
            tanque2.capacidad_gal = 12000
            tanque2.volumen_m3 = 45.42
            tanque2.diametro_m = 2.50
            tanque2.altura_m = 9.25
            
            # Tanque 3 - ACPM
            tanque3 = Tanque()
            tanque3.tipo_combustible = 'ACPM'
            tanque3.contenido = 9500
            tanque3.capacidad_gal = 12000
            tanque3.volumen_m3 = 45.42
            tanque3.diametro_m = 2.50
            tanque3.altura_m = 9.25
            
            # Tanque 4 - Extra
            tanque4 = Tanque()
            tanque4.tipo_combustible = 'Extra'
            tanque4.contenido = 3200
            tanque4.capacidad_gal = 6000
            tanque4.volumen_m3 = 22.71
            tanque4.diametro_m = 2.50
            tanque4.altura_m = 4.63
            
            db.session.add(tanque1)
            db.session.add(tanque2)
            db.session.add(tanque3)
            db.session.add(tanque4)
            db.session.commit()
            print("Tanques de combustible creados con datos de ejemplo")
    
    return app