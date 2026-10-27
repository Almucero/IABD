# Criterios de aceptación: Blog de robótica

## CA-01: Mostrar la portada y los artículos publicados

**Dado** que una persona visita el sitio sin iniciar sesión\
**Cuando** solicita `GET /`\
**Entonces** ve el nombre del blog y los artículos publicados\
**Y** la portada no muestra artículos en borrador.

## CA-02: Ordenar los artículos por fecha de publicación

**Dado** que existen varios artículos publicados con distintas fechas\
**Cuando** una persona consulta la portada\
**Entonces** los artículos aparecen en orden descendente de fecha de publicación\
**Y** los más recientes se muestran primero.

## CA-03: Enlazar cada artículo desde la portada

**Dado** que la portada muestra artículos publicados\
**Cuando** una persona consulta el resumen de un artículo\
**Entonces** ve su título, fecha y extracto\
**Y** puede abrir la página del artículo desde un enlace.

## CA-04: Informar cuando no hay artículos publicados

**Dado** que no existen artículos publicados\
**Cuando** una persona solicita `GET /`\
**Entonces** la portada muestra un mensaje informativo\
**Y** no presenta artículos en borrador.

## CA-05: Mostrar el detalle de un artículo publicado

**Dado** que existe un artículo publicado\
**Cuando** una persona solicita `GET /articulos/<slug>/`\
**Entonces** ve el título, la fecha, la autoría y el cuerpo del artículo\
**Y** puede volver a la portada mediante la navegación.

## CA-06: Dar formato legible al contenido del artículo

**Dado** que un artículo contiene párrafos y subtítulos\
**Cuando** una persona abre su página de detalle\
**Entonces** los párrafos se muestran separados y los subtítulos como encabezados\
**Y** cada línea que empieza por `## ` se representa como subtítulo.

## CA-07: Ocultar los artículos no publicados

**Dado** que una URL corresponde a un artículo inexistente o no publicado\
**Cuando** una persona solicita esa página\
**Entonces** el servidor devuelve `404`\
**Y** no expone el contenido del borrador.

## CA-08: Consultar y editar la presentación del autor

**Dado** que existe una presentación del autor\
**Cuando** una persona visita `GET /sobre-mi/`\
**Entonces** ve el texto de presentación configurado\
**Y** una persona autorizada puede editarlo desde Django Admin.

## CA-09: Navegar entre las páginas principales

**Dado** que una persona visita la portada, un artículo o la página «Sobre mí»\
**Cuando** utiliza la navegación del sitio\
**Entonces** encuentra enlaces claros a la portada y a «Sobre mí»\
**Y** desde un artículo puede volver a la portada.

## CA-10: Navegar sin JavaScript

**Dado** que una persona visita las páginas públicas con JavaScript desactivado\
**Cuando** utiliza los enlaces de navegación\
**Entonces** puede recorrer la portada, los artículos y «Sobre mí»\
**Y** las funciones principales de lectura siguen disponibles.

## CA-11: Gestionar el contenido desde Django Admin

**Dado** que una persona autorizada ha iniciado sesión en Django Admin\
**Cuando** gestiona el contenido editorial\
**Entonces** puede crear, editar y retirar artículos\
**Y** puede modificar la presentación del autor.

## CA-12: Restringir la gestión a personas autorizadas

**Dado** que una persona no ha iniciado sesión\
**Cuando** visita las páginas públicas o intenta acceder a Django Admin\
**Entonces** puede leer las páginas públicas, pero debe autenticarse para administrar contenido\
**Y** el sitio no ofrece registro público.

## CA-13: Adaptar las páginas a distintos tamaños de pantalla

**Dado** que una persona consulta la portada, un artículo o «Sobre mí»\
**Cuando** visualiza el sitio en una ventana de `375 × 667` o `1366 × 768` píxeles\
**Entonces** puede leer el contenido y utilizar la navegación\
**Y** las páginas no requieren desplazamiento horizontal.

## CA-14: Facilitar la lectura y navegación accesibles

**Dado** que una persona navega por cualquiera de las páginas\
**Cuando** utiliza un teclado o tecnologías de asistencia\
**Entonces** puede identificar y activar los enlaces\
**Y** el contenido utiliza HTML semántico, encabezados coherentes y nombres de enlace descriptivos.

## CA-15: Listar artículos publicados mediante la API

**Dado** que existen artículos publicados y borradores\
**Cuando** una persona solicita `GET /api/articulos/`\
**Entonces** recibe HTTP `200` y una lista JSON de artículos publicados\
**Y** cada elemento contiene `id`, `titulo`, `cuerpo` y `estado: "publicado"`\
**Y** ningún borrador aparece en la respuesta.

## CA-16: Consultar un artículo publicado mediante la API

**Dado** que existe un artículo publicado\
**Cuando** una persona solicita `GET /api/articulos/<id>/`\
**Entonces** recibe HTTP `200` y un JSON con `id`, `titulo`, `cuerpo` y `estado: "publicado"`\
**Y** un identificador inexistente o correspondiente a un borrador devuelve HTTP `404`.

## CA-17: Crear un borrador mediante la API

**Dado** que una persona administradora dispone de un token válido\
**Cuando** envía `POST /api/articulos/` con `titulo` y `cuerpo`\
**Entonces** recibe HTTP `201` con `id`, `titulo`, `cuerpo` y `estado: "borrador"`\
**Y** el artículo permanece sin publicar y no aparece en la web ni en las consultas públicas de la API.

## CA-18: Restringir la creación de borradores mediante la API

**Dado** que una solicitud `POST /api/articulos/` no incluye un token de administrador válido\
**Cuando** la API recibe la solicitud\
**Entonces** la rechaza con HTTP `401` o `403`\
**Y** no crea ningún artículo\
**Y** un token de usuario inactivo se rechaza aunque tenga `is_staff=True`.

## CA-19: Validar los datos enviados a la API

**Dado** que una solicitud de creación no incluye un título o un cuerpo válido\
**Cuando** una persona administradora la envía a `POST /api/articulos/`\
**Entonces** la API responde HTTP `400` con errores de validación\
**Y** no crea ningún artículo.
