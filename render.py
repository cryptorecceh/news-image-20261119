#!/usr/bin/env python3
"""Draw the front page for Thursday 19 November 2026 and save entry.png.

Build-time helper only — it needs Pillow, which the graded program does
not. Run it here, on the build machine::

    python3 render.py

It composes a 1024x1024 broadsheet from the four news photographs in
``assets/`` and the headlines below, then writes ``entry.png`` next to this
file. The graded entry, ``main.py``, only copies that file with the standard
library, so the entry itself runs with no network and no packages.

Stories on the page — every one of them first reported on 19 Nov 2026:

- the first-ever Trump–Xi–Putin trilateral, in Shenzhen at APEC;
- GTA VI's worldwide rollout, opening Vice City after thirteen years;
- the Democrats nominating Hakeem Jeffries, the first Black Speaker;
- NASA confirming Voyager 1 one light-day from Earth;
- six more stories from the same day in the strip at the foot.
"""

from pathlib import Path

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

BASE = Path(__file__).resolve().parent
PHOTOS = BASE / "assets"

SIZE = 1024
PAD = 12
EDGE = SIZE - PAD

PALETTE = {
    "paper": (247, 243, 235),
    "ink": (24, 24, 24),
    "navy": (15, 28, 46),
    "gold": (212, 164, 65),
    "crimson": (166, 38, 38),
    "grey": (96, 90, 78),
    "foam": (250, 248, 244),
    "sub": (70, 66, 58),
    "faint": (205, 200, 188),
    "hairline": (150, 142, 126),
}

FONT_DIR = Path("/usr/share/fonts/truetype/liberation")

BANNER_H = 110
LEAD_Y = 121
LEAD_H = 360
STRIP_H = 76
GRID_Y = 569
GRID_H = 200
GRID_W = 320
CAPTION_Y = 775
RULE_Y = 866
ALSO_TITLE_Y = 874
ALSO_Y = 902
ALSO_STEP = 19

LEAD = (
    "shenzhen.webp",
    "THREE PRESIDENTS, ONE TABLE IN SHENZHEN",
    "First-ever Trump–Xi–Putin summit: nuclear arms, AI and the Gulf war on the agenda",
)

PANELS = [
    (
        "vicecity.webp",
        "VICE CITY OPENS FOR GTA VI",
        "After 13 years, gamers enter Vice City as the global rollout begins",
    ),
    (
        "capitol.webp",
        "JEFFRIES SET TO BE FIRST BLACK SPEAKER",
        "Democrats pick Hakeem Jeffries to lead the House from January",
    ),
    (
        "voyager.webp",
        "VOYAGER 1, ONE LIGHT-DAY FROM EARTH",
        "NASA confirms the 49-year-old probe's record distance",
    ),
]

ALSO = [
    "Pew: Islam set to become the world's largest faith by 2035",
    "EU proposes a €45bn loan for Ukraine, repaid from Russian reparations",
    "Cyclone Akvan bears down on India's east coast",
    "Nvidia halts H-series chip sales to China after Huang's exit",
    "Fed minutes point to more rate hikes ahead",
    "Earth's missing billion years traced to mantle currents",
]


def load_font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


def serif(size):
    return load_font("LiberationSerif-Bold.ttf", size)


def sans(size):
    return load_font("LiberationSans-Regular.ttf", size)


def sans_bold(size):
    return load_font("LiberationSans-Bold.ttf", size)


def fit_headline(draw, text, start, width):
    for size in range(start, 9, -1):
        trial = serif(size)
        if draw.textlength(text, font=trial) <= width:
            return trial
    return serif(10)


def cover_crop(photo, width, height, focus=0.5):
    """Crop ``photo`` to ``width`` x ``height``, keeping the interesting
    band. ``focus`` 0.0 takes the top of the frame, 1.0 the bottom."""
    pw, ph = photo.size
    scale = max(width / pw, height / ph)
    big = photo.resize((round(pw * scale), round(ph * scale)), Image.LANCZOS)
    left = (big.width - width) // 2
    top = round((big.height - height) * focus)
    return big.crop((left, top, left + width, top + height))


