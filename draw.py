#!/usr/bin/env python3
"""Draw the entry image for make.fun news-image-20261118.

A 1024x1024 newspaper front page summing up Wednesday 18 November 2026
in six stories. Drawn only with Pillow primitives and DejaVu fonts:
no network, no randomness, no timestamps, so the output is deterministic.
Run:  python3 draw.py  (writes entry.png next to itself)
"""

from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W = H = 1024
PAPER = (250, 246, 235)
HEADER = (22, 35, 63)
GOLD = (198, 148, 66)
INK = (24, 33, 48)
MUTED = (82, 92, 108)
RULE = (178, 168, 148)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def fnt(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def icon_summit(d, cx, cy, col):
    # three heads over shoulders, a small flag between the outer two
    for dx in (-38, 0, 38):
        d.ellipse([cx + dx - 11, cy - 34, cx + dx + 11, cy - 12], fill=col)
        d.pieslice([cx + dx - 20, cy - 8, cx + dx + 20, cy + 34], 180, 360, fill=col)
    d.line([(cx, cy - 44), (cx, cy - 8)], fill=col, width=4)
    d.polygon([(cx, cy - 44), (cx + 22, cy - 36), (cx, cy - 28)], fill=col)


def icon_voyager(d, cx, cy, col):
    # orbit arc, a small probe, and a signal dot on the arc
    d.arc([cx - 48, cy - 48, cx + 48, cy + 48], 210, 30, fill=col, width=5)
    d.ellipse([cx + 34, cy - 42, cx + 46, cy - 30], fill=col)
    d.polygon([(cx - 28, cy - 6), (cx + 6, cy - 22), (cx + 18, cy + 2),
               (cx - 8, cy + 18)], fill=col)
    d.line([(cx + 6, cy - 22), (cx + 30, cy - 38)], fill=col, width=4)
    d.ellipse([cx - 46, cy + 24, cx - 30, cy + 40], fill=col)


def icon_tanker(d, cx, cy, col):
    # tanker hull, containers, a strike flash, waves below
    d.polygon([(cx - 46, cy - 4), (cx + 46, cy - 4), (cx + 36, cy + 22),
               (cx - 36, cy + 22)], fill=col)
    d.rectangle([cx - 30, cy - 26, cx - 6, cy - 4], fill=col)
    d.rectangle([cx + 2, cy - 26, cx + 26, cy - 4], fill=col)
    d.polygon([(cx + 8, cy - 52), (cx + 16, cy - 34), (cx + 24, cy - 34),
               (cx + 14, cy - 18), (cx + 22, cy - 18), (cx + 8, cy + 2)],
              fill=col)
    for i, y in enumerate((cy + 32, cy + 44)):
        d.arc([cx - 46 + i * 10, y, cx - 16 + i * 10, y + 10], 0, 180,
              fill=col, width=4)
        d.arc([cx + 6 + i * 10, y, cx + 36 + i * 10, y + 10], 0, 180,
              fill=col, width=4)


def icon_turbine(d, cx, cy, col):
    # wind turbine with three blades, plus a small sun
    d.ellipse([cx + 26, cy - 52, cx + 46, cy - 32], fill=col)
    d.polygon([(cx - 4, cy - 10), (cx + 4, cy - 10), (cx + 10, cy + 44),
               (cx - 10, cy + 44)], fill=col)
    for angle in (0, 120, 240):
        # three blades drawn as rotated lines from the hub
        import math
        a = math.radians(angle - 90)
        ex, ey = cx + 34 * math.cos(a), cy - 18 + 34 * math.sin(a)
        d.line([(cx, cy - 18), (ex, ey)], fill=col, width=7)
    d.ellipse([cx - 7, cy - 25, cx + 7, cy - 11], fill=col)


def icon_border(d, cx, cy, col):
    # a dashed border line with arrows facing each other
    for i in range(5):
        y = cy - 44 + i * 20
        d.line([(cx, y), (cx, y + 10)], fill=col, width=5)
    d.line([(cx - 44, cy - 18), (cx - 14, cy - 18)], fill=col, width=6)
    d.polygon([(cx - 14, cy - 18), (cx - 28, cy - 28), (cx - 28, cy - 8)],
              fill=col)
    d.line([(cx + 44, cy + 18), (cx + 14, cy + 18)], fill=col, width=6)
    d.polygon([(cx + 14, cy + 18), (cx + 28, cy + 8), (cx + 28, cy + 28)],
              fill=col)


def icon_quake(d, cx, cy, col):
    # concentric rings with a seismograph trace across them
    for r in (46, 32, 18):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col, width=4)
    pts = [(cx - 44, cy), (cx - 28, cy), (cx - 18, cy - 22),
           (cx - 6, cy + 20), (cx + 6, cy - 26), (cx + 18, cy + 14),
           (cx + 28, cy), (cx + 44, cy)]
    d.line(pts, fill=col, width=5, joint="curve")


