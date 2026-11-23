#!/usr/bin/env python3
"""Draw '22 November 2026': one bold, readable page of the day's world news.

The image is a flat-vector front page: a huge date, six major stories with
original pictograms, and a short 'also today' strip.  Every item was reported
on Sunday 22 November 2026.  No network and no third-party artwork are used.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONTS = r"C:\Windows\Fonts"

PAPER = (250, 247, 240)
INK = (17, 30, 43)
RED = (176, 42, 35)
TEAL = (17, 100, 99)
BLUE = (34, 72, 126)
GOLD = (176, 118, 18)
PURPLE = (91, 62, 121)
GREEN = (39, 101, 67)
GRAY = (95, 101, 107)
LIGHT = (232, 228, 216)
WHITE = (255, 255, 255)
CARD = (254, 252, 247)


def font(name, size):
    return ImageFont.truetype(FONTS + "\\" + name, size)


DISPLAY = "Impact.ttf"
SERIF = "PlayfairDisplay-Bold.ttf"
SERIF_IT = "PlayfairDisplay-Italic.ttf"
COND = "Oswald-Bold.ttf"
SANS = "arial.ttf"
SANS_B = "arialbd.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def text(x, y, s, f, fill=INK, anchor="lt"):
    d.text((x, y), s, font=f, fill=fill, anchor=anchor)


def fitted(s, name, size, maxw):
    """Shrink a face until the line fits the given pixel width."""
    while size > 9:
        f = font(name, size)
        if d.textlength(s, font=f) <= maxw:
            return f
        size -= 2
    return font(name, size)


def wrap(s, f, maxw):
    lines, cur = [], ""
    for word in s.split():
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


def tag(x, y, label, color, f=None, pad=8, h=26, width=None):
    f = f or font(COND, 15)
    w = width or (d.textlength(label, font=f) + 2 * pad)
    d.rectangle([x, y, x + w, y + h], fill=color)
    text(x + w / 2, y + h / 2, label, f, WHITE, "mm")
    return w


# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 54], fill=INK)
text(18, 11, "THE WORLD IN ONE DAY", font(COND, 27), WHITE)
text(1004, 15, "SUNDAY EDITION", font(COND, 19), (218, 224, 227), "rt")
d.rectangle([0, 54, W, 59], fill=RED)

# ---------------------------------------------------------------- the date
date = "22 NOVEMBER 2026"
text(512, 66, date, fitted(date, DISPLAY, 132, 984), INK, "mt")
text(512, 186,
     "COP31 collapses  ·  Iran's Gulf barrage  ·  186 drones over Ukraine  ·  24 lost in Nigeria",
     fitted("COP31 collapses  ·  Iran's Gulf barrage  ·  186 drones over Ukraine  ·  24 lost in Nigeria",
            SERIF_IT, 23, 984), RED, "mt")
d.line([(14, 217), (1010, 217)], fill=INK, width=3)

# ---------------------------------------------------------------- pictograms
def conference(box):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=(214, 226, 220))
    d.polygon([(x0 + 10, y0 + 34), ((x0 + x1) / 2, y0 + 8), (x1 - 10, y0 + 34)],
              fill=(63, 92, 86))
    d.rectangle([x0, y0 + 34, x1, y1], fill=(197, 212, 204))
    for i in range(5):
        cx = x0 + 34 + i * ((x1 - x0 - 68) / 4)
        d.ellipse([cx - 7, y1 - 40, cx + 7, y1 - 26], fill=(39, 58, 55))
        d.rectangle([cx - 9, y1 - 26, cx + 9, y1], fill=(39, 58, 55))
    d.rectangle([x1 - 118, y1 - 44, x1 - 14, y1 - 10], fill=WHITE, outline=RED, width=2)
    text(x1 - 66, y1 - 35, "NO DEAL", font(COND, 15), RED, "mt")


def barrage(box):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=(24, 47, 69))
    for i in range(3):
        x = x0 + 66 + i * 78
        d.line([(x - 34, y1 - 12), (x + 30, y0 + 20 + i * 6)], fill=(239, 180, 104), width=3)
        d.ellipse([x + 27, y0 + 16 + i * 6, x + 35, y0 + 24 + i * 6], fill=(240, 206, 120))
    cx = (x0 + x1) / 2
    d.polygon([(cx - 86, y1 - 20), (cx + 90, y1 - 20), (cx + 62, y1 - 4), (cx - 62, y1 - 4)],
              fill=(193, 202, 208))
    d.rectangle([cx - 48, y1 - 40, cx + 34, y1 - 20], fill=(232, 235, 236))
    d.rectangle([cx - 30, y1 - 58, cx + 6, y1 - 40], fill=(232, 235, 236))
    d.polygon([(cx + 40, y1 - 20), (cx + 48, y1 - 50), (cx + 56, y1 - 26),
               (cx + 64, y1 - 56), (cx + 72, y1 - 20)], fill=(225, 96, 40))


def drones(box):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=(29, 48, 67))
    for i, h in enumerate((26, 40, 32, 48, 36)):
        bx = x0 + 16 + i * ((x1 - x0 - 32) / 5)
        d.rectangle([bx, y1 - h, bx + (x1 - x0 - 32) / 5 - 5, y1], fill=(67, 86, 106))
        for r in range(2):
            d.rectangle([bx + 6, y1 - h + 7 + r * 12, bx + 13, y1 - h + 12 + r * 12],
                        fill=(238, 203, 121))
    for i in range(4):
        x = x0 + 42 + i * 70
        y = y0 + 20 + (i % 2) * 18
        d.line([(x - 9, y - 7), (x + 9, y + 7)], fill=(246, 208, 122), width=3)
        d.line([(x - 9, y + 7), (x + 9, y - 7)], fill=(246, 208, 122), width=3)


def boat(box):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=(206, 230, 235))
    for i in range(3):
        d.line([(x0 + 12, y0 + 22 + i * 14), (x1 - 12, y0 + 22 + i * 14)],
               fill=(96, 157, 175), width=2)
    cx = (x0 + x1) / 2
    d.polygon([(cx - 92, y1 - 22), (cx + 96, y1 - 22), (cx + 68, y1 - 5), (cx - 66, y1 - 5)],
              fill=(97, 108, 115))
    d.polygon([(cx - 52, y1 - 22), (cx - 84, y1 - 62), (cx + 6, y1 - 28)], fill=(186, 96, 60))
    d.line([(cx - 20, y1 - 46), (cx + 58, y1 - 70)], fill=(97, 108, 115), width=4)


def campus(box):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=(23, 39, 56))
    for i in range(3):
        y = y0 + 10 + i * 24
        d.rectangle([x0 + 24, y, x1 - 24, y + 18], fill=(61, 83, 105))
        d.ellipse([x0 + 32, y + 6, x0 + 39, y + 13], fill=(124, 212, 161))
        d.line([(x0 + 50, y + 12), (x1 - 44, y + 12)], fill=(110, 138, 160), width=2)
    d.rectangle([x1 - 118, y0 + 12, x1 - 22, y0 + 44], fill=(226, 188, 92))
    text(x1 - 70, y0 + 27, "AI", font(COND, 20), INK, "mm")


def planet(box):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=(19, 31, 53))
    for i in range(22):
        d.point((x0 + (i * 37) % (x1 - x0), y0 + (i * 19) % (y1 - y0)), fill=(228, 228, 216))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    r = 36
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(188, 139, 94))
    d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=(123, 86, 62), width=3)
    d.ellipse([cx - r - 22, cy - 8, cx + r + 22, cy + 10], outline=(226, 202, 150), width=2)
    d.ellipse([cx + r + 26, cy - 4, cx + r + 36, cy + 6], fill=(240, 206, 120))


ICONS = {"conference": conference, "barrage": barrage, "drones": drones,
         "boat": boat, "campus": campus, "planet": planet}


def icon(kind, box):
    """Draw on a layer so no stroke escapes the picture box."""
    global d
    x0, y0, x1, y1 = (int(v) for v in box)
    layer = Image.new("RGB", (x1 - x0, y1 - y0), PAPER)
    saved = d
    d = ImageDraw.Draw(layer)
    ICONS[kind]((0, 0, x1 - x0, y1 - y0))
    d = saved
    img.paste(layer, (x0, y0))


# ---------------------------------------------------------------- six stories
stories = [
    ("CLIMATE · ANTALYA", RED, "conference",
     "COP31 ends with no deal",
     "Nearly 200 nations fail to agree a final text; the draft omitted fossil fuels.",
     "Reuters · AP"),
    ("GULF · WAR & OIL", RED, "barrage",
     "Iran's barrage shakes the Gulf",
     "Trump says missile launches hit a one-year high; two tankers struck mines in Hormuz. Brent near $92.",
     "Reuters · AP"),
    ("UKRAINE · WAR", INK, "drones",
     "186 drones; four dead",
     "Air defences down 161; a block collapses in Dymer and a ship burns in the Baltic.",
     "Reuters · Guardian"),
    ("NIGERIA · DISASTER", TEAL, "boat",
     "24 dead in boat capsizing",
     "A boat carrying mourners overturns at Yenagoa; the toll rises to 24.",
     "Reuters"),
    ("UNITED STATES · TECH", BLUE, "campus",
     "SpaceX unveils $74bn AI campuses",
     "New supercomputing sites are announced in Texas and Arizona.",
     "Reuters"),
    ("SCIENCE · MERCURY", PURPLE, "planet",
     "BepiColombo enters orbit",
     "The probe reaches Mercury after an eight-year cruise.",
     "AP · PBS"),
]

cw = (982 - 2 * 12) / 3
for i, (label, col, art, headline, caption, source) in enumerate(stories):
    row, colno = divmod(i, 3)
    x = 14 + colno * (cw + 12)
    y = 228 + row * 322
    d.rectangle([x, y, x + cw, y + 310], fill=CARD, outline=(196, 192, 182), width=1)
    d.rectangle([x + 1, y + 1, x + cw - 1, y + 32], fill=col)
    text(x + 10, y + 9, label, font(COND, 15), WHITE)
    text(x + cw - 12, y + 9, "22 NOV", font(COND, 14), WHITE, "rt")
    icon(art, (x + 1, y + 33, x + cw - 1, y + 135))
    yy = para(x + 12, y + 146, headline, fitted(headline, SERIF, 28, cw - 24),
              cw - 24, 33, INK, 2)
    para(x + 12, yy + 7, caption, font(SANS, 16), cw - 24, 20, (62, 69, 75), 3)
    text(x + 12, y + 293, source, font(COND, 12), GRAY)

# ---------------------------------------------------------------- also today
d.rectangle([14, 878, 1010, 950], fill=LIGHT)
d.rectangle([14, 878, 1010, 906], fill=INK)
text(24, 883, "ALSO ON SUNDAY 22 NOVEMBER", font(COND, 16), WHITE)
text(1000, 884, "SIX MORE STORIES", font(COND, 12), (214, 220, 224), "rt")
also = [
    ("US POLITICS", "Democrats hold a 56-seat Senate majority after the midterms"),
    ("INDONESIA", "Candy-factory fire kills three; 36 are missing"),
    ("SOUTH KOREA", "Education minister resigns over AI exam checks"),
    ("SPORT", "Alcaraz beats Zverev for a first ATP Finals title"),
]
aw = (982 - 3 * 10) / 4
for i, (where, item) in enumerate(also):
    x = 18 + i * (aw + 10)
    text(x, 912, where, font(COND, 11), RED)
    para(x, 927, item, font(SANS, 13), aw - 4, 15, INK, 2)

# ---------------------------------------------------------------- footer
d.rectangle([0, 958, W, H], fill=INK)
text(16, 968, "SOURCES: Reuters · AP · BBC · CNN · DW · AFP · Al Jazeera · The Guardian · Yonhap",
     font(SANS, 12), (222, 229, 232))
text(16, 990, "ONE DAY · ONE IMAGE · ALL STORIES REPORTED 22 NOVEMBER 2026",
     font(COND, 12), (196, 207, 213))
text(1008, 968, "22 XI 26", font(SERIF, 26), (222, 229, 232), "rt")

img.save("entry.png", format="PNG", optimize=True)
print("wrote entry.png", img.size)
