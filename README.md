# Sitex

Sitex es una aplicación web de gestión desarrollada en Python usando Flask. Este repositorio contiene la lógica del back-end, modelos, rutas, utilidades y scripts auxiliares para administrar una aplicación típica (usuarios, tanques/elementos, envíos de correo, etc.). El README que sigue está pensado para que cualquiera (desarrollador o administrador) pueda instalar, ejecutar, entender la arquitectura básica y contribuir al proyecto.

> Nota: Este README se generó a partir de la estructura actual del repositorio. Revisa los archivos mencionados (por ejemplo `app_factory.py`, `extensions.py`, `models.py`, `routes.py`) para ajustar la configuración y variables de entorno a tu caso particular.

Tabla de contenidos
- [Características](#características)
- [Tecnologías](#tecnologías)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Requisitos previos](#requisitos-previos)
- [Instalación (desarrollo)](#instalación-desarrollo)
- [Variables de entorno (ejemplos)](#variables-de-entorno-ejemplos)
- [Base de datos y migraciones](#base-de-datos-y-migraciones)
- [Scripts útiles](#scripts-útiles)
- [Ejecución](#ejecución)
- [Correo y pruebas](#correo-y-pruebas)
- [Despliegue recomendado](#despliegue-recomendado)
- [Tests](#tests)
- [Contribuir](#contribuir)
- [Licencia](#licencia)
- [Contacto](#contacto)

Características
- Estructura modular de aplicación Flask con fábrica (`app_factory.py`).
- Modelos ORM y definición de entidades en `models.py`.
- Rutas y vistas centralizadas en `routes.py`.
- Formularios WTForms en `forms.py`.
- Inicialización de extensiones en `extensions.py`.
- Scripts de utilidad: creación de admin, siembra de datos, generación de archivos, arreglos específicos.
- Plantillas y estáticos en `templates/` y `static/`.
- Soporte para envío de correos (hay un archivo `test_email.py` y utilidades relacionadas).

Tecnologías
- Python (versión indicada en `runtime.txt`)
- Flask
- SQLAlchemy (u ORM similar, ver `models.py`)
- Flask-Migrate / Alembic (posible integración por la presencia de `migrations/`)
- WTForms
- Otras dependencias en `requirements.txt` o `pyproject.toml`

Estructura del proyecto (resumen)
- app_factory.py — factoría de la aplicación (create_app)
- main.py — punto de entrada simple
- routes.py — definición de rutas y controladores
- models.py — modelos de datos
- forms.py — formularios
- extensions.py — inicialización (DB, login, migrate, mail, etc.)
- utils.py — funciones auxiliares
- create_admin.py — crear usuario administrador
- seed_db.py — poblar BD con datos iniciales
- generar_archivos_carga.py, fix_tanques.py — utilidades de dominio específicas
- requirements.txt / pyproject.toml — dependencias
- templates/, static/ — recursos front-end
- instance/ — carpeta para base de datos local/archivos privados (no versionada)

Requisitos previos
- Python (la versión está en `runtime.txt`; usa la misma para evitar incompatibilidades)
- pip
- virtualenv o venv
- (Opcional) Postgres/MySQL u otra BD si no usas sqlite

Instalación (desarrollo)
1. Clona el repositorio:
   git clone https://github.com/camilo68/Sitex.git
   cd Sitex

2. Crea y activa un entorno virtual:
   python -m venv venv
   # Linux / macOS
   source venv/bin/activate
   # Windows (PowerShell)
   venv\Scripts\Activate.ps1
   # Windows (cmd)
   venv\Scripts\activate

3. Instala dependencias:
   pip install -r requirements.txt
   # o (si está configurado): pip install .

4. Crea carpeta instance (si es requerida para sqlite u otros archivos de configuración):
   mkdir -p instance

Variables de entorno (ejemplos)
Revisa `app_factory.py` y `extensions.py` para confirmar todas las variables que la app lee. Ejemplo de un archivo `.env` o variables necesarias:

FLASK_APP=main.py
FLASK_ENV=development
SECRET_KEY=TuSecretoMuySeguro
DATABASE_URL=sqlite:///instance/sitex.sqlite
# Si usas PostgreSQL: DATABASE_URL=postgresql://user:pass@host:5432/dbname

# Configuración de correo (si se usa)
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=tu_usuario
MAIL_PASSWORD=tu_password
MAIL_DEFAULT_SENDER=nombre <noreply@example.com>

# Otras variables específicas que puede requerir la app (revisa app_factory.py):
# EJEMPLO:
# SENTRY_DSN=...
# OAUTH_CLIENT_ID=...
# OAUTH_CLIENT_SECRET=...

Base de datos y migraciones
La estructura sugiere uso de migraciones (carpeta `migrations/`). Si la aplicación usa Flask-Migrate/Alembic sigue estos pasos:

1. Inicializar (solo la primera vez):
   flask db init

2. Generar una migración:
   flask db migrate -m "Mensaje de migración"

3. Aplicar migraciones:
   flask db upgrade

Si prefieres usar la base de datos SQLite local para pruebas rápidas:
- Asegúrate de que `DATABASE_URL` apunte a `sqlite:///instance/sitex.sqlite` y que la carpeta `instance/` exista.
- Ejecuta los scripts de inicialización o migraciones según el caso.

Scripts útiles (resumen)
- create_admin.py — crea un usuario administrador desde la consola (lee variables/env o pide input).
  Uso típico:
    python create_admin.py

- seed_db.py — puebla la base de datos con datos de ejemplo:
    python seed_db.py

- generar_archivos_carga.py — genera archivos de carga para procesos específicos del dominio.
- fix_tanques.py — script para transformar/arreglar datos relacionados con tanques (dominio).
- test_email.py — script para probar la configuración de correo.

Ejecución
Modo desarrollo (con Flask CLI):
1. Exporta variables de entorno:
   export FLASK_APP=main.py
   export FLASK_ENV=development
   # Windows PowerShell:
   $env:FLASK_APP = 'main.py'; $env:FLASK_ENV = 'development'

2. Ejecuta la app:
   flask run
   # o
   python main.py

Modo producción (ejemplo con Gunicorn):
   gunicorn -w 4 -b 0.0.0.0:8000 'app_factory:create_app()'
Ajusta el comando si tu factory function tiene otro nombre o si necesitas pasar configuración por entorno.

Correo y pruebas
- `test_email.py` contiene ejemplos/pruebas de envío de correo. Antes de ejecutar, asegúrate de configurar las variables `MAIL_*`.
- Para depuración, considera usar un servidor SMTP local (por ejemplo `mailhog` o `python -m smtpd -n -c DebuggingServer localhost:1025`) y apuntar MAIL_SERVER=localhost MAIL_PORT=1025.

Despliegue
- `runtime.txt` sugiere una versión de Python usada para despliegues (ej. Heroku). Verifica que la versión concuerde con tu entorno.
- Configura variables de entorno en la plataforma de despliegue (Heroku, Railway, Render, etc.).
- Usa una base de datos gestionada (Postgres) en producción en lugar de sqlite.
- Configura un servidor WSGI (gunicorn/uvicorn si es ASGI) y un proxy reverso (nginx) para producción.

Tests
- No se detectaron tests automáticos en la raíz (carpeta `tests/`) por ahora. Si quieres, puedo:
  - añadir una plantilla de pruebas con pytest,
  - integrar CI (GitHub Actions) para ejecutar tests y linters.

Buenas prácticas recomendadas
- No subir secretos al repositorio; usa variables de entorno o servicios secretos.
- Añadir un archivo `.env.example` con el listado de variables necesarias (sin valores reales).
- Añadir linter (flake8, black) y tests para asegurar calidad.

Contribuir
1. Abre un issue describiendo el cambio o bug.
2. Crea una rama basada en `main` nombrada `feature/<descripción>` o `fix/<descripción>`.
3. Haz tus cambios y asegúrate de que la app funcione localmente.
4. Abre un pull request con explicación, pasos para probar y capturas si aplica.

Plantilla sugerida para .env.example
SECRET_KEY=changeme
DATABASE_URL=sqlite:///instance/sitex.sqlite
FLASK_ENV=development
MAIL_SERVER=smtp.example.com
MAIL_PORT=587
MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_DEFAULT_SENDER=

Licencia
- Añade el archivo LICENSE según la licencia que quieras (por ejemplo MIT). Actualmente no hay un archivo de licencia en el repo. Si quieres, puedo añadir una plantilla MIT y abrir un PR.

Contacto
- Si necesitas que haga cambios concretos al README (más ejemplos, secciones técnicas específicas, añadir badges, CI, o abrir un PR con el README), dímelo y lo preparo.
- Puedo también:
  - generar `.env.example`,
  - añadir un archivo de CONTRIBUTING.md,
  - crear plantillas de issues/PRs,
  - o abrir un PR que añada este README directamente al repo.
```
