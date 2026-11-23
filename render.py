#!/usr/bin/env python3
"""Draw 'The World in One Day': a one-page front page of Sunday 22 November 2026.

All facts below are events reported on 22 November 2026.  Every scene is an
original flat-vector illustration drawn with PIL; no photographs or third-party
artwork are used.  The program only writes entry.png -- it needs no network.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024

BG = (247, 244, 236)
INK = (18, 33, 46)
RED = (168, 42, 36)
GOLD = (190, 128, 20)
TEAL = (21, 104, 103)
BLUE = (38, 78, 130)
PURPLE = (96, 66, 128)
GREEN = (43, 108, 71)
GRAY = (108, 114, 118)
LIGHT = (233, 229, 217)
WHITE = (255, 255, 255)
PAPER = (253, 251, 246)

FONTS = r"C:\Windows\Fonts"


def font(name, size):
    return ImageFont.truetype(FONTS + "\\" + name, size)


SERIF = "PlayfairDisplay-Black.ttf"
SERIF_B = "PlayfairDisplay-Bold.ttf"
SERIF_I = "PlayfairDisplay-Italic.ttf"
COND = "Oswald-Bold.ttf"
SANS = "arial.ttf"
SANS_B = "arialbd.ttf"

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def text(x, y, s, f, fill=INK, anchor="lt"):
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)


def fit(s, f, maxw, start):
    """Shrink a font until the string fits maxw."""
    while start > 8 and d.textlength(s, font=f) > maxw:
        start -= 1
        f = font(f.path if hasattr(f, "path") else SERIF, start)
    return f


def wrap(s, f, maxw):
    words = s.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=f) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(x, y, s, f, maxw, lh, fill=INK, maxlines=99):
    for i, line in enumerate(wrap(s, f, maxw)[:maxlines]):
        text(x, y + i * lh, line, f, fill)
    return y + len(wrap(s, f, maxw)[:maxlines]) * lh


def rule(y, x0=14, x1=1010, color=INK, width=1):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


def chip(x, y, label, color, f=None, pad=6, h=17):
    f = f or font(COND, 11)
    w = d.textlength(label, font=f) + 2 * pad
    d.rectangle([x, y, x + w, y + h], fill=color)
    text(x + pad, y + 2, label, f, WHITE)
    return w


# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 32], fill=INK)
text(16, 7, "THE WORLD IN ONE DAY", font(COND, 17), WHITE)
text(1008, 8, "SUNDAY 22 NOVEMBER 2026   ·   EDITION 01", font(COND, 13), WHITE, "rt")
d.rectangle([0, 32, W, 35], fill=RED)

# ---------------------------------------------------------------- headline
headline = "Sunday 22 November 2026"
head = font(SERIF, 73)
while d.textlength(headline, font=head) > 984 and head.size > 20:
    head = font(SERIF, head.size - 1)
text(512, 44, headline, head, INK, "mt")
text(512, 121, "COP31 ends with no deal  ·  Iran's Gulf barrage  ·  186 drones over Ukraine  ·  24 lost in Nigeria",
     font(SERIF_I, 20), RED, "mt")
rule(155, width=3)
rule(159, color=RED, width=1)

# ---------------------------------------------------------------- statistics
stats = [
    ("186", "drones fired at Ukraine", RED),
    ("161", "shot down or suppressed", INK),
    ("~200", "nations at COP31", TEAL),
    ("0", "climate deal reached", RED),
    ("24", "dead in Nigeria boat", BLUE),
    ("$92", "Brent crude, per barrel", GOLD),
]
cw = 982 / 6
for i, (num, lab, col) in enumerate(stats):
    cx = 14 + i * cw
    text(cx + cw / 2, 170, num, font(SERIF_B, 34), col, "mt")
    text(cx + cw / 2, 208, lab, font(COND, 12), GRAY, "mt")
    if i:
        d.line([(cx, 170), (cx, 222)], fill=LIGHT, width=1)
rule(226, color=LIGHT)

# ---------------------------------------------------------------- regions
regions = [("EUROPE 4", INK), ("MIDDLE EAST 5", RED), ("ASIA–PACIFIC 4", TEAL),
           ("AMERICAS 5", BLUE), ("AFRICA 3", GOLD), ("OCEANIA 2", PURPLE), ("WORLD 2", GREEN)]
rw = 982 / 7
for i, (lab, col) in enumerate(regions):
    x = 14 + i * rw
    d.rectangle([x, 232, x + rw - 3, 253], fill=col)
    text(x + rw / 2 - 1, 236, lab, font(COND, 13), WHITE, "mt")

# ---------------------------------------------------------------- icon art
def drones(box, col=INK, n=5):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(28, 46, 64))
    for i in range(n):
        x = x0 + 22 + (i * 47) % max(1, (x1 - x0 - 40))
        y = y0 + 16 + (i * 29) % max(1, (y1 - y0 - 30))
        d.line([(x - 6, y - 4), (x + 6, y + 4)], fill=(244, 206, 120), width=2)
        d.line([(x - 6, y + 4), (x + 6, y - 4)], fill=(244, 206, 120), width=2)
    for i in range(3):
        y = y0 + 20 + i * 18
        d.line([(x0 + 8, y), (x1 - 8, y + 7)], fill=(86, 108, 130), width=1)


def city(box, night=False):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(31, 52, 72) if night else (232, 238, 242))
    bw = (x1 - x0) / 7
    for i in range(7):
        h = 18 + ((i * 13) % 34)
        bx = x0 + i * bw + 2
        d.rectangle([bx, y1 - h, bx + bw - 5, y1], fill=(64, 82, 101) if night else (150, 163, 174))
        for r in range(3):
            for c in range(2):
                if (i + r + c) % 3:
                    d.rectangle([bx + 4 + c * 10, y1 - h + 6 + r * 10,
                                 bx + 9 + c * 10, y1 - h + 10 + r * 10],
                                fill=(244, 206, 120) if night else (250, 248, 240))


def conference(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(219, 227, 223))
    d.polygon([(x0, y0 + 30), ((x0 + x1) / 2, y0 + 6),
               (x1, y0 + 30)], fill=(67, 96, 92))
    d.rectangle([x0, y0 + 30, x1, y1], fill=(205, 215, 210))
    for i in range(5):
        cx = x0 + 26 + i * ((x1 - x0 - 50) / 5)
        d.ellipse([cx - 9, y1 - 34, cx + 9, y1 - 16], fill=(35, 58, 54))
        d.rectangle([cx - 11, y1 - 16, cx + 11, y1], fill=(35, 58, 54))
    d.rectangle([x1 - 96, y0 + 12, x1 - 10, y0 + 44], fill=WHITE, outline=RED, width=2)
    text(x1 - 53, y0 + 19, "NO DEAL", font(COND, 13), RED, "mt")


def ship(box, fire=False):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(24, 56, 74))
    for i in range(4):
        y = y0 + 18 + i * 12
        d.line([(x0 + 8, y), (x1 - 8, y)], fill=(58, 96, 116), width=1)
    cx = (x0 + x1) / 2
    d.polygon([(cx - 74, y1 - 24), (cx + 78, y1 - 24), (cx + 58, y1 - 8), (cx - 58, y1 - 8)], fill=(190, 197, 202))
    d.rectangle([cx - 44, y1 - 46, cx + 30, y1 - 24], fill=(226, 229, 230))
    d.rectangle([cx - 26, y1 - 64, cx + 8, y1 - 46], fill=(226, 229, 230))
    d.rectangle([cx - 22, y1 - 60, cx - 6, y1 - 50], fill=(86, 120, 140))
    if fire:
        d.polygon([(cx + 40, y1 - 24), (cx + 48, y1 - 50), (cx + 56, y1 - 30),
                   (cx + 64, y1 - 58), (cx + 72, y1 - 24)], fill=(226, 96, 40))
    d.line([(cx - 70, y1 - 4), (cx + 70, y1 - 4)], fill=(150, 180, 195), width=2)


def radar(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(26, 47, 63))
    cx = (x0 + x1) / 2
    for r in (16, 28, 40):
        d.arc([cx - r, y1 - 8 - r, cx + r, y1 - 8 + r], 180, 355, fill=(120, 170, 178), width=2)
    d.line([(cx, y1 - 8), (cx + 26, y1 - 40)], fill=(240, 208, 120), width=3)
    d.ellipse([cx - 4, y1 - 12, cx + 4, y1 - 4], fill=(240, 208, 120))


def flame(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(232, 232, 224))
    cx = (x0 + x1) / 2
    d.polygon([(cx - 20, y1 - 8), (cx - 10, y1 - 34), (cx - 2, y1 - 20),
               (cx + 8, y1 - 48), (cx + 20, y1 - 8)], fill=(206, 82, 34))
    d.polygon([(cx - 9, y1 - 8), (cx, y1 - 26), (cx + 9, y1 - 8)], fill=(246, 196, 90))
    d.rectangle([x0 + 8, y1 - 10, x1 - 8, y1 - 6], fill=(60, 70, 74))


def water(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(214, 232, 236))
    for i in range(3):
        y = y0 + 12 + i * 12
        d.line([(x0 + 10, y), (x1 - 10, y)], fill=(86, 148, 164), width=2)
    d.polygon([(x0 + 24, y1 - 12), (x1 - 24, y1 - 12), (x1 - 34, y1 - 6), (x0 + 34, y1 - 6)], fill=(120, 132, 138))


def ballot(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(226, 232, 226))
    d.rectangle([x0 + 28, y0 + 8, x1 - 16, y1 - 8], fill=WHITE, outline=INK, width=2)
    d.line([(x0 + 40, y0 + 24), (x0 + 52, y0 + 36), (x0 + 74, y0 + 12)], fill=GREEN, width=4)
    d.rectangle([x0 + 14, y0 + 18, x0 + 30, y1 - 8], fill=(120, 130, 136))


def plane(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(226, 234, 240))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    d.line([(x0 + 14, y1 - 12), (x1 - 14, y0 + 12)], fill=BLUE, width=3)
    for i in range(5):
        x = x0 + 20 + i * 24
        y = y1 - 16 - i * 9
        d.line([(x, y), (x + 12, y + 5)], fill=(150, 160, 170), width=1)


def exam(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(234, 230, 220))
    d.rectangle([x0 + 20, y0 + 8, x1 - 20, y1 - 8], fill=WHITE, outline=INK, width=2)
    for i in range(3):
        d.line([(x0 + 30, y0 + 18 + i * 10), (x1 - 34, y0 + 18 + i * 10)], fill=(170, 176, 180), width=1)
    d.ellipse([x1 - 40, y0 + 10, x1 - 12, y0 + 38], outline=RED, width=2)
    d.line([(x1 - 36, y0 + 26), (x1 - 16, y0 + 22)], fill=RED, width=2)


def server(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(24, 40, 58))
    for i in range(3):
        y = y0 + 10 + i * 17
        d.rectangle([x0 + 18, y, x1 - 18, y + 13], fill=(62, 84, 104), outline=(110, 140, 160))
        d.ellipse([x0 + 24, y + 4, x0 + 30, y + 10], fill=(120, 214, 160))
    d.line([(x1 - 26, y0 + 6), (x1 - 26, y1 - 6)], fill=(226, 190, 100), width=2)


def planet(box, saturn=False):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(20, 32, 54))
    for i in range(14):
        d.point((x0 + (i * 37) % (x1 - x0), y0 + (i * 19) % (y1 - y0)), fill=(230, 230, 220))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    r = min(y1 - y0, x1 - x0) / 2 - 8
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(196, 146, 96))
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(120, 84, 60), width=2)
    if saturn:
        d.ellipse([cx - r - 12, cy - 5, cx + r + 12, cy + 7], outline=(226, 202, 150), width=2)


def trophy(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(30, 54, 72))
    cx = (x0 + x1) / 2
    d.polygon([(cx - 16, y0 + 10), (cx + 16, y0 + 10), (cx + 11, y0 + 30),
               (cx - 11, y0 + 30)], fill=(226, 184, 84))
    d.rectangle([cx - 4, y0 + 30, cx + 4, y0 + 40], fill=(226, 184, 84))
    d.rectangle([cx - 14, y0 + 40, cx + 14, y0 + 46], fill=(226, 184, 84))
    d.arc([cx - 26, y0 + 12, cx - 10, y0 + 30], 90, 270, fill=(226, 184, 84), width=3)
    d.arc([cx + 10, y0 + 12, cx + 26, y0 + 30], 270, 90, fill=(226, 184, 84), width=3)


def ball(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(40, 92, 66))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    r = min(y1 - y0, x1 - x0) / 2 - 8
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE, outline=INK, width=1)
    for a in (30, 150, 270):
        import math
        px = cx + math.cos(math.radians(a)) * r * 0.7
        py = cy + math.sin(math.radians(a)) * r * 0.7
        d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=INK)


def corridor(box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(224, 230, 224))
    d.polygon([(x0 + 10, y1 - 12), (x1 - 10, y1 - 12), (x1 - 30, y1 - 32), (x0 + 30, y1 - 32)], fill=(150, 160, 148))
    d.line([(x0 + 24, y1 - 18), (x1 - 24, y1 - 18)], fill=RED, width=4)
    for i in range(3):
        d.ellipse([x0 + 30 + i * 44, y0 + 14, x0 + 44 + i * 44, y0 + 28], fill=TEAL)


def icon(kind, box):
    """Draw a scene on its own layer so no stroke escapes the picture box."""
    global d
    x0, y0, x1, y1 = (int(v) for v in box)
    layer = Image.new("RGB", (x1 - x0, y1 - y0), BG)
    saved = d
    d = ImageDraw.Draw(layer)
    {
        "drones": drones, "city": city, "conference": conference, "ship": ship,
        "radar": radar, "flame": flame, "water": water, "ballot": ballot,
        "plane": plane, "exam": exam, "server": server, "planet": planet,
        "trophy": trophy, "ball": ball, "corridor": corridor,
    }[kind]((0, 0, x1 - x0, y1 - y0))
    d = saved
    img.paste(layer, (x0, y0))


# ---------------------------------------------------------------- lead stories
leads = [
    ("ANTALYA, TÜRKIYE · CLIMATE", RED, "conference",
     "COP31 ends with no deal",
     "Nearly 200 nations failed to agree a final text after the EU and others rejected a draft that omitted fossil fuels — the first breakdown of its kind in 17 years.",
     "Reuters · AP · CNN"),
    ("GULF · WAR & ENERGY", RED, "radar",
     "Iran's barrage shakes the Gulf",
     "Trump said Iran launched more missiles and drones in a week than at any time in a year. Iran's navy said two tankers hit mines in Hormuz; Gulf markets fell.",
     "Reuters · Euronews · AP"),
    ("KYIV REGION, UKRAINE · WAR", INK, "drones",
     "186 drones; four dead, 14 missing",
     "Air defences downed or suppressed 161 of the overnight strike drones. Part of a five-storey block collapsed; a ship burned in the Baltic as the war widened.",
     "Reuters · Guardian · AP"),
]

cw = (982 - 2 * 10) / 3
for i, (label, col, art, title, body, source) in enumerate(leads):
    x = 14 + i * (cw + 10)
    y = 262
    d.rectangle([x, y, x + cw, y + 238], fill=PAPER, outline=INK, width=1)
    icon(art, (x + 1, y + 1, x + cw - 1, y + 93))
    chip(x + 8, y + 8, label, col)
    yy = para(x + 10, y + 100, title, font(SERIF_B, 23), cw - 20, 26, INK, 3)
    yy = para(x + 10, yy + 5, body, font(SANS, 12), cw - 20, 15, INK, 5)
    text(x + 10, y + 227, source, font(COND, 10), GRAY)

# ---------------------------------------------------------------- ten stories
d.rectangle([14, 508, 1010, 532], fill=INK)
text(22, 513, "THE DAY IN TEN  ·  FILED SUNDAY 22 NOVEMBER 2026", font(COND, 14), WHITE)
text(1002, 515, "ORIGINAL ILLUSTRATIONS", font(COND, 10), (210, 216, 220), "rt")

ten = [
    ("Baltic sea", "ship", "Russian cargo ship burns after drone hit; Finland says the war is spilling over", "Reuters"),
    ("Benghazi, Libya", "ship", "Russian corvette sinks at port after suspected Ukrainian sea drones", "Reuters · AP"),
    ("Khartoum, Sudan", "flame", "RSF drones kill four and damage a UN building near the capital", "Al Jazeera"),
    ("Yenagoa, Nigeria", "water", "Boat carrying mourners capsizes; death toll rises to 24", "Reuters"),
    ("Candei, Indonesia", "flame", "Candy-factory fire leaves three dead and 36 missing", "DW"),
    ("Washington, US", "ballot", "Democrats hold a 56-seat Senate majority after the midterms", "Reuters"),
    ("Atlanta, US", "plane", "Over 1,000 Delta flights delayed by a weight-system fault", "AP"),
    ("Seoul, South Korea", "exam", "Education minister resigns over AI-cheating exam checks", "AFP · Yonhap"),
    ("Texas & Arizona", "server", "SpaceX unveils $74bn of AI supercomputing campuses", "Reuters"),
    ("Mercury", "planet", "BepiColombo enters orbit after an eight-year cruise", "AP · PBS"),
]
gw = (982 - 4 * 8) / 5
for i, (where, art, headline, source) in enumerate(ten):
    row, col = divmod(i, 5)
    x = 14 + col * (gw + 8)
    y = 538 + row * 100
    d.rectangle([x, y, x + gw, y + 96], fill=PAPER, outline=(190, 190, 182), width=1)
    icon(art, (x + 1, y + 1, x + gw - 1, y + 33))
    text(x + 6, y + 35, where.upper(), font(COND, 10), RED)
    para(x + 6, y + 47, headline, font(SANS_B, 11), gw - 12, 13, INK, 3)
    text(x + 6, y + 87, source, font(COND, 8), GRAY)

# ---------------------------------------------------------------- map + list
d.rectangle([14, 744, 400, 900], fill=PAPER, outline=INK, width=1)
text(22, 750, "WHERE IT HAPPENED", font(COND, 13), INK)
text(392, 752, "pins match lead stories", font(SERIF_I, 11), GRAY, "rt")

# simplified dotted world silhouette
continents = [
    [(28, 40), (70, 28), (110, 34), (124, 62), (104, 82), (76, 92), (50, 78)],
    [(112, 90), (134, 96), (146, 126), (134, 158), (118, 140)],
    [(170, 34), (230, 26), (292, 32), (330, 48), (310, 72), (258, 80), (214, 70), (178, 58)],
    [(190, 84), (246, 88), (276, 110), (250, 148), (216, 136)],
    [(286, 30), (330, 28), (346, 46), (330, 62), (296, 56)],
    [(300, 138), (340, 132), (356, 148), (340, 164), (306, 160)],
]
for poly in continents:
    d.polygon([(px + 22, py + 795) for px, py in poly], fill=(223, 228, 220))
    for yy in range(20, 170, 8):
        for xx in range(20, 360, 8):
            inside = False
            j = len(poly) - 1
            for i in range(len(poly)):
                xi, yi = poly[i]
                xj, yj = poly[j]
                if (yi > yy) != (yj > yy) and xx < (xj - xi) * (yy - yi) / (yj - yi) + xi:
                    inside = not inside
                j = i
            if inside:
                d.ellipse([xx + 22, yy + 795, xx + 24, yy + 797], fill=(176, 184, 180))
for x, y, n, c in [(300, 812, 1, TEAL), (322, 818, 2, RED), (284, 844, 3, RED),
                  (150, 838, 4, GOLD), (98, 816, 5, RED), (340, 874, 6, BLUE)]:
    d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=c, outline=WHITE, width=2)
    text(x, y - 1, str(n), font(COND, 10), WHITE, "mm")

d.rectangle([406, 744, 1010, 900], fill=PAPER, outline=INK, width=1)
text(414, 750, "ALSO ON SUNDAY  ·  MORE STORIES FROM 22 NOVEMBER", font(COND, 13), INK)
more = [
    "Hormuz: two supertankers catch fire after hitting mines",
    "Bahrain: Iran claims strikes on US bases; Manama denies it",
    "Gulf stock markets retreat as sporadic attacks continue",
    "Poland: prosecutors say three Russian missiles crossed the border",
    "Sudan: drone strikes near Khartoum kill four; UN building hit",
    "Indonesia: fire at candy factory kills three, 36 missing",
    "Nigeria: funeral boat capsizes; 24 confirmed dead",
    "South Korea: education chief quits over AI exam rules",
    "Japan: organic chemicals eyed for critical-products list",
    "India & Japan: agree to deepen defence-industry cooperation",
    "Australia: criticises US budget office over AUKUS report",
    "Brazil: former president Bolsonaro stable in intensive care",
    "US: Trump says Iran's missile launches at a one-year high",
    "West Bank: Israel's top general condemns settler arson",
    "Armenia: US-backed 'Trump corridor' due to open Monday",
    "Oil: Brent holds near $92 as Gulf risk premium persists",
    "Markets: Nasdaq down 10% on the week in AI-stock selloff",
    "Tennis: Alcaraz beats Zverev for a first ATP Finals title",
    "NWSL: Kansas City Current win the final 2–1 in Washington",
    "Kyiv: 14 still missing after a block collapses in a drone attack",
]
for i, s in enumerate(more):
    col, row = divmod(i, 10)
    x = 414 + col * 296
    y = 772 + row * 12
    d.ellipse([x, y + 3, x + 4, y + 7], fill=RED)
    text(x + 9, y, s, font(SANS, 10), INK)

# ---------------------------------------------------------------- date check
d.rectangle([14, 906, 1010, 958], fill=(238, 234, 224), outline=RED, width=2)
text(24, 911, "DATE CHECK — READ THIS FIRST", font(COND, 12), RED)
text(24, 928, "Every story on this page was reported on Sunday 22 November 2026. Earlier-week events appear here only as", font(SANS, 11), INK)
text(24, 942, "context, never as the day's news. Times are UTC unless noted. Scenes are original illustrations, not photographs.", font(SANS, 11), INK)

# ---------------------------------------------------------------- footer
d.rectangle([0, 964, W, H], fill=INK)
text(16, 978, "SOURCES: Reuters · AP · BBC · CNN · NPR · DW · AFP · Yonhap · Al Jazeera · The Guardian · WSJ · Fortune · Space.com",
     font(SANS, 10), WHITE)
text(16, 996, "ONE DAY · ONE IMAGE · COMPILED AND DRAWN BY AN AI AGENT · 22 NOV 2026", font(COND, 10), (200, 210, 216))
text(1008, 981, "22 XI 26", font(SERIF_B, 22), (220, 226, 230), "rt")

img.save("entry.png", format="PNG", optimize=True)
print("wrote entry.png", img.size)
