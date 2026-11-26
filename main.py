#!/usr/bin/env python3
"""Draw a newspaper front page summing up the world news of Friday
27 November 2026 and write it to /output/entry.png.

Pure stdlib + Pillow, no network, fully deterministic: fixed layout,
fixed palette, no randomness, no timestamps.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

PAPER = (247, 242, 231)
INK = (25, 25, 25)
NAVY = (22, 35, 60)
NAVY_LIGHT = (42, 60, 92)
RED = (169, 35, 24)
GOLD = (201, 162, 39)
SLATE = (58, 74, 99)
GREY = (110, 110, 104)
LIGHT_GREY = (228, 224, 212)

_HERE = os.path.dirname(os.path.abspath(__file__))


def load_font(name, size):
    """Load a bundled subset font, falling back to system DejaVu."""
    for path in (
        os.path.join(_HERE, "fonts", name),
        os.path.join("/usr/share/fonts/truetype/dejavu", name),
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


SERIF_B = lambda s: load_font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: load_font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: load_font("DejaVuSans.ttf", s)


def wrap(draw, text, font, max_width):
    """Wrap text into lines that fit max_width pixels."""
    lines, line = [], ""
    for word in text.split(" "):
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_text_block(draw, x, y, text, font, color, max_width, leading):
    """Draw wrapped text; return the y just below the last line."""
    for line in wrap(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=color)
        y += leading
    return y


def tag(draw, x, y, label, color=RED):
    draw.text((x, y), label, font=SANS_B(19), fill=color)
    return y + 26


# ------------------------------------------------------------------ art

def draw_storm(draw, x0, y0, w, h):
    """Thanksgiving storm over a city skyline: dark sky, clouds, rain,
    lit windows, one lightning bolt."""
    # sky: vertical bands getting darker toward the top
    bands = 24
    for i in range(bands):
        t = i / (bands - 1)
        col = tuple(
            int(NAVY_LIGHT[c] + (NAVY[c] - NAVY_LIGHT[c]) * t) for c in range(3)
        )
        draw.rectangle([x0, y0 + i * h // bands, x0 + w, y0 + (i + 1) * h // bands], fill=col)
    # storm clouds
    cloud = (52, 62, 84)
    for cx, cy, rx, ry in (
        (0.22, 0.20, 0.20, 0.075),
        (0.55, 0.13, 0.24, 0.09),
        (0.85, 0.22, 0.20, 0.075),
        (0.40, 0.26, 0.18, 0.06),
    ):
        draw.ellipse(
            [x0 + (cx - rx) * w, y0 + (cy - ry) * h,
             x0 + (cx + rx) * w, y0 + (cy + ry) * h],
            fill=cloud,
        )
    # lightning bolt
    bolt = [
        (0.68, 0.18), (0.60, 0.42), (0.66, 0.42),
        (0.56, 0.68), (0.66, 0.40), (0.60, 0.40),
    ]
    draw.polygon(
        [(x0 + bx * w, y0 + by * h) for bx, by in bolt], fill=(247, 214, 74)
    )
    # rain: fixed diagonal strokes
    for i in range(46):
        rx = x0 + (i * 97 % 100) / 100.0 * w
        ry = y0 + (i * 53 % 100) / 100.0 * h * 0.62 + h * 0.30
        draw.line([rx, ry, rx - 7, ry + 16], fill=(150, 170, 205), width=2)
    # skyline silhouettes with lit windows
    base = y0 + h
    buildings = [
        (0.00, 0.52, 0.13, 0.30), (0.13, 0.62, 0.11, 0.20),
        (0.24, 0.48, 0.12, 0.34), (0.36, 0.58, 0.10, 0.24),
        (0.46, 0.44, 0.13, 0.38), (0.59, 0.60, 0.11, 0.22),
        (0.70, 0.50, 0.12, 0.32), (0.82, 0.64, 0.09, 0.18),
        (0.91, 0.56, 0.09, 0.26),
    ]
    for bx, by, bw, bh in buildings:
        draw.rectangle(
            [x0 + bx * w, y0 + by * h, x0 + (bx + bw) * w, base], fill=(16, 22, 36)
        )
        # a few lit windows, fixed pattern
        for wx in range(2):
            for wy in range(3):
                if (int(bx * 100) + wx * 3 + wy) % 3 == 0:
                    draw.rectangle(
                        [x0 + (bx + 0.02 + wx * 0.045) * w,
                         y0 + (by + 0.03 + wy * 0.09) * h,
                         x0 + (bx + 0.045 + wx * 0.045) * w,
                         y0 + (by + 0.07 + wy * 0.09) * h],
                        fill=(247, 214, 74),
                    )
    # ground line
    draw.rectangle([x0, base - 4, x0 + w, base], fill=(16, 22, 36))


def draw_pylon(draw, x0, y0, w, h):
    """Power pylon against a dusk sky."""
    for i in range(12):
        t = i / 11
        shade = int(78 - 46 * t)
        draw.rectangle([x0, y0 + i * h // 12, x0 + w, y0 + (i + 1) * h // 12],
                       fill=(shade, shade + 8, shade + 24))
    # horizon glow
    draw.rectangle([x0, y0 + h * 0.78, x0 + w, y0 + h], fill=(96, 84, 96))
    # pylon: wide legs, two crossarms, sagging wires
    cx = x0 + w * 0.30
    top = y0 + h * 0.06
    bot = y0 + h
    draw.polygon([(cx - 5, top), (cx + 5, top), (cx + 30, bot), (cx + 14, bot)], fill=INK)
    draw.polygon([(cx - 5, top), (cx + 5, top), (cx - 14, bot), (cx - 30, bot)], fill=INK)
    for ay in (0.16, 0.32):
        y = y0 + h * ay
        draw.rectangle([cx - w * 0.32, y - 3, cx + w * 0.32, y + 3], fill=INK)
        # insulator dots at the arm ends
        draw.ellipse([cx - w * 0.32 - 3, y - 2, cx - w * 0.32 + 3, y + 8], fill=INK)
        draw.ellipse([cx + w * 0.32 - 3, y - 2, cx + w * 0.32 + 3, y + 8], fill=INK)
    # wires sagging from the arm ends toward the frame edges
    for ay in (0.16, 0.32):
        y = y0 + h * ay
        draw.line([x0, y + 10, cx - w * 0.32, y + 4], fill=INK, width=2)
        draw.line([cx + w * 0.32, y + 4, x0 + w, y + 10], fill=INK, width=2)
    # distant second pylon, smaller
    cx2 = x0 + w * 0.82
    draw.polygon([(cx2 - 3, y0 + h * 0.34), (cx2 + 3, y0 + h * 0.34),
                  (cx2 + 12, bot), (cx2 + 5, bot)], fill=(40, 40, 44))
    draw.polygon([(cx2 - 3, y0 + h * 0.34), (cx2 + 3, y0 + h * 0.34),
                  (cx2 - 5, bot), (cx2 - 12, bot)], fill=(40, 40, 44))
    draw.rectangle([cx2 - w * 0.10, y0 + h * 0.40, cx2 + w * 0.10, y0 + h * 0.40 + 3],
                   fill=(40, 40, 44))


def draw_refinery(draw, x0, y0, w, h):
    """Refinery towers with smoke and flame under a night sky."""
    draw.rectangle([x0, y0, x0 + w, y0 + h], fill=(38, 34, 40))
    # orange glow near the ground
    for i in range(10):
        t = i / 9
        col = (200 - int(90 * t), 90 - int(40 * t), 30)
        draw.rectangle([x0, y0 + h - (i + 1) * h // 22, x0 + w, y0 + h - i * h // 22], fill=col)
    # smoke puffs, kept high and small so the flame reads clearly
    smoke = (120, 116, 118)
    for sx, sy, sr in ((0.55, 0.12, 0.08), (0.72, 0.08, 0.09), (0.88, 0.14, 0.07)):
        draw.ellipse([x0 + (sx - sr) * w, y0 + (sy - sr) * h,
                      x0 + (sx + sr) * w, y0 + (sy + sr) * h], fill=smoke)
    # towers
    for tx, tw, th in ((0.10, 0.10, 0.62), (0.26, 0.13, 0.78), (0.46, 0.10, 0.55), (0.62, 0.14, 0.70)):
        draw.rectangle([x0 + tx * w, y0 + h * (1 - th), x0 + (tx + tw) * w, y0 + h], fill=(20, 18, 22))
        draw.rectangle([x0 + tx * w, y0 + h * (1 - th) - 6, x0 + (tx + tw) * w, y0 + h * (1 - th)], fill=(60, 56, 60))
    # flame rising from the top of the tallest tower (centre 0.325w,
    # tower top at 0.22h) so its base sits on the tower, not in the sky
    fx = x0 + w * 0.325
    fy = y0 + h * 0.24
    draw.polygon([(fx - 13, fy + 16), (fx, fy - 12), (fx + 13, fy + 16)], fill=(247, 160, 40))
    draw.polygon([(fx - 6, fy + 16), (fx, fy + 2), (fx + 6, fy + 16)], fill=(247, 214, 74))


def draw_tanker(draw, x0, y0, w, h):
    """Fuel tanker on a desert road at dusk, flame above it."""
    draw.rectangle([x0, y0, x0 + w, y0 + h * 0.62], fill=(214, 158, 92))
    draw.ellipse([x0 + w * 0.78, y0 + h * 0.10, x0 + w * 0.92, y0 + h * 0.34], fill=(240, 190, 110))
    draw.rectangle([x0, y0 + h * 0.62, x0 + w, y0 + h], fill=(168, 128, 84))
    # road
    draw.rectangle([x0, y0 + h * 0.80, x0 + w, y0 + h], fill=(60, 56, 52))
    # tanker truck: tank bottom meets the wheels, wheels sit on the road
    ty = y0 + h * 0.50
    draw.rounded_rectangle([int(x0 + w * 0.08), int(ty), int(x0 + w * 0.60),
                            int(ty + h * 0.28)], radius=10, fill=(205, 205, 202))
    draw.rectangle([x0 + w * 0.08, ty + h * 0.10, x0 + w * 0.60, ty + h * 0.14], fill=(170, 170, 166))
    draw.polygon([(x0 + w * 0.60, ty + h * 0.04), (x0 + w * 0.70, ty + h * 0.04),
                  (x0 + w * 0.75, ty + h * 0.28), (x0 + w * 0.60, ty + h * 0.28)], fill=(170, 40, 30))
    for wx in (0.14, 0.30, 0.46):
        draw.ellipse([x0 + w * wx, ty + h * 0.26, x0 + w * (wx + 0.055), ty + h * 0.38], fill=INK)
    draw.ellipse([x0 + w * 0.66, ty + h * 0.26, x0 + w * 0.715, ty + h * 0.38], fill=INK)
    # flame above the tank
    fx = x0 + w * 0.34
    fy = ty - h * 0.08
    draw.polygon([(fx - 15, fy + 12), (fx, fy - 18), (fx + 15, fy + 12)], fill=(247, 160, 40))
    draw.polygon([(fx - 7, fy + 12), (fx, fy - 2), (fx + 7, fy + 12)], fill=(247, 214, 74))


def draw_ship(draw, x0, y0, w, h):
    """Container ship on the sea under a pale sky."""
    draw.rectangle([x0, y0, x0 + w, y0 + h * 0.55], fill=(196, 214, 228))
    draw.rectangle([x0, y0 + h * 0.55, x0 + w, y0 + h], fill=(44, 84, 120))
    # wave lines
    for wy in (0.62, 0.72, 0.84):
        draw.line([x0, y0 + h * wy, x0 + w, y0 + h * wy], fill=(120, 160, 190), width=2)
    # hull
    draw.polygon([(x0 + w * 0.06, y0 + h * 0.62), (x0 + w * 0.94, y0 + h * 0.62),
                  (x0 + w * 0.86, y0 + h * 0.82), (x0 + w * 0.14, y0 + h * 0.82)],
                 fill=(30, 44, 66))
    # stacked containers
    cols = [(200, 70, 50), (40, 110, 160), (220, 160, 40), (60, 140, 90)]
    for i, col in enumerate(cols):
        cx = x0 + w * (0.14 + i * 0.19)
        draw.rectangle([cx, y0 + h * 0.40, cx + w * 0.16, y0 + h * 0.62], fill=col)
        draw.rectangle([cx, y0 + h * 0.40, cx + w * 0.16, y0 + h * 0.44], fill=(255, 255, 255))
    # bridge tower
    draw.rectangle([x0 + w * 0.86, y0 + h * 0.34, x0 + w * 0.93, y0 + h * 0.62], fill=(240, 240, 236))


# ------------------------------------------------------------------ page

def story_block(draw, x, y, w, art, region, headline, body):
    """One grid story: illustration strip, region tag, headline, body.
    Block is 212 px tall: art 76, tag 24, headline up to 2 lines,
    body exactly 2 lines."""
    art(draw, x, y, w, 76)
    y += 84
    y = tag(draw, x, y, region)
    y = draw_text_block(draw, x, y, headline, SERIF_B(25), INK, w, 29)
    y += 3
    draw_text_block(draw, x, y, body, SANS(18), (60, 60, 56), w, 21)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 100], fill=NAVY)
    d.text((W // 2, 50), "THE WORLD TODAY", font=SERIF_B(60),
           fill=(250, 246, 236), anchor="mm")
    d.rectangle([0, 100, W, 104], fill=GOLD)

    # ---- date bar
    d.text((W // 2, 126), "FRIDAY  27  NOVEMBER  2026", font=SANS_B(32),
           fill=RED, anchor="mm")
    d.line([24, 152, W - 24, 152], fill=INK, width=2)

    # ---- lead story: Thanksgiving storm
    draw_storm(d, 24, 164, 472, 316)
    lx = 520
    y = 170
    y = tag(d, lx, y, "AMERICAS")
    y = draw_text_block(d, lx, y, "Thanksgiving storm slams the US Northeast",
                        SERIF_B(40), INK, 480, 48)
    y += 8
    draw_text_block(
        d, lx, y,
        "New York postpones the 100th Macy's parade for the first time. "
        "Over half a million homes lose power and hundreds of flights are "
        "cancelled as about 80 million people travel.",
        SANS(22), (60, 60, 56), 480, 28)
    d.line([24, 492, W - 24, 492], fill=INK, width=2)

    # ---- row 1
    story_block(d, 24, 506, 476, draw_pylon, "EUROPE",
                "Zelenskyy warns of new strikes on power grid",
                "EU split over a \u20ac45bn loan for Ukraine. "
                "North Korea halts missile deliveries to Russia.")
    story_block(d, 524, 506, 476, draw_refinery, "ASIA",
                "Fire engulfs Bangkok oil refinery",
                "Blast at the Bangchak refinery injures 9, three critically. "
                "All units shut down.")
    d.line([24, 726, W - 24, 726], fill=(190, 186, 172), width=1)

    # ---- row 2
    story_block(d, 24, 738, 476, draw_tanker, "MIDDLE EAST",
                "Two Italians killed in drone attack in Kuwait",
                "Iranian drone strike kills two technicians. A tanker fire "
                "near Cairo claims at least 31 lives.")
    story_block(d, 524, 738, 476, draw_ship, "TRADE",
                "Vietnam races to finish US trade deal",
                "Tariffs of up to 35% threaten clothing and footwear exports; "
                "China says it may respond.")
    d.line([24, 962, W - 24, 962], fill=INK, width=2)

    # ---- footer: New Zealand + sport
    d.text((24, 972),
           "ALSO TODAY  \u2014  NEW ZEALAND: Final election count due; centre-right "
           "coalition holds 67 of 131 seats.",
           font=SANS_B(15), fill=INK)
    d.text((24, 994),
           "SPORT: Steelers release quarterback Aaron Rodgers; Jannik Sinner out "
           "of the Australian Open with a knee injury.",
           font=SANS(14), fill=(60, 60, 56))

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img.save(os.path.join(out_dir, "entry.png"), format="PNG")


if __name__ == "__main__":
    main()
