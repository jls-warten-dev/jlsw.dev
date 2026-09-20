# jlsw.dev

Sitio personal de José Luis Sánchez Warten — **estático** (HTML + CSS + JS, sin framework ni build).

## Estructura

| ruta | qué es |
|---|---|
| `index.html` | portada |
| `app.js` | lógica del sitio: i18n (ES/EN), tema claro/oscuro, lightbox de capturas, contador de visitas |
| `styles.css` | estilos |
| `blog/` | listado del blog |
| `posts/` | artículos publicados |
| `img/` | capturas de proyectos (`img/shots/`, en WebP) y demás imágenes |
| `og-cover.png` | imagen para redes (Open Graph) |
| `CV_*.pdf` | currículum |
| `rss.xml`, `sitemap.xml`, `robots.txt` | SEO y sindicación |
| `404.html` | página de error |

## Comentarios

Los comentarios del blog los sirve **Waline** (autohospedado), apuntado desde `app.js`:

```js
serverURL: 'https://jlsw.dev/waline'
```

La infraestructura de Waline (contenedor, base SQLite y proxy en nginx) **no vive en este
repositorio**: es servicio del servidor, no código del sitio.

## Despliegue

El sitio se sirve como estático desde `/var/www/jlsw` en el servidor de producción, detrás de nginx.
Los ficheros se suben tal cual: **no hay paso de compilación**. Tras cualquier cambio, comprobar en el
navegador sobre el dominio real.

## Notas

- Las capturas de `img/shots/` están en WebP (full 1200x750 y miniatura), con su entrada de idioma en
  `app.js` para el pie del lightbox.
