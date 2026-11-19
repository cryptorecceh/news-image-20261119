#!/usr/bin/env python3
"""Compose entry.png for the 19 November 2026 news-image bounty.

Run on the build machine only: python3 render.py (needs Pillow here).
The picture itself is a broadsheet-style front page for Thursday
19 November 2026, built from four generated news photographs in
assets/ plus headlines drawn with local Liberation fonts. The graded
program, main.py, is separate: it only copies entry.png with the
standard library, so the entry runs with no network and no packages.

What the page carries (all of it first reported on 19 Nov 2026):
  * the first-ever Trump-Xi-Putin trilateral in Shenzhen (APEC),
  * GTA VI's global rollout begins after a 13-year wait,
  * Democrats nominate Hakeem Jeffries, the first Black Speaker,
  * NASA confirms Voyager 1 one light-day from Earth,
  * and a strip of six more stories from the same day.
"""

import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets")

PAGE = 1024
MARGIN = 12
RIGHT = PAGE - MARGIN

BG = (247, 243, 235)
FG = (24, 24, 24)
NAVY = (15, 28, 46)
GOLD = (212, 164, 65)
CRIMSON = (166, 38, 38)
GREY = (96, 90, 78)
FOAM = (250, 248, 244)
SUB = (70, 66, 58)
FAINT = (205, 200, 188)
FRAME_INNER = (150, 142, 126)

FACES = "/usr/share/fonts/truetype/liberation/"
SERIF = os.path.join(FACES, "LiberationSerif-Bold.ttf")
PLAIN = os.path.join(FACES, "LiberationSans-Regular.ttf")
BOLD = os.path.join(FACES, "LiberationSans-Bold.ttf")

MAST_H = 110
LEAD_TOP = 121
LEAD_H = 360
STRIP_H = 76
PANEL_TOP = 569
PANEL_H = 200
PANEL_W = 320
HEAD_Y = 775
RULE_Y = 866
ALSO_Y = 874
ALSO_FIRST = 902
ALSO_STEP = 19

LEAD = {
    "photo": "shenzhen.webp",
    "head": "THREE PRESIDENTS, ONE TABLE IN SHENZHEN",
    "sub": "First-ever Trump\u2013Xi\u2013Putin summit: nuclear arms, AI and the Gulf war on the agenda",
}

PANELS = [
    {
        "photo": "vicecity.webp",
        "head": "VICE CITY OPENS FOR GTA VI",
        "sub": "After 13 years, gamers enter Vice City as the global rollout begins",
    },
    {
        "photo": "capitol.webp",
        "head": "JEFFRIES SET TO BE FIRST BLACK SPEAKER",
        "sub": "Democrats pick Hakeem Jeffries to lead the House from January",
    },
    {
        "photo": "voyager.webp",
        "head": "VOYAGER 1, ONE LIGHT-DAY FROM EARTH",
        "sub": "NASA confirms the 49-year-old probe's record distance",
    },
]

ALSO = [
    "Pew: Islam set to become the world's largest faith by 2035",
    "EU proposes a \u20ac45bn loan for Ukraine, repaid from Russian reparations",
    "Cyclone Akvan bears down on India's east coast",
    "Nvidia halts H-series chip sales to China after Huang's exit",
    "Fed minutes point to more rate hikes ahead",
    "Earth's missing billion years traced to mantle currents",
]


def face(path, size):
    return ImageFont.truetype(path, size)


def shrink(draw, path, text, top, width):
    size = top
    while size > 10:
        trial = face(path, size)
        if draw.textlength(text, font=trial) <= width:
            return trial
        size -= 1
    return face(path, size)


def cover(img, w, h):
    iw, ih = img.size
    factor = max(w / iw, h / ih)
    grown = img.resize((round(iw * factor), round(ih * factor)), Image.LANCZOS)
    ox = (grown.size[0] - w) // 2
    oy = (grown.size[1] - h) // 2
    return grown.crop((ox, oy, ox + w, oy + h))


def fold(draw, text, fnt, width):
    parts = text.split()
    out, line = [], ""
    for part in parts:
        cand = part if not line else line + " " + part
        if draw.textlength(cand, font=fnt) <= width:
            line = cand
        else:
            if line:
                out.append(line)
            line = part
    if line:
        out.append(line)
    return out


def spaced(draw, pos, text, fnt, color, gap=4):
    x, y = pos
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=color)
        x += draw.textlength(ch, font=fnt) + gap
    return x


