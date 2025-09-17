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
        
        # Create default admin user if none exists
        from models import Empleado
        admin_user = db.session.query(Empleado).filter_by(rol='admin').first()
        if not admin_user:
            admin_password = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            admin = Empleado()
            admin.nombre_empleado = 'Administrador'
            admin.apellido_empleado = 'Sistema'
            admin.numero_documento = '00000000'
            admin.tipo_documento = 'CC'
            admin.email = 'admin@sitex.com'
            admin.telefono = '0000000000'
            admin.direccion = 'Sistema'
            admin.cargo_establecido = 'admin'
            admin.contrasena = admin_password
            admin.usuario = 'admin'
            admin.temporal = False
            admin.confirmado = True
            admin.rol = 'admin'
            
            db.session.add(admin)
            db.session.commit()
            print("Usuario administrador creado: admin / admin123")
    
    return app