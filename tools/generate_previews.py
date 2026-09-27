#!/usr/bin/env python3
"""Generate README showcase mockups from the skin's own assets."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
SKIN = ROOT / "skin"
OUT = ROOT / "docs" / "showcase"
SIZE = (1600, 900)
OUTPUT_SIZE = (1920, 1080)
CYAN = "#00baff"
GREEN = "#00ff90"
INK = "#071018"
WHITE = "#f4f8fb"


def font(size: int, bold: bool = False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(f"/usr/share/fonts/TTF/{name}", size)


def asset(name: str, size=None):
    image = Image.open(SKIN / name).convert("RGBA")
    if size:
        image.thumbnail(size, Image.Resampling.LANCZOS)
    return image


def cover(image: Image.Image, size=SIZE):
    ratio = max(size[0] / image.width, size[1] / image.height)
    scaled = image.resize(
        (round(image.width * ratio), round(image.height * ratio)),
        Image.Resampling.LANCZOS,
    )
    left = (scaled.width - size[0]) // 2
    top = (scaled.height - size[1]) // 2
    return scaled.crop((left, top, left + size[0], top + size[1]))


def background(blur=5, darkness=0.42):
    image = cover(Image.open(SKIN / "menu-background.jpg").convert("RGB"))
    image = image.filter(ImageFilter.GaussianBlur(blur))
    image = ImageEnhance.Brightness(image).enhance(darkness).convert("RGBA")
    image.alpha_composite(Image.new("RGBA", SIZE, (2, 8, 14, 55)))
    return image


def paste_center(canvas, image, center):
    canvas.alpha_composite(
        image, (round(center[0] - image.width / 2), round(center[1] - image.height / 2))
    )


def save_preview(canvas, filename, **kwargs):
    """Export at the 1920x1080 resolution used by the current osu! setup."""
    canvas.resize(OUTPUT_SIZE, Image.Resampling.LANCZOS).save(OUT / filename, **kwargs)


def label(draw, text, xy, size, fill=WHITE, anchor="la", bold=False, stroke=0):
    draw.text(
        xy,
        text,
        font=font(size, bold),
        fill=fill,
        anchor=anchor,
        stroke_width=stroke,
        stroke_fill="#000000",
    )


def menu_preview():
    # Reproduce osu!lazer's current main-menu geometry, while keeping the
    # background shipped by the skin instead of exposing the last beatmap.
    canvas = background(0, 0.78)
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 1600, 47), fill=(22, 22, 22, 245))
    for x in (34, 98, 155, 202, 249, 296):
        draw.ellipse((x - 13, 10, x + 13, 36), outline=WHITE, width=2)
    label(draw, "TEAGAR", (1365, 24), 16, WHITE, anchor="rm")
    label(draw, "01:12:35", (1515, 24), 14, WHITE, anchor="rm")

    ribbon_y1, ribbon_y2 = 417, 529
    draw.rectangle((0, ribbon_y1, 1600, ribbon_y2), fill=(17, 18, 21, 235))
    sections = [
        (0, 423, "SETTINGS", "#277ea8"),
        (673, 920, "PLAY", "#d42ca0"),
        (920, 1075, "EDIT", "#d42ca0"),
        (1075, 1235, "BROWSE", "#d42ca0"),
        (1235, 1375, "EXIT", "#d42ca0"),
    ]
    for left, right, text, colour in sections:
        draw.polygon(((left, ribbon_y1), (right - 15, ribbon_y1), (right, ribbon_y2), (left, ribbon_y2)), fill=colour)
        label(draw, text, ((left + right) // 2, 473), 19, WHITE, anchor="mm", bold=True)

    draw.ellipse((397, 327, 687, 617), fill="#dd36a5", outline="#ffffff", width=9)
    draw.ellipse((414, 344, 670, 600), outline=(255, 255, 255, 65), width=4)
    label(draw, "osu!", (542, 474), 94, WHITE, anchor="mm", bold=True)
    label(draw, "TEAGAR'S 2.0", (542, 585), 15, WHITE, anchor="mm", bold=True)

    cursor = asset("cursor@2x.png", (62, 62))
    paste_center(canvas, cursor, (790, 465))
    label(draw, "osu!lazer", (26, 866), 15, WHITE)
    label(draw, "skin preview", (1574, 866), 14, "#c9d1d8", anchor="ra")
    save_preview(canvas, "menu.png", optimize=True)


def hit_object(canvas, center, number, scale=1.0, approach=True):
    circle = asset("hitcircle@2x.png")
    overlay = asset("hitcircleoverlay@2x.png")
    diameter = round(128 * scale)
    circle = circle.resize((diameter, diameter), Image.Resampling.LANCZOS)
    overlay = overlay.resize((diameter, diameter), Image.Resampling.LANCZOS)
    paste_center(canvas, circle, center)
    paste_center(canvas, overlay, center)
    if approach:
        ring = asset("approachcircle@2x.png")
        outer = round(205 * scale)
        ring = ring.resize((outer, outer), Image.Resampling.LANCZOS)
        ring.putalpha(ring.getchannel("A").point(lambda p: int(p * 0.68)))
        paste_center(canvas, ring, center)
    draw = ImageDraw.Draw(canvas)
    label(draw, str(number), center, round(47 * scale), WHITE, anchor="mm", bold=True, stroke=2)


def gameplay_preview():
    # Current gameplay setting uses 100% background dim and no blur.
    canvas = Image.new("RGBA", SIZE, (0, 0, 0, 255))
    draw = ImageDraw.Draw(canvas)
    points = [(635, 335), (930, 490), (1200, 300), (1030, 660)]
    for first, second in zip(points, points[1:]):
        draw.line((first, second), fill=(255, 255, 255, 50), width=5)
    for i, point in enumerate(points, 1):
        hit_object(canvas, point, i, 1.15, approach=i in (1, 2, 4))

    # Gameplay cursor size is 0.69 in the current local configuration.
    cursor = asset("cursor@2x.png", (52, 52))
    paste_center(canvas, cursor, (1015, 392))

    label(draw, "0013586", (1580, 35), 47, WHITE, anchor="ra", bold=True)
    label(draw, "99.72%", (1580, 78), 27, WHITE, anchor="ra", bold=True)
    label(draw, "431x", (22, 865), 58, WHITE, anchor="ls", bold=True, stroke=2)
    label(draw, "72", (1580, 870), 53, WHITE, anchor="rs", bold=True)
    for index, value in enumerate((13, 12, 13)):
        y = 408 + index * 56
        draw.line((1595, y - 18, 1595, y + 30), fill=CYAN, width=3)
        label(draw, str(value), (1578, y), 17, WHITE, anchor="rm", bold=True)
    # Horizontal hit-error meter observed at the bottom-centre.
    draw.rectangle((680, 882, 920, 887), fill="#ffdc00")
    draw.rectangle((920, 882, 990, 887), fill=GREEN)
    draw.rectangle((990, 882, 1060, 887), fill=CYAN)
    draw.rectangle((799, 874, 802, 894), fill=WHITE)
    save_preview(canvas, "gameplay-standard.png", optimize=True)


def mania_preview():
    # Current gameplay setting uses 100% background dim and no blur.
    canvas = Image.new("RGBA", SIZE, (0, 0, 0, 255))
    draw = ImageDraw.Draw(canvas)

    # Exact 7K geometry observed in-game at 1920x1080, mapped to this canvas.
    left, right, hit_y = 537, 1063, 707
    lane_width = (right - left) / 7
    stage = asset("mania-stage-bottom.png").resize((right - left, 25), Image.Resampling.LANCZOS)
    canvas.alpha_composite(stage, (left, 817))
    draw.rectangle((left, hit_y, right, hit_y + 2), fill=(0, 255, 0, 255))

    note_files = ["mania-note1.png", "mania-note2.png", "mania-note1.png", "mania-noteS.png",
                  "mania-note1.png", "mania-note2.png", "mania-note1.png"]
    notes = [(0, 205, 0), (1, 370, 120), (2, 125, 0), (3, 535, 190),
             (4, 300, 0), (5, 105, 135), (6, 455, 0), (0, 595, 0),
             (2, 500, 0), (4, 610, 0), (6, 250, 0)]
    for lane, y, hold in notes:
        x = round(left + lane * lane_width)
        width = round(lane_width)
        if hold:
            draw.rounded_rectangle((x + 7, y, x + width - 7, y + hold + 31), 25,
                                   fill=(183, 183, 183, 255))
        note = asset(note_files[lane]).resize((width, 44), Image.Resampling.LANCZOS)
        canvas.alpha_composite(note, (x, y + hold))

    label(draw, "0247186", (1583, 35), 47, WHITE, anchor="ra", bold=True)
    label(draw, "99.140%", (1583, 78), 27, WHITE, anchor="ra", bold=True)
    label(draw, "348x", (800, 420), 42, WHITE, anchor="mm", bold=True)
    label(draw, "300", (800, 535), 54, GREEN, anchor="mm", bold=True)
    draw.rectangle((680, 882, 920, 887), fill="#ffdc00")
    draw.rectangle((920, 882, 990, 887), fill=GREEN)
    draw.rectangle((990, 882, 1060, 887), fill=CYAN)
    draw.rectangle((799, 874, 802, 894), fill=WHITE)
    save_preview(canvas, "gameplay-mania.png", optimize=True)


def results_preview():
    canvas = background(8, 0.35)
    draw = ImageDraw.Draw(canvas)

    panel = asset("ranking-panel@2x.png")
    panel = panel.resize((870, 705), Image.Resampling.LANCZOS)
    canvas.alpha_composite(panel, (120, 177))
    rank = asset("ranking-S@2x.png", (390, 390))
    paste_center(canvas, rank, (1265, 420))

    label(draw, "0128450", (175, 295), 56, WHITE, bold=True)
    label(draw, "ACCURACY", (175, 620), 18, "#aebac4", bold=True)
    label(draw, "98.72%", (175, 666), 42, GREEN, bold=True)
    label(draw, "MAX COMBO", (575, 620), 18, "#aebac4", bold=True)
    label(draw, "428x", (575, 666), 42, CYAN, bold=True)

    stats = [("300", "512", GREEN), ("100", "18", CYAN), ("50", "2", "#ffdc55"), ("MISS", "0", "#ff6a7a")]
    for index, (name, value, colour) in enumerate(stats):
        x = 175 + (index % 2) * 400
        y = 395 + (index // 2) * 105
        label(draw, name, (x, y), 18, colour, bold=True)
        label(draw, value, (x + 175, y + 2), 34, WHITE, anchor="rm", bold=True)
    save_preview(canvas, "results.png", optimize=True)


def overview():
    canvas = Image.new("RGB", SIZE, INK)
    draw = ImageDraw.Draw(canvas)
    previews = [
        ("menu.png", "MENU"),
        ("gameplay-mania.png", "OSU!MANIA"),
        ("gameplay-standard.png", "OSU!STANDARD"),
        ("results.png", "RESULTS"),
    ]
    for index, (filename, title) in enumerate(previews):
        image = Image.open(OUT / filename).convert("RGB").resize((770, 433), Image.Resampling.LANCZOS)
        x = 20 + (index % 2) * 790
        y = 17 + (index // 2) * 450
        canvas.paste(image, (x, y))
        draw.rectangle((x, y + 382, x + 770, y + 433), fill=(2, 9, 15))
        label(draw, title, (x + 24, y + 408), 19, GREEN if index % 2 == 0 else CYAN, anchor="lm", bold=True)
    save_preview(canvas, "overview.jpg", quality=91, optimize=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    menu_preview()
    gameplay_preview()
    mania_preview()
    results_preview()
    overview()
    print(f"Generated showcase in {OUT}")


if __name__ == "__main__":
    main()