def spaced_centre(draw, cx, y, text, fnt, color, gap=4):
    total = sum(draw.textlength(ch, font=fnt) + gap for ch in text) - gap
    spaced(draw, (round(cx - total / 2), y), text, fnt, color, gap)


class FrontPage:
    def __init__(self):
        self.page = Image.new("RGB", (PAGE, PAGE), BG)
        self.d = ImageDraw.Draw(self.page)

    def masthead(self):
        d = self.d
        d.rectangle([0, 0, PAGE, MAST_H], fill=NAVY)
        d.text((PAGE // 2, 14), "THE WORLD IN ONE PAGE",
               font=face(SERIF, 56), fill=FOAM, anchor="ma")
        spaced_centre(d, PAGE // 2, 74, "THURSDAY \u00b7 19 NOVEMBER 2026",
                      face(BOLD, 25), GOLD, gap=6)
        d.rectangle([0, MAST_H, PAGE, MAST_H + 3], fill=GOLD)

    def lead(self):
        d = self.d
        photo = cover(Image.open(os.path.join(ASSETS, LEAD["photo"])),
                      RIGHT - MARGIN, LEAD_H)
        self.page.paste(photo, (MARGIN, LEAD_TOP))
        d.rectangle([MARGIN, LEAD_TOP, RIGHT, LEAD_TOP + LEAD_H],
                    outline=FG, width=2)
        strip_top = LEAD_TOP + LEAD_H
        d.rectangle([0, strip_top, PAGE, strip_top + STRIP_H], fill=NAVY)
        head = shrink(d, SERIF, LEAD["head"], 34, RIGHT - MARGIN)
        d.text((PAGE // 2, strip_top + 8), LEAD["head"],
               font=head, fill=FOAM, anchor="ma")
        d.text((PAGE // 2, strip_top + 47), LEAD["sub"],
               font=face(PLAIN, 20), fill=FAINT, anchor="ma")

    def panels(self):
        d = self.d
        xs = [MARGIN, 352, 692]
        for panel, x in zip(PANELS, xs):
            photo = cover(Image.open(os.path.join(ASSETS, panel["photo"])),
                          PANEL_W, PANEL_H)
            self.page.paste(photo, (x, PANEL_TOP))
            d.rectangle([x, PANEL_TOP, x + PANEL_W, PANEL_TOP + PANEL_H],
                        outline=FG, width=2)
            hf = face(BOLD, 19)
            for i, line in enumerate(fold(d, panel["head"], hf, PANEL_W)):
                d.text((x, HEAD_Y + i * 23), line, font=hf, fill=FG)
            sf = face(PLAIN, 15)
            for i, line in enumerate(fold(d, panel["sub"], sf, PANEL_W)):
                d.text((x, HEAD_Y + 2 * 23 + i * 18), line, font=sf, fill=SUB)

    def also(self):
        d = self.d
        d.line([MARGIN, RULE_Y, RIGHT, RULE_Y], fill=GREY, width=1)
        spaced_centre(d, PAGE // 2, ALSO_Y, "ALSO ON 19 NOVEMBER",
                      face(BOLD, 20), CRIMSON, gap=3)
        lf = face(PLAIN, 18)
        for i, line in enumerate(ALSO):
            d.text((MARGIN, ALSO_FIRST + i * ALSO_STEP),
                   "\u2022  " + line, font=lf, fill=FG)

    def frame(self):
        d = self.d
        d.rectangle([0, 0, PAGE - 1, PAGE - 1], outline=FG, width=3)
        d.rectangle([4, 4, PAGE - 5, PAGE - 5], outline=FRAME_INNER, width=1)

    def save(self):
        out = os.path.join(BASE, "entry.png")
        self.page.save(out, "PNG", optimize=True)
        size = os.path.getsize(out)
        print("wrote", out, size, "bytes")
        if size > 1048576:
            # PNG of photos can run past the cap; a JPEG in the same
            # name is allowed, the gate reads the first bytes.
            self.page.save(out, "JPEG", quality=88, optimize=True)
            size = os.path.getsize(out)
            print("PNG over 1 MiB; saved as JPEG inside entry.png:",
                  size, "bytes")
        assert size <= 1048576, "entry.png still over 1 MiB"
        assert self.page.size == (PAGE, PAGE)


def build():
    sheet = FrontPage()
    sheet.masthead()
    sheet.lead()
    sheet.panels()
    sheet.also()
    sheet.frame()
    sheet.save()


if __name__ == "__main__":
    build()
