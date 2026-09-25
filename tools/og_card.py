#!/usr/bin/env python3
"""Card OG tipografica (1200x630) para un post del blog de jlsw.dev.

Estilo del og-cover.png: ventana de terminal, JetBrains Mono, verde menta.
PNG y no WebP porque Facebook no renderiza WebP en og:image.

Uso:
    python3 tools/og_card.py <slug>        # regenera src/og/<slug>.png
    python3 tools/og_card.py --all

Desde build_blog.py se importa ensure_card(), que solo regenera si la card
no existe o es mas antigua que el .md fuente.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "src" / "posts"
OG_OUT = ROOT / "src" / "og"

W, H = 1200, 630
BG      = "#0B0E14"
PANEL   = "#11151F"
BAR     = "#0D1119"
BORDER  = "#1D2433"
TEXT    = "#E6EDF3"
MUTED   = "#8B98A9"
ACCENT  = "#4ADE80"
DOTGRID = "#141926"
DOTS    = ["#FF5F57", "#FEBC2E", "#28C840"]

MARGIN, BAR_H, PAD = 44, 46, 40
LADDER = (58, 52, 46, 40, 34, 30)

FONT_CANDIDATES = (
    os.path.expanduser("~/.fonts/JetBrainsMono.ttf"),
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
)


def _font_path() -> str:
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return p
    raise FileNotFoundError("ni JetBrains Mono ni DejaVu Sans Mono")


def mono(size: int, weight: str = "Bold") -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(_font_path(), size)
    if "JetBrains" in _font_path():
        try:
            names = f.get_variation_names()
            f.set_variation_by_name(weight if weight in names else names[0])
        except Exception:
            pass
    return f


def wrap(text: str, font, max_w: float, draw) -> list[str]:
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def _no_orphan(lines: list[str]) -> bool:
    """Ultima linea de una sola palabra corta: huérfano, no se acepta."""
    return len(lines) <= 1 or len(lines[-1].split()) >= 2


def fit_title(text: str, draw, max_w: float, max_h: int):
    """Mayor tamano (escalera descendente) que cabe en 4 lineas y en max_h.

    Para cada tamano se prueban anchos ligeramente menores hasta que la ultima
    linea no quede con una palabra suelta.
    """
    fallback = None
    for size in LADDER:
        f = mono(size, "Bold")
        bb = draw.textbbox((0, 0), "Ag", font=f)
        line_h = int((bb[3] - bb[1]) * 1.32)
        for k in (0, 0.025, 0.05, 0.075, 0.10, 0.13):
            lines = wrap(text, f, max_w * (1 - k), draw)
            if len(lines) > 4 or line_h * len(lines) > max_h:
                continue
            if not all(draw.textlength(l, font=f) <= max_w for l in lines):
                continue
            if _no_orphan(lines):
                return f, lines, line_h
            if fallback is None:
                fallback = (f, lines, line_h)
    if fallback:
        return fallback
    raise ValueError(f"el titulo no cabe: {text[:60]}")


def build_card(slug: str, title: str, date_fmt: str, tags: list[str]) -> Image.Image:
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    for y in range(16, H, 26):
        for x in range(16, W, 26):
            d.ellipse([x, y, x + 2, y + 2], fill=DOTGRID)

    x0, y0, x1 = MARGIN, MARGIN, W - MARGIN
    y1 = H - 132
    d.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=PANEL, outline=BORDER, width=2)
    d.rounded_rectangle([x0, y0, x1, y0 + BAR_H], radius=12, fill=BAR)
    d.rectangle([x0, y0 + BAR_H - 8, x1, y0 + BAR_H], fill=BAR)
    d.line([x0, y0 + BAR_H, x1, y0 + BAR_H], fill=BORDER, width=2)
    for i, c in enumerate(DOTS):
        cx = x0 + 26 + i * 26
        cy = y0 + BAR_H // 2
        d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=c)
    bar_txt = f"jose@jlsw:~/blog $ cat {slug}.md"
    fb = mono(17, "Regular")
    d.text(((W - d.textlength(bar_txt, font=fb)) / 2, y0 + BAR_H // 2 - 11), bar_txt, font=fb, fill=MUTED)

    inner_x = x0 + PAD
    inner_w = (x1 - PAD) - inner_x
    y = y0 + BAR_H + 34

    fp = mono(21, "Regular")
    d.text((inner_x, y), "$", font=fp, fill=ACCENT)
    d.text((inner_x + d.textlength("$ ", font=fp), y), f"cat blog/{slug}.md", font=fp, fill=MUTED)
    y += 40

    max_h = (y1 - PAD - 34) - y
    ft, lines, line_h = fit_title(title, d, inner_w, max_h)
    for l in lines:
        d.text((inner_x, y), l, font=ft, fill=TEXT)
        y += line_h

    y += 22
    d.text((inner_x, y), "$", font=fp, fill=ACCENT)
    cw = d.textlength("$ ", font=fp)
    d.rectangle([inner_x + cw, y + 3, inner_x + cw + 15, y + 27], fill=TEXT)

    fy = y1 + 40
    fl = mono(21, "Regular")
    d.text((x0, fy), date_fmt + "  ·  " + "  · ".join("#" + t for t in tags), font=fl, fill=MUTED)
    fr = mono(24, "Bold")
    d.text((x1 - d.textlength("jlsw.dev", font=fr), fy - 3), "jlsw.dev", font=fr, fill=ACCENT)
    return img


def parse_md(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    fm: dict = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip().strip('"')
    return fm


def ensure_card(slug: str, title: str, date_iso: str, tags: list[str]) -> Path:
    """Escribe src/og/<slug>.png si no existe o si es mas antiga que el .md."""
    from datetime import datetime

    md = POSTS / f"{slug}.md"
    out = OG_OUT / f"{slug}.png"
    OG_OUT.mkdir(parents=True, exist_ok=True)
    if out.exists() and md.exists() and out.stat().st_mtime >= md.stat().st_mtime:
        return out
    date_fmt = datetime.strptime(date_iso, "%Y-%m-%d").strftime("%d %b %Y")
    build_card(slug, title, date_fmt, tags).save(out, optimize=True)
    return out


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__, file=sys.stderr)
        return 2
    slugs = []
    if argv[0] == "--all":
        slugs = [p.stem for p in sorted(POSTS.glob("*.md"))]
    else:
        slugs = argv
    for slug in slugs:
        md = POSTS / f"{slug}.md"
        if not md.exists():
            print(f"no existe src/posts/{slug}.md", file=sys.stderr)
            return 1
        fm = parse_md(md)
        out = ensure_card(slug, fm.get("title", slug), fm.get("date", "1970-01-01"),
                          [t.strip() for t in fm.get("tags", "").split(",") if t.strip()])
        print(f"{out.relative_to(ROOT)}  {out.stat().st_size // 1024} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
