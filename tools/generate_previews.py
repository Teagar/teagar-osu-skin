#!/usr/bin/env python3
"""Generate README showcase mockups from the skin's own assets."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "showcase"
SIZE = (1600, 900)
CYAN = "#00baff"
GREEN = "#00ff90"
INK = "#071018"
WHITE = "#f4f8fb"


def font(size: int, bold: bool = False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(f"/usr/share/fonts/TTF/{name}", size)


def asset(name: str, size=None):
    image = Image.open(ROOT / name).convert("RGBA")
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
    image = cover(Image.open(ROOT / "menu-background.jpg").convert("RGB"))
    image = image.filter(ImageFilter.GaussianBlur(blur))
    image = ImageEnhance.Brightness(image).enhance(darkness).convert("RGBA")
    image.alpha_composite(Image.new("RGBA", SIZE, (2, 8, 14, 55)))
    return image


def paste_center(canvas, image, center):
    canvas.alpha_composite(
        image, (round(center[0] - image.width / 2), round(center[1] - image.height / 2))
    )


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


def header(canvas, section, subtitle):
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((55, 45, 485, 142), 16, fill=(4, 12, 20, 220), outline=CYAN, width=2)
    label(draw, "TEAGAR'S 2.0", (82, 73), 31, GREEN, bold=True)
    label(draw, section.upper(), (82, 113), 18, WHITE, bold=True)
    label(draw, subtitle, (1540, 70), 18, "#b7c3cd", anchor="ra")
    draw.line((55, 162, 1545, 162), fill=(0, 186, 255, 110), width=2)


def menu_preview():
    canvas = background(2, 0.7)
    draw = ImageDraw.Draw(canvas)
    canvas.alpha_composite(Image.new("RGBA", SIZE, (0, 8, 14, 85)))
    header(canvas, "Main menu", "blueberry backdrop • cyan + neon green")

    draw.ellipse((160, 230, 610, 680), fill=(1, 10, 17, 225), outline=CYAN, width=8)
    draw.ellipse((188, 258, 582, 652), outline=GREEN, width=3)
    label(draw, "osu!", (385, 430), 116, WHITE, anchor="mm", bold=True)
    label(draw, "TEAGAR", (385, 545), 25, GREEN, anchor="mm", bold=True)

    menu_asset = asset("menu-button-background@2x.png")
    menu_asset = menu_asset.resize((720, 108), Image.Resampling.LANCZOS)
    for index, (name, accent) in enumerate(
        [("PLAY", GREEN), ("EDIT", CYAN), ("OPTIONS", "#ffffff"), ("EXIT", "#8b99a5")]
    ):
        y = 262 + index * 122
        canvas.alpha_composite(menu_asset, (720, y))
        draw.rectangle((720, y, 728, y + 108), fill=accent)
        label(draw, name, (770, y + 54), 35, accent, anchor="lm", bold=True)
        label(draw, ["Choose a beatmap", "Create and refine", "Tune your game", "See you next time"][index],
              (1010, y + 56), 18, "#aebac4", anchor="lm")

    cursor = asset("cursor@2x.png", (94, 94))
    paste_center(canvas, cursor, (1345, 350))
    label(draw, "CUSTOM SKIN", (1515, 820), 20, GREEN, anchor="ra", bold=True)
    canvas.save(OUT / "menu.png", optimize=True)


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
    canvas = background(12, 0.26)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle((125, 185, 1475, 845), 18, fill=(1, 8, 14, 145), outline=(255, 255, 255, 28), width=2)
    header(canvas, "osu!standard", "gameplay mockup • Focus preset")

    points = [(420, 610), (650, 460), (900, 555), (1160, 365)]
    for first, second in zip(points, points[1:]):
        draw.line((first, second), fill=(255, 255, 255, 80), width=7)
        draw.line((first, second), fill=(0, 186, 255, 125), width=3)
    for i, point in enumerate(points, 1):
        hit_object(canvas, point, i, 1.0 if i < 4 else 0.9, approach=i in (1, 4))

    cursor = asset("cursor@2x.png", (104, 104))
    paste_center(canvas, cursor, (704, 500))
    for radius, alpha in [(55, 100), (76, 55), (98, 25)]:
        draw.ellipse((704-radius, 500-radius, 704+radius, 500+radius), outline=(0, 186, 255, alpha), width=4)

    draw.rounded_rectangle((128, 198, 500, 262), 10, fill=(1, 8, 14, 210))
    label(draw, "00128450", (155, 230), 31, WHITE, anchor="lm", bold=True)
    label(draw, "98.72%", (1448, 226), 29, GREEN, anchor="rm", bold=True)
    label(draw, "127x", (177, 793), 43, CYAN, bold=True)
    draw.rounded_rectangle((520, 808, 1080, 824), 8, fill=(255, 255, 255, 40))
    draw.rounded_rectangle((650, 808, 1015, 824), 8, fill=CYAN)
    label(draw, "STANDARD", (1445, 802), 18, "#aebac4", anchor="ra", bold=True)
    canvas.save(OUT / "gameplay-standard.png", optimize=True)


def mania_preview():
    canvas = background(12, 0.23)
    draw = ImageDraw.Draw(canvas)
    header(canvas, "osu!mania", "4K gameplay mockup • configured for 1–7 keys")

    left, top, right, bottom = 470, 178, 1130, 845
    draw.rectangle((left, top, right, bottom), fill=(0, 0, 0, 215), outline=CYAN, width=2)
    lane_width = (right - left) // 4
    for i in range(1, 4):
        x = left + i * lane_width
        draw.line((x, top, x, bottom), fill=(255, 255, 255, 40), width=2)
    draw.rectangle((left, 785, right, 795), fill=GREEN)
    draw.rectangle((left, 795, right, bottom), fill=(0, 186, 255, 45))

    note_files = ["mania-note1.png", "mania-note2.png", "mania-note2.png", "mania-note1.png"]
    positions = [(0, 350), (1, 265), (2, 490), (3, 315), (1, 610), (3, 665), (0, 560)]
    for lane, y in positions:
        note = asset(note_files[lane]).resize((lane_width - 20, 42), Image.Resampling.LANCZOS)
        canvas.alpha_composite(note, (left + lane * lane_width + 10, y))
    for lane in range(4):
        key_color = CYAN if lane in (1, 2) else WHITE
        draw.rounded_rectangle(
            (left + lane * lane_width + 9, 803, left + (lane + 1) * lane_width - 9, 836),
            5,
            fill=key_color,
        )

    label(draw, "SCORE", (190, 300), 18, "#aebac4", bold=True)
    label(draw, "0247186", (190, 338), 43, WHITE, bold=True)
    label(draw, "COMBO", (190, 450), 18, "#aebac4", bold=True)
    label(draw, "348x", (190, 493), 48, CYAN, bold=True)
    label(draw, "300", (1305, 430), 75, GREEN, anchor="mm", bold=True)
    label(draw, "99.14%", (1305, 505), 28, WHITE, anchor="mm", bold=True)
    label(draw, "4 KEYS", (1305, 650), 23, CYAN, anchor="mm", bold=True)
    canvas.save(OUT / "gameplay-mania.png", optimize=True)


def results_preview():
    canvas = background(8, 0.35)
    draw = ImageDraw.Draw(canvas)
    header(canvas, "Results", "ranking screen mockup • custom grades and counters")

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
    canvas.save(OUT / "results.png", optimize=True)


def overview():
    canvas = Image.new("RGB", SIZE, INK)
    draw = ImageDraw.Draw(canvas)
    previews = [
        ("menu.png", "MENU"),
        ("gameplay-standard.png", "OSU!STANDARD"),
        ("gameplay-mania.png", "OSU!MANIA"),
        ("results.png", "RESULTS"),
    ]
    for index, (filename, title) in enumerate(previews):
        image = Image.open(OUT / filename).convert("RGB").resize((770, 433), Image.Resampling.LANCZOS)
        x = 20 + (index % 2) * 790
        y = 17 + (index // 2) * 450
        canvas.paste(image, (x, y))
        draw.rectangle((x, y + 382, x + 770, y + 433), fill=(2, 9, 15))
        label(draw, title, (x + 24, y + 408), 19, GREEN if index % 2 == 0 else CYAN, anchor="lm", bold=True)
    canvas.save(OUT / "overview.jpg", quality=91, optimize=True)


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
