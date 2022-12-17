from PIL import ImageDraw, Image

from const import LAYER_RECTANGLE_WIDTH, LAYER_RECTANGLE_HEIGHT, COLOR_WHITESMOKE, SIDE_SPACE, \
    LAYER_RECTANGLE_MARGIN
from draw_basic import draw_text, draw_rectangle
from tools import process_shape


class BasicLayer:
    def __init__(self, layer):
        self.layer = layer
        self.layer_name = layer['name']
        self.layer_type = layer['type']
        self.layer_input_shape = process_shape(layer['input_shape'])
        self.layer_output_shape = process_shape(layer['output_shape'])
        self.layer_config = layer['config']

    def _draw_layer_side_info(self, ctx, sx, sy):
        draw_text(ctx, sx, sy - 20, f"{self.layer_type}: {self.layer_name}", anchor='lm', color=(0, 0, 0),
                  font_size=18, bold=True)
        draw_text(ctx, sx, sy, f"{self.layer_input_shape} ⟶ {self.layer_output_shape}", anchor='lm', color=(0, 0, 0),
                  font_size=18)

    def draw_layer(self, ctx: ImageDraw, sy=0) -> int:
        x, y = 0, sy
        width, height = LAYER_RECTANGLE_WIDTH, LAYER_RECTANGLE_HEIGHT
        draw_rectangle(ctx, x, y,
                       width=LAYER_RECTANGLE_WIDTH,
                       height=LAYER_RECTANGLE_HEIGHT,
                       fill_color=COLOR_WHITESMOKE)

        text_x = x + width + SIDE_SPACE
        text_y = y + height / 2

        self._draw_layer_side_info(ctx, text_x, text_y)
        total_height = LAYER_RECTANGLE_HEIGHT
        return sy + total_height + LAYER_RECTANGLE_MARGIN

    def get_height(self) -> int:
        with Image.new('RGBA', (1, 1)) as img:
            ctx = ImageDraw.Draw(img)
            return int(self.draw_layer(ctx))


def __repr__(self):
    return f"{self.layer}"


def __str__(self):
    return f"{self.layer}"
