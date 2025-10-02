# app_factory.py - CORREGIDO
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import DeclarativeBase
import bcrypt
from flask_wtf import CSRFProtect

csrf = CSRFProtect()


class Base(DeclarativeBase):
    pass

# Inicializar extensiones
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    csrf.init_app(app)
    # ==========================
    # Configuración CORREGIDA
    # ==========================
    app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET', 'fallback-secret-key')
    # CORREGIDO: Configuración para MySQL
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/sitex_prueba'
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_recycle': 300,
        'pool_pre_ping': True,
    }
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    
    # Configuración de login_manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicie sesión para acceder a esta página.'
    login_manager.login_message_category = 'info'
    
    # ==========================
    # Cargador de usuario CORREGIDO
    # ==========================
    @login_manager.user_loader
    def load_user(user_id):
        from models import Empleado
        return db.session.get(Empleado, int(user_id))

    # ==========================
    # Importar modelos y blueprints
    # ==========================
    import models
    from routes import auth_bp, main_bp, dashboard_bp, medicion_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(medicion_bp)
    
    # ==========================
    # Crear datos base si no existen CORREGIDO
    # ==========================
    with app.app_context():
        db.create_all()
        
        from models import Empleado, Tanque
        # Verificar si ya existen datos
        if db.session.query(Empleado).count() == 0:
            print("No hay empleados, creando datos de ejemplo...")
            
            # Los datos ya existen en la BD según el SQL, no crear duplicados
            pass
        
        # Crear tanques si no existen
        if db.session.query(Tanque).count() == 0:
            tanque1 = Tanque(tipo_combustible='Diesel', capacidad=6000)
            tanque2 = Tanque(tipo_combustible='Diesel', capacidad=12000)
            tanque3 = Tanque(tipo_combustible='ACPM', capacidad=12000)
            tanque4 = Tanque(tipo_combustible='Extra', capacidad=6000)

            db.session.add_all([tanque1, tanque2, tanque3, tanque4])
            db.session.commit()
            print("Tanques creados con datos de ejemplo")
    
    return app