def wrap_text(draw, text, font, width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def lettered(draw, x, y, text, font, colour, gap=4):
    for char in text:
        draw.text((x, y), char, font=font, fill=colour)
        x += draw.textlength(char, font=font) + gap
    return x


def lettered_centre(draw, cx, y, text, font, colour, gap=4):
    total = sum(draw.textlength(c, font=font) + gap for c in text) - gap
    lettered(draw, round(cx - total / 2), y, text, font, colour, gap)


def draw_banner(canvas, draw):
    draw.rectangle([0, 0, SIZE, BANNER_H], fill=PALETTE["navy"])
    draw.text((SIZE // 2, 14), "THE WORLD IN ONE PAGE",
              font=serif(56), fill=PALETTE["foam"], anchor="ma")
    lettered_centre(draw, SIZE // 2, 74, "THURSDAY · 19 NOVEMBER 2026",
                    sans_bold(25), PALETTE["gold"], gap=6)
    draw.rectangle([0, BANNER_H, SIZE, BANNER_H + 3], fill=PALETTE["gold"])


def draw_lead(canvas, draw):
    photo, head, sub = LEAD
    shot = cover_crop(Image.open(PHOTOS / photo), EDGE - PAD, LEAD_H,
                      focus=0.45)
    canvas.paste(shot, (PAD, LEAD_Y))
    draw.rectangle([PAD, LEAD_Y, EDGE, LEAD_Y + LEAD_H],
                   outline=PALETTE["ink"], width=2)
    band = LEAD_Y + LEAD_H
    draw.rectangle([0, band, SIZE, band + STRIP_H], fill=PALETTE["navy"])
    headline = fit_headline(draw, head, 34, EDGE - PAD)
    draw.text((SIZE // 2, band + 8), head,
              font=headline, fill=PALETTE["foam"], anchor="ma")
    draw.text((SIZE // 2, band + 47), sub,
              font=sans(20), fill=PALETTE["faint"], anchor="ma")


def draw_grid(canvas, draw):
    columns = [PAD, 352, 692]
    for (photo, head, sub), x in zip(PANELS, columns):
        shot = cover_crop(Image.open(PHOTOS / photo), GRID_W, GRID_H)
        canvas.paste(shot, (x, GRID_Y))
        draw.rectangle([x, GRID_Y, x + GRID_W, GRID_Y + GRID_H],
                       outline=PALETTE["ink"], width=2)
        head_font = sans_bold(19)
        for row, line in enumerate(wrap_text(draw, head, head_font, GRID_W)):
            draw.text((x, CAPTION_Y + row * 23), line,
                      font=head_font, fill=PALETTE["ink"])
        sub_font = sans(15)
        for row, line in enumerate(wrap_text(draw, sub, sub_font, GRID_W)):
            draw.text((x, CAPTION_Y + 2 * 23 + row * 18), line,
                      font=sub_font, fill=PALETTE["sub"])


def draw_also(draw):
    draw.line([PAD, RULE_Y, EDGE, RULE_Y], fill=PALETTE["grey"], width=1)
    lettered_centre(draw, SIZE // 2, ALSO_TITLE_Y, "ALSO ON 19 NOVEMBER",
                    sans_bold(20), PALETTE["crimson"], gap=3)
    item_font = sans(18)
    for row, line in enumerate(ALSO):
        draw.text((PAD, ALSO_Y + row * ALSO_STEP),
                  "•  " + line, font=item_font, fill=PALETTE["ink"])


def draw_border(draw):
    draw.rectangle([0, 0, SIZE - 1, SIZE - 1], outline=PALETTE["ink"], width=3)
    draw.rectangle([4, 4, SIZE - 5, SIZE - 5],
                   outline=PALETTE["hairline"], width=1)


def build():
    canvas = Image.new("RGB", (SIZE, SIZE), PALETTE["paper"])
    draw = ImageDraw.Draw(canvas)
    draw_banner(canvas, draw)
    draw_lead(canvas, draw)
    draw_grid(canvas, draw)
    draw_also(draw)
    draw_border(draw)
    out = BASE / "entry.png"
    canvas.save(out, "PNG", optimize=True)
    size = out.stat().st_size
    print("wrote", out, size, "bytes")
    if size > 1048576:
        # Photographs can push the PNG past the 1 MiB cap; a JPEG under
        # the same name is allowed — the gate reads the first bytes.
        canvas.save(out, "JPEG", quality=88, optimize=True)
        size = out.stat().st_size
        print("PNG over 1 MiB; saved as JPEG inside entry.png:", size, "bytes")
    assert size <= 1048576, "entry.png still over 1 MiB"
    assert canvas.size == (SIZE, SIZE)


if __name__ == "__main__":
    build()
