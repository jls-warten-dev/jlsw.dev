# jlsw.dev

Sitio personal de José Luis Sánchez Warten — **estático** (HTML + CSS + JS, sin framework).
El blog es lo único generado: Markdown en `posts/` → HTML con `tools/build_blog.py`, en Python
estándar y sin dependencias. El resto se edita a mano.

## Estructura

| ruta | qué es |
|---|---|
| `index.html` | portada |
| `app.js` | lógica del sitio: i18n (ES/EN), tema claro/oscuro, lightbox de capturas, contador de visitas |
| `styles.css` | estilos |
| `blog/` | páginas del blog y su listado (generadas) |
| `posts/` | artículos en Markdown: la fuente |
| `img/` | capturas de proyectos (`img/shots/`, en WebP) y demás imágenes |
| `og-cover.png` | imagen genérica para redes (Open Graph) |
| `og/` | card tipográfica 1200x630 de cada post (Open Graph), PNG |
| `tools/` | `build_blog.py` (Markdown → HTML + RSS) y `og_card.py` (cards OG) |
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
Los ficheros se suben tal cual. Lo único que hay que regenerar es el blog:

```bash
python3 tools/build_blog.py   # desde la raíz: escribe blog/, rss.xml y las cards de og/
```

Si una card no se puede dibujar (falta la fuente), el post sale con `og-cover.png` en vez de con una
URL rota. Tras cualquier cambio, comprobar en el navegador sobre el dominio real.

## Notas

- Las capturas de `img/shots/` están en WebP (full 1200x750 y miniatura), con su entrada de idioma en
  `app.js` para el pie del lightbox.
