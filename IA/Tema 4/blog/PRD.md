# PRD: blog sobre peces con Django

Este documento concreta los requisitos funcionales y técnicos de implementación. El objetivo y los límites de producto se definen en [spec/scope.md](spec/scope.md); la dirección editorial y visual, en [briefing.md](briefing.md).

## 1. Datos

Crear una aplicación Django para el blog con los siguientes modelos:

### `Category`

- `name`: nombre visible de la categoría.
- `slug`: identificador único utilizado en la URL.

### `Article`

- `title`: título del artículo.
- `slug`: identificador único utilizado en la URL.
- `summary`: resumen breve para los listados.
- `body`: contenido completo del artículo.
- `category`: relación obligatoria con `Category`.
- `created_at`: fecha de creación automática.
- `updated_at`: fecha de modificación automática.
- `published_at`: fecha y hora de publicación; puede estar vacía mientras el artículo no se haya publicado.
- `is_published`: indicador de publicación y visibilidad pública.

Usar migraciones de Django para crear y modificar el esquema. SQLite es suficiente para la configuración inicial.

## 2. Administración de contenido

- Registrar `Category` y `Article` en Django Admin.
- Permitir crear y editar los campos de ambos modelos.
- En la lista de artículos, mostrar título, categoría y estado de publicación.
- Permitir buscar artículos por título.
- El contenido no publicado debe quedar excluido de todas las páginas públicas.

## 3. Páginas y rutas públicas

- `GET /`: listado de artículos publicados, del más reciente al más antiguo.
- `GET /categoria/<slug>/`: listado de artículos publicados asociados a la categoría indicada.
- `GET /articulo/<slug>/`: detalle de un artículo publicado.

Las consultas públicas deben filtrar por `is_published`. Se pueden implementar con vistas genéricas de Django (`ListView` y `DetailView`) o vistas equivalentes.

## 4. Plantillas y recursos estáticos

- Crear plantillas para el inicio, el listado de categoría y el detalle de artículo.
- Reutilizar una plantilla base para la estructura y navegación comunes.
- Servir los estilos CSS mediante el sistema de archivos estáticos de Django.
- Incluir enlaces a categorías y una forma de volver al inicio desde las páginas interiores.
- En los listados, mostrar título, categoría y resumen; cada artículo debe enlazar a su detalle.
- En el detalle, mostrar el contenido completo y su categoría.
