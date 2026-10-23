# Blog de acuariofilia

Proyecto de un blog divulgativo para personas que comienzan en la acuariofilia. Reúne artículos breves sobre cuidados y mantenimiento del acuario, alimentación y especies comunes. El contenido está pensado para orientar y no sustituye el consejo de un veterinario.

## Alcance

La primera versión contempla:

- Página de inicio con artículos publicados, ordenados del más reciente al más antiguo.
- Listados de artículos por categoría y páginas de detalle.
- Gestión de categorías y artículos desde Django Admin.
- Lectura pública sin necesidad de registrarse y diseño adaptable a móviles y ordenadores.

El alcance completo, incluidas las exclusiones de esta versión, está en [spec/scope.md](spec/scope.md).

## Documentación

- [Visión del producto](spec/vision.md): público, necesidad y valor.
- [Alcance](spec/scope.md): objetivo, funcionalidades incluidas y límites.
- [Criterios de aceptación](spec/acceptance_criteria.md): condiciones para verificar el comportamiento esperado.
- [PRD](PRD.md): requisitos funcionales y técnicos.
- [Briefing editorial y visual](briefing.md): temas, tono y dirección visual.

## Estructura del proyecto

El código ejecutable vive en `src/`; la raíz conserva documentación y configuración básica del entorno.

```text
src/
├── apps/
│   └── articles/ # Modelos, vistas, administración, pruebas y estáticos
├── config/       # Configuración y rutas del proyecto Django
├── templates/    # Plantillas compartidas
├── manage.py     # Comandos de Django
├── requirements.txt # Dependencias Python
└── db.sqlite3       # Base de datos SQLite local
```

## Tecnología prevista

Aplicación web con Django 5.2 y SQLite. El esquema de datos se gestiona mediante migraciones de Django.

## Preparar el entorno

Se necesita Python 3.10 o posterior. En Windows PowerShell, desde la raíz del proyecto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r src/requirements.txt
python src/manage.py migrate
python src/manage.py createsuperuser
python src/manage.py runserver
```

Abre `http://127.0.0.1:8000/` para visitar el blog y `http://127.0.0.1:8000/admin/` para administrar el contenido. Crea categorías y artículos desde el administrador; los artículos solo aparecerán públicamente cuando estén marcados como publicados.

Para ejecutar las pruebas:

```powershell
python src/manage.py test apps.articles
```

El `SECRET_KEY` y `DEBUG` generados en la configuración son solo para desarrollo local; deben sustituirse por configuración segura antes de desplegar el proyecto.

## Estado

El proyecto Django y la aplicación inicial del blog están creados. No se incluyen categorías ni artículos de ejemplo.
