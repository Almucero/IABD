# Criterios de aceptación

## Consulta pública

1. Una petición `GET /` realizada sin iniciar sesión devuelve la página de inicio correctamente.
2. El inicio solo muestra artículos con `is_published` activado y los ordena de más reciente a más antiguo según `published_at`.
3. Cada artículo del inicio muestra título, categoría y resumen, y ofrece un enlace a su página de detalle.
4. Una petición `GET /categoria/<slug>/` muestra únicamente artículos publicados pertenecientes a esa categoría.
5. Una petición `GET /articulo/<slug>/` para un artículo publicado muestra el título, el contenido completo y la categoría.
6. Un artículo no publicado no aparece en el inicio ni en los listados de categoría; una petición a su URL de detalle devuelve `404` y no expone su contenido.
7. Desde una página interior se puede volver al inicio y navegar a las categorías disponibles.

## Administración

8. Una persona administradora puede crear y modificar categorías y artículos desde Django Admin.
9. La lista de artículos de Django Admin muestra título, categoría y estado de publicación, y permite buscar por título.

## Presentación adaptable

10. Las páginas de inicio, categoría y detalle se pueden leer y navegar sin desplazamiento horizontal en una ventana móvil de 375 × 667 píxeles y una ventana de escritorio de 1366 × 768 píxeles.
