#!/usr/bin/env python3
"""VELMARIS — travel poster for a place that isn't there.

Draws the poster with Pillow (local build tool only) and writes entry.png
(1024x1024) next to this file. The shipped entrypoint main.py is stdlib-only
and merely copies entry.png to the grader's output directory.

Concept: VELMARIS, the town where the sea hangs above the rooftops.
One impossible landmark — a band of sea floating in the dusk sky, a thin
waterfall spilling from it down to the town, a sailboat crossing the sky-sea.
Golden-hour light, one hero image, the place's name as the only text.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont, ImageFilter

W = H = 1024
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

# --- palette: 4 colours + tints -------------------------------------------
INDIGO = (26, 32, 66)        # deep dusk top / town silhouette
VIOLET = (122, 90, 158)      # mid sky
AMBER = (242, 166, 90)       # golden hour
CREAM = (247, 232, 201)      # the name, windows
TEAL = (30, 110, 120)        # the sky-sea
TEAL_DARK = (18, 74, 88)
TEAL_LIGHT = (92, 178, 186)
SUN = (255, 196, 110)
SUN_CORE = (255, 224, 160)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sky_gradient(img):
    """Vertical dusk gradient: indigo -> violet -> amber at the horizon."""
    stops = [(0.00, (22, 26, 58)),
             (0.34, (58, 48, 96)),
             (0.58, (122, 90, 158)),
             (0.78, (214, 138, 96)),
             (1.00, (247, 178, 104))]
    px = img.load()
    for y in range(H):
        t = y / (H - 1)
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= t <= t1:
                f = 0 if t1 == t0 else (t - t0) / (t1 - t0)
                col = lerp(c0, c1, f)
                break
        else:
            col = stops[-1][1]
        for x in range(W):
            px[x, y] = col


def draw_sun(base):
    """Low golden sun at the right, half sunk behind the horizon haze."""
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    cx, cy, r = 770, 640, 118
    for i in range(14, 0, -1):
        rr = r + i * 16
        a = int(10 + (14 - i) * 4)
        gd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                   fill=SUN + (a,))
    glow = glow.filter(ImageFilter.GaussianBlur(18))
    base.alpha_composite(glow)
    d = ImageDraw.Draw(base)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SUN + (255,))
    d.ellipse([cx - r + 26, cy - r + 26, cx + r - 26, cy + r - 26],
              fill=SUN_CORE + (255,))


def draw_clouds(d):
    """A few soft flat clouds, pale violet, high in the sky."""
    clouds = [(120, 300, 210, 34), (700, 210, 260, 30), (520, 272, 150, 22),
              (880, 330, 150, 24), (60, 470, 150, 22)]
    for x, y, w, h in clouds:
        d.ellipse([x, y, x + w, y + h], fill=(196, 164, 210, 70))
        d.ellipse([x + w * 0.18, y - h * 0.45, x + w * 0.82, y + h * 0.55],
                  fill=(196, 164, 210, 70))


def draw_birds(d):
    for x, y, s in [(180, 210, 16), (250, 180, 12), (880, 150, 14),
                    (640, 250, 11), (330, 260, 10)]:
        d.arc([x - s, y - s // 2, x, y + s // 2], 200, 340,
              fill=(30, 30, 60, 220), width=3)
        d.arc([x, y - s // 2, x + s, y + s // 2], 200, 340,
              fill=(30, 30, 60, 220), width=3)


def draw_sky_sea(d, base):
    """THE landmark: a band of sea floating in the sky above the town.

    Wavy top and bottom edges, a bright sunlit top rim, dark keel below,
    a sailboat crossing it, and one thin waterfall spilling down to town.
    """
    top, bot = 350, 452
    xs = list(range(40, 985, 8))
    top_edge = [(x, top + int(7 * math.sin(x / 61.0))) for x in xs]
    bot_edge = [(x, bot + int(9 * math.sin(x / 47.0 + 1.3))) for x in xs]
    poly = top_edge + list(reversed(bot_edge))
    # vertical gradient inside the band: sunlit top -> deep keel
    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gpx = grad.load()
    for y in range(top - 8, bot + 12):
        t = (y - (top - 8)) / ((bot + 12) - (top - 8))
        col = lerp((74, 158, 168), TEAL_DARK, t)
        for x in range(40, 985):
            gpx[x, y] = col + (255,)
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).polygon(poly, fill=255)
    base.paste(grad, (0, 0), mask)
    d = ImageDraw.Draw(base)
    # sunlit rim along the top edge
    for (x0, y0), (x1, y1) in zip(top_edge, top_edge[1:]):
        d.line([x0, y0, x1, y1], fill=TEAL_LIGHT + (255,), width=5)
    # dark keel shadow under the bottom edge
    for (x0, y0), (x1, y1) in zip(bot_edge, bot_edge[1:]):
        d.line([x0, y0 + 4, x1, y1 + 4], fill=TEAL_DARK + (255,), width=6)
    # wave dashes on the water
    for x in range(90, 940, 70):
        y = top + 34 + int(6 * math.sin(x / 40.0))
        d.line([x, y, x + 34, y], fill=(210, 235, 230, 200), width=4)
    for x in range(130, 920, 90):
        y = top + 62 + int(6 * math.sin(x / 33.0 + 2.0))
        d.line([x, y, x + 26, y], fill=(170, 215, 215, 160), width=3)
    # sailboat crossing the sky-sea
    bx, by = 620, top + 8
    d.polygon([(bx, by - 46), (bx, by - 2), (bx + 34, by - 2)],
              fill=CREAM + (255,))
    d.polygon([(bx - 4, by - 38), (bx - 4, by - 2), (bx - 30, by - 2)],
              fill=(226, 205, 168, 255))
    d.polygon([(bx - 42, by), (bx + 46, by), (bx + 34, by + 14),
               (bx - 30, by + 14)], fill=(24, 30, 62, 255))
    d.line([bx, by - 50, bx, by - 2], fill=(24, 30, 62, 255), width=3)
    # the waterfall: one thin ribbon spilling from the sea to the town
    fall_x = 300
    pts = []
    for i in range(41):
        t = i / 40
        x = fall_x + int(26 * math.sin(t * 2.4))
        y = bot + 6 + int(t * (742 - bot))
        pts.append((x, y))
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        d.line([x0, y0, x1, y1], fill=(226, 240, 238, 210), width=7)
        d.line([x0 - 5, y0, x1 - 5, y1], fill=(170, 215, 215, 130), width=3)
    # foam where the fall lands
    d.ellipse([fall_x - 26, 736, fall_x + 34, 756],
              fill=(226, 240, 238, 190))


def draw_town(d):
    """Rooftop silhouette along the bottom, warm windows, one spire."""
    # ground / shore band
    d.rectangle([0, 800, W, H], fill=(20, 24, 52, 255))
    # rooftops: a run of gabled houses
    houses = [
        (0, 812, 120, 742), (96, 812, 210, 726), (190, 812, 300, 752),
        (282, 812, 400, 718), (380, 812, 500, 748), (480, 812, 596, 724),
        (576, 812, 700, 754), (680, 812, 800, 720), (780, 812, 900, 748),
        (880, 812, 1024, 730),
    ]
    for x0, base, x1, peak in houses:
        mid = (x0 + x1) // 2
        d.polygon([(x0, base), (x0, peak + 34), (mid, peak),
                   (x1, peak + 34), (x1, base)], fill=(20, 24, 52, 255))
    # chimneys
    for x, y, h in [(150, 726, 34), (340, 718, 30), (540, 724, 36),
                    (740, 720, 30), (950, 730, 32)]:
        d.rectangle([x, y - h, x + 14, y + 8], fill=(20, 24, 52, 255))
    # church spire, left of centre
    d.rectangle([428, 660, 448, 742], fill=(20, 24, 52, 255))
    d.polygon([(420, 664), (438, 606), (456, 664)], fill=(20, 24, 52, 255))
    d.ellipse([434, 596, 442, 604], fill=AMBER + (255,))
    # warm lit windows: varied, not a grid — some dark, some paired
    for x in range(36, 1000, 46):
        for y in (766, 796, 826):
            h = (x * 2654435761 + y * 40503) % 11
            if h < 4:
                d.rectangle([x, y, x + 12, y + 16], fill=AMBER + (235,))
            elif h == 4:
                d.rectangle([x, y, x + 26, y + 16], fill=AMBER + (200,))
    # a few windows in the spire
    d.rectangle([433, 690, 443, 712], fill=AMBER + (235,))
    # low foreground ridge with two lamp posts — depth, no clutter
    d.polygon([(0, 1024), (0, 946), (180, 930), (420, 948), (640, 928),
               (860, 950), (1024, 936), (1024, 1024)],
              fill=(14, 17, 40, 255))
    for lx, ly in [(200, 948), (820, 954)]:
        d.line([lx, ly, lx, ly - 34], fill=(96, 102, 156, 255), width=5)
        d.ellipse([lx - 13, ly - 46, lx + 13, ly - 24],
                  fill=AMBER + (70,))
        d.ellipse([lx - 6, ly - 42, lx + 6, ly - 30], fill=AMBER + (255,))


def draw_name(d):
    """VELMARIS — the only text. Big, cream, letter-spaced, top third."""
    name = "VELMARIS"
    size = 118
    font = ImageFont.truetype(FONT_BOLD, size)
    widths = [d.textlength(ch, font=font) for ch in name]
    gap = 26
    total = sum(widths) + gap * (len(name) - 1)
    x = (W - total) // 2
    y = 96
    # soft shadow to lift the letters off the sky
    for ch, w in zip(name, widths):
        d.text((x + 4, y + 5), ch, font=font, fill=(18, 20, 48, 160))
        x += w + gap
    x = (W - total) // 2
    for ch, w in zip(name, widths):
        d.text((x, y), ch, font=font, fill=CREAM + (255,))
        x += w + gap
    # thin rule under the name, the width of the word
    d.line([(W - total) // 2 + 8, y + size + 26,
            (W + total) // 2 - 8, y + size + 26],
           fill=CREAM + (220,), width=4)


def main():
    img = Image.new("RGB", (W, H))
    sky_gradient(img)
    base = img.convert("RGBA")
    d = ImageDraw.Draw(base)
    draw_clouds(d)
    draw_birds(d)
    draw_sun(base)
    d = ImageDraw.Draw(base)
    draw_sky_sea(d, base)
    draw_town(d)
    draw_name(d)
    out = base.convert("RGB")
    # palette-quantise to keep the file under the 1 MiB gate; dithering
    # breaks up the gradient banding a flat palette would leave
    out = out.convert("P", palette=Image.ADAPTIVE, colors=256,
                      dither=Image.FLOYDSTEINBERG)
    out.save(OUT, optimize=True)
    size = os.path.getsize(OUT)
    print(f"wrote {OUT} {size} bytes")
    assert size <= 1_048_576, "over the 1 MiB gate"


if __name__ == "__main__":
    main()
