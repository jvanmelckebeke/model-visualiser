from keraspoj.util.config import Config, StyleConfig

SCALE_Y = float(Config.load('diagram', 'coordinate-system', 'y', 'value'))

FONT_SIZE = 6  # pt
INNER_SEP = int(StyleConfig.load('default-style', 'options', 'inner sep')[:-2])  # remove pt


COLOR_MAP = Config.load_colormap()