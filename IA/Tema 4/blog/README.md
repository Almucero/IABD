# Bitácora Robótica

Blog en español sobre robótica, desarrollado con Django. Permite leer artículos publicados, consultar la sección «Sobre mí» y administrar el contenido desde Django Admin.

## Contenido

- [Puesta en marcha](#puesta-en-marcha)
- [API de artículos](#api-de-artículos)
- [Pruebas](#pruebas)
- [Documentación del proyecto](#documentación-del-proyecto)

## Puesta en marcha

Requisitos: Python 3.10 o posterior. Los comandos de esta guía son para Windows PowerShell; en otros sistemas, la sintaxis puede variar.

### Primera instalación

1. Crea y activa el entorno virtual; instala las dependencias:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install -r src/requirements.txt
   ```

2. Crea una clave secreta para Django:

   ```powershell
   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```

3. **Crea manualmente un archivo llamado `.env` en la raíz**, junto a este README. Abre `.env.example`, copia su contenido en el archivo nuevo y reemplaza `SECRET_KEY` por la clave generada:

   ```dotenv
   SECRET_KEY=pega_aqui_la_clave_generada
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost
   BLOG_API_TOKEN=
   ```

   El archivo debe llamarse exactamente `.env` (no `.env.txt`) y no puede quedar vacío. `.env.example` es solo una plantilla: Django carga `.env` automáticamente. No compartas ni subas `.env` al repositorio.

   **Para qué sirve cada variable:**

   | Variable         | Uso                                                                                                                                                                                                                    |
   | ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | `SECRET_KEY`     | Obligatoria. Django la usa internamente para firmar datos (por ejemplo, tokens de restablecimiento de contraseña y datos firmados). No es el token de la API; genera una clave aleatoria y mantenla privada y estable. |
   | `DEBUG`          | Activa el modo de desarrollo. Usa `True` solo localmente; en producción debe ser `False`.                                                                                                                              |
   | `ALLOWED_HOSTS`  | Lista de nombres de host aceptados por Django. Los valores del ejemplo son para desarrollo local.                                                                                                                      |
   | `BLOG_API_TOKEN` | Token opcional para las solicitudes API desde la terminal; Django no lo usa como ajuste.                                                                                                                               |

4. Prepara la base de datos y crea la cuenta administradora:

   ```powershell
   python src/manage.py migrate
   python src/manage.py createsuperuser
   ```

   Las migraciones crean también las tablas que necesita el sistema de tokens. `createsuperuser` se hace una vez; el nombre de usuario que elijas se usará después para generar el token de API.

5. Arranca el sitio:

   ```powershell
   python src/manage.py runserver
   ```

   Blog: <http://127.0.0.1:8000/> · Administración: <http://127.0.0.1:8000/admin/>

### Arranques siguientes

En cada nueva terminal, activa el entorno y arranca el servidor:

```powershell
.\.venv\Scripts\Activate.ps1
python src/manage.py runserver
```

No repitas la creación del entorno, la instalación de dependencias ni `createsuperuser`. Ejecuta `python src/manage.py migrate` cuando actualices el proyecto y haya migraciones nuevas. La base local `src/db.sqlite3` conserva artículos y cuentas; no la borres para iniciar el servidor.

## API de artículos

| Método | Ruta                   | Acceso                 | Resultado                  |
| ------ | ---------------------- | ---------------------- | -------------------------- |
| `GET`  | `/api/articulos/`      | Público                | Lista artículos publicados |
| `GET`  | `/api/articulos/<id>/` | Público                | Artículo publicado o `404` |
| `POST` | `/api/articulos/`      | Token de administrador | Crea un borrador           |

Las respuestas contienen `id`, `titulo`, `cuerpo` y `estado`. La API oculta borradores en las consultas públicas. Para crear uno, el cuerpo JSON requiere `titulo` y `cuerpo`.

### Token y pruebas de la API

Después de completar la primera instalación y crear el superusuario, genera el token con el nombre real de esa cuenta (sustituye `mi_usuario`):

```powershell
python src/manage.py drf_create_token mi_usuario
```

Añade el token que imprime a `BLOG_API_TOKEN=` en el `.env` de la raíz. El token es distinto de `SECRET_KEY`. Para cargarlo en la terminal PowerShell actual, lee su valor desde `.env`:

```powershell
$env:BLOG_API_TOKEN = ((Get-Content .env | Where-Object { $_ -like 'BLOG_API_TOKEN=*' } | Select-Object -First 1) -replace '^BLOG_API_TOKEN=', '').Trim()
```

Con el servidor ejecutándose, prueba primero las consultas públicas. No necesitan token:

```powershell
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/articulos/'
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/articulos/1/'
```

#### Probar un POST desde la terminal

El siguiente bloque muestra cómo enviar un `POST` desde PowerShell y crear un borrador de ejemplo. Puedes cambiar el título y el cuerpo por cualquier texto no vacío; ambos campos son obligatorios. El artículo se guardará como borrador y no se publicará automáticamente. `Invoke-RestMethod` evita el alias de `curl` de PowerShell y los problemas de comillas/UTF-8 al enviar JSON:

```powershell
$headers = @{ Authorization = "Token $env:BLOG_API_TOKEN" }
$payload = @{ titulo = 'Robot de aula'; cuerpo = "Prueba`ndidáctica." } | ConvertTo-Json -Compress
$body = [System.Text.Encoding]::UTF8.GetBytes($payload)
Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/articulos/' `
  -Method Post -Headers $headers `
  -ContentType 'application/json; charset=utf-8' -Body $body
```

La respuesta correcta es `201 Created` y muestra `estado: "borrador"`. El artículo no será visible públicamente hasta publicarlo desde Django Admin. `400` indica datos ausentes o vacíos, `401` token ausente o inválido y `403` usuario sin permisos de administración. Para invalidar un token expuesto o reemplazarlo, ejecuta `python src/manage.py drf_create_token --reset mi_usuario` y actualiza `BLOG_API_TOKEN` en `.env`.

## Pruebas

Desde la raíz, con el entorno virtual activo y `.env` configurado:

```powershell
python src/manage.py test apps.articles
```

## Documentación del proyecto

- [Visión](spec/vision.md): público, valor y principios.
- [Alcance](spec/scope.md): funciones incluidas y excluidas.
- [Criterios de aceptación](spec/acceptance_criteria.md): comportamiento verificable.
- [PRD](PRD.md): requisitos funcionales y técnicos.
- [Briefing](briefing.md): orientación editorial y visual.

Para publicar el sitio, configura una `SECRET_KEY` propia, `DEBUG=False` y los `ALLOWED_HOSTS` del entorno. No uses en producción los valores locales de ejemplo.
