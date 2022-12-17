from typing import Literal
import seaborn as sns


def hex_to_rgb(value):
    value = value.lstrip('#')
    rgb_as_int = tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))
    return rgb_as_int


def float_tuple_to_int_tuple(float_tuple):
    return tuple(int(x*255) for x in float_tuple)


IMAGE_WIDTH = 1300

LAYER_RECTANGLE_WIDTH = 850
LAYER_RECTANGLE_HEIGHT = 75
LAYER_RECTANGLE_MARGIN = 25

LAYER_SHAPE_HEIGHT = 50

SIDE_SPACE = 50

MAX_VIEWABLE_NEURONS_COLS = 10
MAX_VIEWABLE_NEURONS_ROWS = 3
MAX_VIEWABLE_CHANNELS = 4

DEFAULT_COLORS = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
                  "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"]
DEFAULT_CHANNEL_COLORS = [float_tuple_to_int_tuple(c) for c in
                          sns.light_palette("#79C", MAX_VIEWABLE_CHANNELS + 2)[1:-1]][::-1]
DEFAULT_COLORS_RGB = [hex_to_rgb(color) for color in DEFAULT_COLORS]
COLOR_BLUE = DEFAULT_COLORS_RGB[0]
COLOR_ORANGE = DEFAULT_COLORS_RGB[1]
COLOR_WHITESMOKE = hex_to_rgb("#F5F5F5")

ARROW_COLOR = hex_to_rgb("#808080")
ARROW_SIZE = 5

DEFAULT_FONT = "/usr/share/fonts/TTF/DejaVuMathTeXGyre.ttf"
BOLD_FONT = "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"

TH_COLOR = (int, int, int)
TH_ANCHOR = Literal[
    "la", "lt", 'lm', 'ls', 'lb', 'ld',
    'ma', 'mt', 'mm', 'ms', 'mb', 'md',
    'ra', 'rt', 'rm', 'rs', 'rb', 'rd',
    'sa', 'st', 'sm', 'ss', 'sb', 'sd',
]
