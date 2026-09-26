#!/usr/bin/env python3
"""Generate og-cover.png (1200x630) for the portfolio — terminal style, no deps beyond Pillow."""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (11, 14, 20)        # #0B0E14
RAISE = (17, 21, 31)     # #11151F
BORDER = (29, 36, 51)    # #1D2433
TEXT = (230, 237, 243)   # #E6EDF3
MUTED = (139, 152, 169)  # #8B98A9
ACCENT = (74, 222, 128)  # #4ADE80
RED = (255, 95, 87)
YELLOW = (254, 188, 46)
GREEN = (40, 200, 64)

MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# subtle grid dots background
for y in range(30, H, 44):
    for x in range(30, W, 44):
        d.point((x, y), fill=(22, 27, 39))

# ── terminal window ──
tx0, ty0, tx1, ty1 = 90, 110, 1110, 460
d.rounded_rectangle([tx0, ty0, tx1, ty1], radius=16, fill=RAISE, outline=BORDER, width=2)
# bar + traffic lights
for i, c in enumerate([RED, YELLOW, GREEN]):
    cx, cy = tx0 + 34 + i * 34, ty0 + 32
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=c)
f_title = ImageFont.truetype(MONO, 22)
d.text((tx0 + 140, ty0 + 19), "jose@homelab: ~", font=f_title, fill=MUTED)
# bar separator
d.line([tx0, ty0 + 62, tx1, ty0 + 62], fill=BORDER, width=2)

f_prompt = ImageFont.truetype(MONO_B, 34)
f_body = ImageFont.truetype(MONO, 30)
f_name = ImageFont.truetype(MONO_B, 52)
f_role = ImageFont.truetype(MONO_B, 40)

y = ty0 + 96
d.text((tx0 + 36, y), "$", font=f_prompt, fill=ACCENT)
d.text((tx0 + 76, y), "whoami", font=f_body, fill=TEXT)
y += 58
d.text((tx0 + 36, y), "José Luis Sánchez Warten", font=f_name, fill=TEXT)
y += 76
d.text((tx0 + 36, y), "> python & frappe developer", font=f_role, fill=ACCENT)
y += 68
d.text((tx0 + 36, y), "$", font=f_body, fill=ACCENT)
d.rectangle([tx0 + 70, y + 4, tx0 + 98, y + 38], fill=TEXT)  # cursor block

# footer strip
f_small = ImageFont.truetype(MONO, 26)
d.text((tx0 + 36, ty1 + 28), "jlsw.dev", font=f_small, fill=ACCENT)
w_jlsw = d.textlength("jlsw.dev", font=f_small)
d.text((tx0 + 36 + w_jlsw + 24, ty1 + 28), "·  python · frappe · docker · self-hosted", font=f_small, fill=MUTED)

img.save("/opt/data/portfolio/src/og-cover.png", optimize=True)
print("og-cover.png generado")
