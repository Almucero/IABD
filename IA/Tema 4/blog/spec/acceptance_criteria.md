# Criterios de aceptación

## Portada y artículos

1. `GET /`, sin iniciar sesión, muestra el nombre del blog y los artículos publicados.
2. Los artículos de la portada aparecen en orden descendente de fecha de publicación.
3. Cada artículo de la portada muestra título, fecha y extracto, con un enlace a su detalle.
4. Si no hay artículos publicados, la portada muestra un mensaje informativo.
5. `GET /articulos/<slug>/` muestra el título, fecha, autor y cuerpo del artículo publicado.
6. El cuerpo presenta párrafos y subtítulos de forma legible; las líneas que empiezan por `## ` se muestran como subtítulos.
7. Una URL de artículo inexistente o no publicado devuelve `404` y no expone el contenido del borrador.

## Presentación del autor y navegación

8. `GET /sobre-mi/` muestra una presentación del autor cuyo texto se puede editar desde Django Admin.
9. La navegación principal ofrece enlaces claros a la portada y a «Sobre mí»; desde un artículo se puede volver a la portada.
10. La navegación básica funciona sin JavaScript.

## Administración y acceso

11. Un usuario autorizado de Django Admin puede crear, editar y retirar artículos y modificar la presentación del autor.
12. No hay registro público; las páginas de lectura están disponibles sin iniciar sesión y las operaciones administrativas requieren autenticación.

## Adaptabilidad y accesibilidad

13. Portada, artículo y «Sobre mí» se pueden leer y navegar sin desplazamiento horizontal en ventanas de 375 × 667 y 1366 × 768 píxeles.
14. Las páginas utilizan HTML semántico, encabezados ordenados y enlaces con etiquetas comprensibles; el sitio no necesita JavaScript para las funciones principales.
