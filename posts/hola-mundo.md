---
title: "Este blog también es código: cómo está hecho"
title_en: "This blog is code too: how it works"
date: 2026-08-23
excerpt: "Sin WordPress, sin CMS, sin base de datos: Markdown, un script de Python de 200 líneas y nginx. Así funciona este blog."
excerpt_en: "No WordPress, no CMS, no database: Markdown, a 200-line Python script and nginx. This is how this blog works."
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
 (BLOG_OUT / f"{p['slug']}.html").write_text(post_page(p, md_to_html(p["body_md"])))
```

El script genera además el `rss.xml` y los datos estructurados JSON-LD
(`BlogPosting`) para SEO. Cero dependencias externas.

*Los comentarios estarán disponibles próximamente.*

<!-- :en -->

## The idea

This site is a static build: there is no database and no admin panel.
Every article is a Markdown file in a repository, and a Python script
turns it into HTML with the same design as the rest of the site.

## Why no CMS

- **Speed**: plain HTML served by nginx. No queries, no cache to expire.
- **Security**: there is no attack surface from logins, plugins or updates.
- **Simplicity**: writing a post is `git commit` on a `.md` file.

## The pipeline

```python
posts = [parse_post(f) for f in sorted(POSTS.glob("*.md"))]
for p in posts:
 (BLOG_OUT / f"{p['slug']}.html").write_text(post_page(p, md_to_html(p["body_md"])))
```

The script also generates `rss.xml` and the JSON-LD structured data
(`BlogPosting`) for SEO. Zero external dependencies.

*Comments will be available soon.*
