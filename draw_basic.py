import math
from typing import Literal

from PIL import ImageDraw, ImageFont, Image

from const import DEFAULT_FONT, BOLD_FONT, TH_COLOR, TH_ANCHOR


def draw_rectangle(ctx: ImageDraw,
                   x: int, y: int,
                   width: int, height: int,
                   fill_color: TH_COLOR = (255, 255, 255),
                   stroke_color: TH_COLOR = (0, 0, 0),
                   stroke_width: int = 1):
    x1 = int(x)
    y1 = int(y)
    x2 = int(x + width)
    y2 = int(y + height)
    ctx.rectangle((x1, y1, x2, y2), outline=stroke_color, fill=fill_color, width=stroke_width)


def draw_text(ctx: ImageDraw,
              x: int,
              y: int,
              text: str,
              anchor: TH_ANCHOR = 'lm',
              color: TH_COLOR = (0, 0, 0),
              font_size: int = 12,
              bold: bool = False):
    if bold:
        fnt = ImageFont.truetype(BOLD_FONT, size=font_size)
    else:
        fnt = ImageFont.truetype(DEFAULT_FONT, size=font_size)

    ctx.text((x, y), text, font=fnt, fill=color, anchor=anchor)


def draw_arrow(ctx: ImageDraw,
               x1: int, y1: int,
               x2: int, y2: int,
               arrow: bool = True,
               arrow_size=10,
               color: TH_COLOR = (0, 0, 0),
               stroke_width=1):
    ctx.line((x1, y1, x2, y2), fill=color, width=stroke_width)
    if arrow:
        # Now work out the arrowhead
        # = it will be a triangle with one vertex at ptB
        # - it will extend 8 pixels either side of the line
        # Now we can work out the x,y coordinates of the bottom of the arrowhead triangle
        xb = 0.95 * (x2 - x1) + x1
        yb = 0.95 * (y2 - y1) + y1

        # Work out the other two vertices of the triangle
        # Check if line is vertical
        if x1 == x2:
            vtx1 = (xb - 5, yb)
            vtx2 = (xb + 5, yb)
        # Check if line is horizontal
        elif y1 == y2:
            vtx1 = (xb, yb + 5)
            vtx2 = (xb, yb - 5)
        else:
            alpha = math.atan2(y2 - y1, x2 - x1) - 90 * math.pi / 180
            a = arrow_size * math.cos(alpha)
            b = arrow_size * math.sin(alpha)
            vtx1 = (xb + a, yb + b)
            vtx2 = (xb - a, yb - b)

        ctx.polygon([vtx1, vtx2, (x2, y2)], fill=color)


def draw_annotated_rectangle(ctx: ImageDraw,
                             x: int, y: int,
                             width: int, height: int,
                             label: str,
                             font_size: int = 20,
                             fill_color: TH_COLOR = (240, 240, 240),
                             stroke_color: TH_COLOR = (0, 0, 0),
                             stroke_width: int = 1,
                             text_color: TH_COLOR = (0, 0, 0)):
    draw_rectangle(ctx, x, y, width, height, fill_color, stroke_color, stroke_width)

    font = ImageFont.truetype(BOLD_FONT, 20)
    img_txt = Image.new('L', font.getsize(label))
    draw_txt = ImageDraw.Draw(img_txt)
    draw_txt.text((0, 0), label, font=font, fill=255)

    t = img_txt.rotate(-90, expand=True)
    # scale the image such that the text fits in the rectangle
    if t.size[1] > height - 10:
        scale = (height - 10) / t.size[1]
        t = t.resize((int(t.size[0] * scale), int(t.size[1] * scale)), Image.ANTIALIAS)

    offset = (x + width - t.size[0], y + (height - t.size[1]) // 2)

    ctx.bitmap((x + width - t.size[0], y + 5), t, fill=text_color)
