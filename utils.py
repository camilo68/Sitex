from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def roles_required(*roles):
    """
    Decorador para verificar que el usuario tiene uno de los roles requeridos
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Debe iniciar sesión para acceder a esta página', 'error')
                return redirect(url_for('auth.login'))
            
            if current_user.rol not in roles:
                flash(f'No tiene permisos para acceder a esta función. Se requiere rol: {", ".join(roles)}', 'error')
                return redirect(url_for('dashboard.index'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def islero_required(f):
    """
    Decorador específico para funciones que solo puede realizar un islero
    """
    return roles_required('islero')(f)

def admin_or_encargado_required(f):
    """
    Decorador para funciones que pueden realizar administradores o encargados
    """
    return roles_required('admin', 'encargado')(f)