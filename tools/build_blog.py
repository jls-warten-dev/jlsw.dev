#!/usr/bin/env python3
"""Build blog: Markdown -> static HTML with site design + RSS.

Zero dependencies: converts the Markdown subset used in src/posts/*.md
(headings, paragraphs, bold/italic/inline-code, fenced code, lists, links).
Usage: python3 tools/build_blog.py  (from portfolio root)
"""
from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))
ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
POSTS = SRC / "posts"
BLOG_OUT = SRC / "blog"
SITE_URL = "https://jlsw.dev"

# ── Minimal front-matter + markdown ───────────────────────────
FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
# Separador entre la versión en español y la inglesa dentro de un mismo post.
EN_SPLIT_RE = re.compile(r"^\s*<!--\s*:en\s*-->\s*$", re.MULTILINE)


def parse_post(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fm = {}
    m = FM_RE.match(text)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip().strip('"')
        text = text[m.end():]
    body = text.strip()
    # Un post puede llevar su versión en inglés a continuación del español.
    # El separador es una línea con solo el marcador, que md_to_html reconoce.
    body_es, body_en = body, ""
    if EN_SPLIT_RE.search(body):
        body_es, body_en = EN_SPLIT_RE.split(body, maxsplit=1)
        body_es, body_en = body_es.strip(), body_en.strip()
    return {
        "slug": path.stem,
        "title": fm.get("title", path.stem),
        "title_en": fm.get("title_en", ""),
        "date": fm.get("date", "1970-01-01"),
        "excerpt": fm.get("excerpt", ""),
        "excerpt_en": fm.get("excerpt_en", ""),
        "tags": [t.strip() for t in fm.get("tags", "").split(",") if t.strip()],
        "body_md": body_es,
        "body_en_md": body_en,
    }


def md_to_html(md: str, ref_suffix: str = "") -> str:
    """Convert the Markdown subset used by the posts. No deps.

    Las listas numeradas (sección de referencias) se convierten en párrafos
    con ancla ``id="ref-N"`` para que las citas del cuerpo puedan enlazarlas.
    ``ref_suffix`` se añade al id en la versión en inglés (que va en su propio
    bloque, así se evitan ids duplicados en la misma página).
    """
    # fenced code blocks first (protect from inline transforms)
    code_blocks: list[str] = []

    def _code(m: re.Match) -> str:
        lang = m.group(1) or ""
        inner = html.escape(m.group(2))
        code_blocks.append(f'<pre class="code-block mono" data-lang="{lang}"><code>{inner}</code></pre>')
        return f"\x00CODE{len(code_blocks)-1}\x00"

    md = re.sub(r"```(\w*)\n(.*?)```", _code, md, flags=re.DOTALL)

    out: list[str] = []
    in_list = False
    para: list[str] = []

    def _flush_para():
        # Markdown: líneas consecutivas se unen en UN solo <p>
        if para:
            joined = " ".join(para).strip()
            # Imagen en línea propia: ![alt](src "pie opcional") → <figure>
            m_img = re.fullmatch(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)", joined)
            if m_img:
                alt, src, caption = m_img.group(1), m_img.group(2), m_img.group(3)
                fig = (f'<figure class="post-figure">'
                       f'<img src="{html.escape(src)}" alt="{html.escape(alt)}" loading="lazy" decoding="async">')
                if caption:
                    fig += f"<figcaption>{_inline(caption)}</figcaption>"
                fig += "</figure>"
                out.append(fig)
                para.clear()
                return
            out.append(f"<p>{_inline(joined)}</p>")
            para.clear()

    for raw in md.split("\n"):
        line = raw.rstrip()
        if not line:
            _flush_para()
            if in_list:
                out.append("</ul>")
                in_list = False
            continue
        if line.startswith("### "):
            _flush_para()
            if in_list:
                out.append("</ul>"); in_list = False
            out.append(f"<h3>{_inline(line[4:])}</h3>")
        elif line.startswith("## "):
            _flush_para()
            if in_list:
                out.append("</ul>"); in_list = False
            out.append(f"<h2>{_inline(line[3:])}</h2>")
        elif re.match(r"^[-*] ", line):
            _flush_para()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{_inline(line[2:])}</li>")
        elif (m_ref := re.match(r"^(\d+)\.\s+(.*)$", line)):
            # Lista numerada -> párrafo con ancla para las citas [N](#ref-N)
            _flush_para()
            if in_list:
                out.append("</ul>"); in_list = False
            num, cuerpo = m_ref.group(1), m_ref.group(2)
            out.append(f'<p class="ref-item" id="ref-{num}{ref_suffix}">'
                       f"{num}. {_inline(cuerpo)}</p>")
        else:
            if in_list:
                out.append("</ul>"); in_list = False
            para.append(line.strip())
    _flush_para()
    if in_list:
        out.append("</ul>")

    html_text = "\n".join(out)
    # restore code blocks
    for i, cb in enumerate(code_blocks):
        html_text = html_text.replace(f"\x00CODE{i}\x00", f"<p></p>{cb}")
    return html_text


def _inline(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r"<code class='inline-code'>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
    # Cita numerada a la lista de referencias: conserva los corchetes a la
    # vista ([14]) para que se lea como cita y no como un número suelto.
    s = re.sub(r"\[(\d{1,2})\]\(#(ref-[\w-]+)\)",
               r"<a href='#\2' class='ref-cite'>[\1]</a>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"<a href='\2' rel='noopener'>\1</a>", s)
    return s


# ── Page templates (mirror index.html design) ─────────────────
def og_block(url: str, alt: str | None = None) -> str:
    """Bloque og:image. Con alt => es una card propia (1200x630)."""
    if not alt:
        return f'<meta property="og:image" content="{url}">'
    return (f'<meta property="og:image" content="{url}">\n'
            '  <meta property="og:image:width" content="1200">\n'
            '  <meta property="og:image:height" content="630">\n'
            f'  <meta property="og:image:alt" content="{html.escape(alt)}">')


def og_for_post(p: dict) -> tuple:
    """Genera la card tipografica del post; si falla, cae a og-cover."""
    try:
        from og_card import ensure_card
        path = ensure_card(p["slug"], p["title"], p["date"], p["tags"])
        return f"{SITE_URL}/og/{path.name}", p["title"]
    except Exception as exc:
        print(f"aviso: card OG de {p['slug']} no generada ({exc}); se usa og-cover",
              file=sys.stderr)
        return f"{SITE_URL}/og-cover.png?v=2", None


def shell(title: str, desc: str, canonical: str, jsonld: str, content: str,
          og: str) -> str:
    return f"""<!doctype html>
<html lang="es" data-theme="dark">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <link rel="canonical" href="{canonical}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{html.escape(title)}">
  <meta property="og:description" content="{html.escape(desc)}">
  {og}
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#0B0E14">
  <link rel="alternate" type="application/rss+xml" title="RSS" href="{SITE_URL}/rss.xml">
  <!-- Umami analytics (self-hosted, cookieless) -->
  <script defer src="https://stats.jlsw.dev/script.js" data-website-id="fca495c3-3863-4756-b844-2b204f34a2fe"></script>
  <link rel="icon" href="/favicon.ico" sizes="48x48">
  <link rel="icon" href="/favicon.png" type="image/png" sizes="128x128">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <script type="application/ld+json">{jsonld}</script>
  <style>
    :root{{--bg:#0B0E14;--bg-raise:#11151F;--border:#1D2433;--text:#E6EDF3;
    --muted:#8B98A9;--accent:#4ADE80;--accent2:#7DD3FC;
    --mono:'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
    --sans:'Inter',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;}}
    html[data-theme="light"]{{--bg:#FAFBFC;--bg-raise:#FFFFFF;--border:#E3E8EF;--text:#1B2430;
    --muted:#5C6B7E;--accent:#15803D;--accent2:#0369A1;}}
    html{{background:var(--bg);color-scheme:dark}}
    html[data-theme="light"]{{color-scheme:light}}
  </style>
  <link rel="stylesheet" href="/styles.css?v=10">
</head>
<body>
  <a class="skip-link" href="#main" data-i18n="skip">Saltar al contenido</a>
  <header class="site-header">
    <nav class="nav container" data-i18n-aria="a.principal">
      <a class="brand" href="/" data-i18n-aria="a.brand">
        <img class="brand-logo brand-logo-dark" src="/img/logo-blanco.png?v=2" alt="&gt;_ joseluis - jlsw.dev" width="134" height="24">
        <img class="brand-logo brand-logo-light" src="/img/logo-negro.png?v=2" alt="" aria-hidden="true" width="134" height="24">
      </a>
      <div class="nav-links" id="nav-links">
        <a href="/#proyectos">Proyectos</a>
        <a href="/blog/">Blog</a>
        <a href="/#stack">Stack</a>
        <a href="/#certificaciones">Certificaciones</a>
        <a href="/#sobre-mi">Sobre mí</a>
        <a href="/#contacto">Contacto</a>
        <button id="lang-toggle" class="btn-ghost mono" type="button" data-i18n-aria="a.lang">EN</button>
        <button id="theme-toggle" class="btn-ghost" type="button" data-i18n-aria="a.theme">&#9684;</button>
      </div>
      <button id="nav-toggle" class="btn-ghost nav-burger" type="button" data-i18n-aria="a.menu" aria-expanded="false" aria-controls="nav-links">&#9776;</button>
    </nav>
  </header>
  <main id="main">{content}</main>
  <footer class="site-footer">
    <div class="container footer-inner mono">
      <span>&copy; 2026 Jos&eacute; Luis S&aacute;nchez Warten</span>
      <span class="footer-meta"><a href="/rss.xml">rss</a> &middot; <span data-i18n="foot.static">build est&aacute;tica</span> &middot; 0 trackers</span>
      <a class="kofi-footer" href="https://ko-fi.com/jlswarten" rel="noopener" target="_blank">&#9749; ko-fi</a>
    </div>
  </footer>
  <script src="/app.js?v=19" defer></script>
</body>
</html>
"""


def theme_bootstrap() -> str:
    """Small inline script so post pages respect stored theme before paint."""
    return ""


def post_page(p: dict, body_html: str) -> str:
    date_iso = p["date"]
    date_fmt = datetime.strptime(date_iso, "%Y-%m-%d").strftime("%d %b %Y")
    jsonld = json.dumps({
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": p["title"],
        "datePublished": date_iso,
        "author": {"@type": "Person", "name": "José Luis Sánchez Warten", "url": SITE_URL + "/"},
        "url": f"{SITE_URL}/blog/{p['slug']}.html",
    }, ensure_ascii=False)
    tags = "".join(f'<li>{html.escape(t)}</li>' for t in p["tags"])
    # Versión inglesa: título propio y bloque completo, con su ancla para enlazar
    tiene_en = bool(p.get("body_en_md"))
    toggle = ""
    bloque_en = ""
    if tiene_en:
        title_en = p.get("title_en") or p["title"]
        toggle = f"""
  <p class="mono lang-switch" role="group" data-i18n-aria="a.idioma">
    <span aria-hidden="true">$</span>
    <a href="#es" id="lang-es" class="lang-link is-active" data-lang="es">es</a>
    <a href="#en" id="lang-en" class="lang-link" data-lang="en">en</a>
  </p>"""
        bloque_en = f"""
  <div class="prose" id="en" lang="en" data-lang-block="en" hidden>
{md_to_html(p['body_en_md'], ref_suffix='-en')}
  </div>"""
    content = f"""
<section class="container section post-article">
  <p class="mono post-meta">$ cat blog/{p['slug']}.md <span class="post-date">&middot; {date_fmt}</span></p>
  <h1 class="post-title" data-lang-title="es">{html.escape(p['title'])}</h1>
  <h1 class="post-title" data-lang-title="en" lang="en" hidden>{html.escape(p.get('title_en') or p['title'])}</h1>
  <ul class="tags" data-i18n-aria="a.etiquetas">{tags}</ul>{toggle}
  <div class="prose" id="es" lang="es" data-lang-block="es">
{body_html}
  </div>{bloque_en}

  <!-- Comments hook: Waline mount point -->
  <section id="comentarios" class="comments-box card" data-i18n-aria="a.comentarios">
    <h2 class="mono section-title" style="margin-bottom:.9rem"><span aria-hidden="true">$ tail -f</span> <span data-i18n="cm.title">comentarios</span></h2>
    <div id="waline"></div>
    <p class="muted-note"><span data-i18n="cm.loading">Cargando comentarios&hellip;</span> <noscript>(se necesitan JavaScript y acceso al servidor de comentarios)</noscript></p>
  </section>
</section>
<nav class="container post-nav mono" data-i18n-aria="a.volver">
  <a href="/blog/">&larr; cd ../</a>
</nav>
"""
    return shell(p["title"], p["excerpt"], f"{SITE_URL}/blog/{p['slug']}.html", jsonld,
                 content, og_block(*og_for_post(p)))


def _bilingual(tag: str, cls: str, es: str, en: str) -> str:
    """Fila bilingüe del listado. Si el post no trae EN, el texto va sin
    atributo: así no se esconde en modo inglés (no hay versión que mostrar)."""
    attr = ' data-i18n-show="es"' if en else ""
    out = f'<{tag} class="{cls}"{attr}>{html.escape(es)}</{tag}>'
    if en:
        out += (f'\n        <{tag} class="{cls}" data-i18n-show="en" lang="en" hidden>'
                f'{html.escape(en)}</{tag}>')
    return out


def blog_index(posts: list[dict]) -> str:
    rows = []
    for i, p in enumerate(sorted(posts, key=lambda x: x["date"], reverse=True), 1):
        date_fmt = datetime.strptime(p["date"], "%Y-%m-%d").strftime("%d %b %Y")
        rows.append(f"""
    <li class="card post-row">
      <a class="post-row-link" href="/blog/{p['slug']}.html">
        <span class="mono post-meta">$ cat blog/{p['slug']}.md</span>
        {_bilingual('h2', 'post-title-sm', p['title'], p.get('title_en', ''))}
        {_bilingual('p', 'post-excerpt', p['excerpt'], p.get('excerpt_en', ''))}
        <span class="mono post-date">{date_fmt}</span>
      </a>
    </li>""")
    content = f"""
<section class="container section">
  <h1 class="section-title mono"><span aria-hidden="true">$ ls -t</span> blog/</h1>
  <ul class="post-list">{"".join(rows)}
  </ul>
</section>
"""
    return shell("Blog | José Luis Sánchez Warten", "Artículos sobre Python, Frappe, homelab y desarrollo.",
                 f"{SITE_URL}/blog/", "{}", content,
                 og_block(f"{SITE_URL}/og-cover.png?v=2"))


def rss(posts: list[dict]) -> str:
    items = []
    for p in sorted(posts, key=lambda x: x["date"], reverse=True)[:20]:
        rfc = datetime.strptime(p["date"], "%Y-%m-%d").strftime("%a, %d %b %Y 00:00:00 +0000")
        items.append(f"""    <item>
      <title>{html.escape(p['title'])}</title>
      <link>{SITE_URL}/blog/{p['slug']}.html</link>
      <guid isPermaLink="true">{SITE_URL}/blog/{p['slug']}.html</guid>
      <pubDate>{rfc}</pubDate>
      <description>{html.escape(p['excerpt'])}</description>
    </item>""")
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
  <title>jlsw.dev - blog</title>
  <link>{SITE_URL}/blog/</link>
  <description>Python, Frappe/ERPNext, homelab y desarrollo web</description>
  <language>es</language>
{chr(10).join(items)}
</channel></rss>
"""


def main() -> int:
    if not POSTS.exists():
        print("no src/posts/", file=sys.stderr)
        return 1
    BLOG_OUT.mkdir(exist_ok=True)
    posts = [parse_post(f) for f in sorted(POSTS.glob("*.md"))]
    built = []
    for p in posts:
        page = post_page(p, md_to_html(p["body_md"]))
        out = BLOG_OUT / f"{p['slug']}.html"
        out.write_text(page, encoding="utf-8")
        built.append(str(out.relative_to(ROOT)))
    (BLOG_OUT / "index.html").write_text(blog_index(posts), encoding="utf-8")
    (SRC / "rss.xml").write_text(rss(posts), encoding="utf-8")
    print(f"built {len(built)} posts:")
    for b in built:
        print("  ", b)
    print("   src/blog/index.html")
    print("   src/rss.xml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
