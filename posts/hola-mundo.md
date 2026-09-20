---
title: "Este blog también es código: cómo está hecho"
date: 2026-08-23
excerpt: "Sin WordPress, sin CMS, sin base de datos: Markdown, un script de Python de 200 líneas y nginx. Así funciona este blog."
tags: python, meta, estático
---

## La idea

Este sitio es una build estática: no hay base de datos ni panel de administración.
Cada artículo es un archivo Markdown en un repositorio, y un script de Python
lo convierte a HTML con el mismo diseño que el resto de la web.

## Por qué sin CMS

- **Velocidad**: HTML plano servido por nginx. Sin consultas, sin caché que caduca.
- **Seguridad**: no hay superficie de ataque de login, plugins ni actualizaciones.
- **Simplicidad**: escribir un post es `git commit` de un `.md`.

## El pipeline

```python
posts = [parse_post(f) for f in sorted(POSTS.glob("*.md"))]
for p in posts:
    (BLOG_OUT / f"{p['slug']}.html").write_text(
        post_page(p, md_to_html(p["body_md"]))
    )
```

El script genera además el `rss.xml` y los datos estructurados JSON-LD
(`BlogPosting`) para SEO. Cero dependencias externas.

*Los comentarios estarán disponibles próximamente.*
