def hex_to_rgb(value):
    value = value.lstrip('#')
    rgb_as_int = tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))
    rgb_as_float = tuple([float(x) / 255 for x in rgb_as_int])
    return rgb_as_float


LAYER_RECTANGLE_WIDTH = 850
LAYER_RECTANGLE_HEIGHT = 75
LAYER_RECTANGLE_MARGIN = 25

LAYER_SHAPE_HEIGHT = 50

SIDE_SPACE = 50

MAX_VIEWABLE_NEURONS_COLS = 10
MAX_VIEWABLE_NEURONS_ROWS = 3

DEFAULT_COLORS = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
                  "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"]
DEFAULT_COLORS_RGB = [hex_to_rgb(color) for color in DEFAULT_COLORS]
COLOR_BLUE = DEFAULT_COLORS_RGB[0]
COLOR_ORANGE = DEFAULT_COLORS_RGB[1]
COLOR_WHITESMOKE = (0.96, 0.96, 0.96)  # F5F5F5

ARROW_COLOR = (0.5, 0.5, 0.5)
ARROW_SIZE = 5

DEFAULT_FONT = "DejaVu Math TeX Gyre"