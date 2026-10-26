# Bitácora Robótica

Blog en español para publicar y leer artículos sobre robótica. Incluye una portada con publicaciones recientes, páginas individuales de artículo y una sección «Sobre mí» editable. Los artículos y la presentación del autor se mantienen desde Django Admin; no hay registro público ni comentarios.

## Documentación del producto

- [Visión](spec/vision.md): personas destinatarias y valor del blog.
- [Alcance](spec/scope.md): objetivos y límites de la primera versión.
- [Criterios de aceptación](spec/acceptance_criteria.md): comportamiento verificable.
- [PRD](PRD.md): requisitos funcionales y técnicos.
- [Briefing](briefing.md): orientación editorial y visual.

## Estructura

```text
src/
├── apps/
│   └── articles/       # Modelos, vistas, administración, pruebas y CSS
├── config/             # Configuración Django y rutas
├── templates/          # Plantillas HTML
├── media/
│   └── images/          # Ilustraciones e imágenes del proyecto
├── db.sqlite3          # Base de datos local
├── manage.py           # Comandos Django
└── requirements.txt    # Dependencias Python
spec/                   # Documentación del producto
```

## Preparar y ejecutar en Windows

Se necesita Python 3.10 o posterior. Desde la raíz del proyecto, en PowerShell:

```powershell
# Solo la primera vez, si aún no existe el entorno:
py -m venv .venv

# Activar el entorno virtual en PowerShell:
.\.venv\Scripts\Activate.ps1

# Instalar dependencias y preparar la base de datos:
python -m pip install -r src/requirements.txt
python src/manage.py migrate

# Crear un administrador y arrancar el servidor:
python src/manage.py createsuperuser
python src/manage.py runserver
```

Si PowerShell bloquea la activación de scripts, permite la ejecución solo en la sesión actual y vuelve a activar el entorno:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Visita `http://127.0.0.1:8000/` para leer el blog y `http://127.0.0.1:8000/admin/` para editar artículos o la presentación «Sobre mí». La base de datos empieza con tres artículos de ejemplo, editables o eliminables desde el panel.

`createsuperuser` solicita nombre de usuario, correo (opcional) y contraseña de forma interactiva. Para cambiar la contraseña posteriormente, usa:

```powershell
python src/manage.py changepassword nombre_de_usuario
```

Cada artículo tiene el campo booleano **Publicado**: marcado significa `True` y muestra el artículo en el blog; desmarcado significa `False` y lo mantiene como borrador privado.

El contenido de cada artículo admite párrafos separados por una línea en blanco. Para añadir subtítulos, comienza una línea con `## `.

Las imágenes del proyecto se guardan bajo `src/media/` (por ejemplo, en `src/media/images/`). En desarrollo, Django las sirve desde `/media/`; en producción, el servidor web o el almacenamiento de despliegue debe servir esa carpeta.

## Pruebas

```powershell
python src/manage.py test apps.articles
```

La clave secreta y `DEBUG` de la configuración son solo para desarrollo local. Antes de desplegar, configura valores seguros y específicos del entorno.