CARDS = [
    ("01  /  SHENZHEN  \u00b7  APEC",
     "Xi welcomes Trump to Shenzhen",
     "Trilateral talks with Putin due Thu",
     (16, 92, 80), (233, 242, 234), icon_summit),
    ("02  /  SPACE  \u00b7  NASA",
     "Voyager 1 reaches one light-day",
     "A signal now takes 24 hours",
     (31, 58, 110), (229, 236, 245), icon_voyager),
    ("03  /  GULF  \u00b7  SHIPPING",
     "Ship struck in the Strait of Hormuz",
     "ADNOC: 1 crew missing, 11 hurt",
     (164, 66, 38), (247, 234, 224), icon_tanker),
    ("04  /  EUROPE  \u00b7  ENERGY",
     "EU agrees faster green permits",
     "Provisional deal covers grids too",
     (28, 102, 74), (229, 241, 232), icon_turbine),
    ("05  /  HORN OF AFRICA",
     "Ethiopia, Eritrea build up at border",
     "Reuters: troops massing, war fears",
     (122, 54, 96), (242, 231, 240), icon_border),
    ("06  /  PERU  \u00b7  EARTHQUAKE",
     "Magnitude 6.0 quake off Peru",
     "96 km west of Marcona, Ica",
     (146, 100, 24), (247, 238, 216), icon_quake),
]


def draw_header(d):
    d.rectangle([0, 0, W, 200], fill=HEADER)
    # globe: concentric circles and meridians, top right
    gx, gy = 892, 100
    for r in (96, 70, 44):
        d.ellipse([gx - r, gy - r, gx + r, gy + r],
                  outline=(94, 122, 160), width=2)
    d.line([(gx, gy - 96), (gx, gy + 96)], fill=(94, 122, 160), width=2)
    d.line([(gx - 96, gy), (gx + 96, gy)], fill=(94, 122, 160), width=2)
    for px, py in ((812, 48), (852, 158), (946, 44), (972, 132)):
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=GOLD)
    d.text((40, 30), "THE WORLD IN SIX",
           font=fnt(SANS_BOLD, 26), fill=GOLD)
    d.line([(40, 66), (340, 66)], fill=GOLD, width=3)
    d.text((38, 76), "Wednesday", font=fnt(SERIF_REG, 54), fill=PAPER)
    d.text((38, 128), "18 November 2026", font=fnt(SERIF, 68), fill=PAPER)
    d.rectangle([0, 200, W, 206], fill=GOLD)


def draw_card(d, x, y, w, h, card):
    kicker, headline, sub, accent, bg, painter = card
    d.rectangle([x, y, x + w, y + h], fill=bg)
    d.rectangle([x, y, x + 6, y + h], fill=accent)
    d.text((x + 24, y + 18), kicker, font=fnt(SANS_BOLD, 20), fill=accent)
    icx, icy = x + w - 78, y + 106
    d.ellipse([icx - 54, icy - 54, icx + 54, icy + 54],
              fill=(255, 255, 255, 96))
    painter(d, icx, icy, accent)
    head = fnt(SANS_BOLD, 36)
    lines = wrap(d, headline, head, w - 168)
    ly = y + 52
    for line in lines:
        d.text((x + 24, ly), line, font=head, fill=INK)
        ly += 43
    d.text((x + 24, y + h - 38), sub, font=fnt(SANS, 24), fill=MUTED)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d)
    margin, gap = 36, 16
    cw = (W - 2 * margin - gap) // 2
    ch = 232
    y0 = 224
    for i, card in enumerate(CARDS):
        x = margin + (i % 2) * (cw + gap)
        y = y0 + (i // 2) * (ch + gap)
        draw_card(d, x, y, cw, ch, card)
    d.line([(margin, 968), (W - margin, 968)], fill=RULE, width=2)
    d.text((margin, 980), "REPORTING",
           font=fnt(SANS_BOLD, 21), fill=(164, 66, 38))
    d.text((margin + 148, 980),
           "DW  \u00b7  NASA  \u00b7  ADNOC  \u00b7  EU Council  \u00b7  "
           "Reuters  \u00b7  Peru IGP",
           font=fnt(SANS, 20), fill=MUTED)
    img.save(OUT, "PNG", optimize=True)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    main()
