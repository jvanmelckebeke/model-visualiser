from visualizer.util.config import Config

UTILITY_LAYER_TYPES = Config.load('layer-types', 'utility', 'items')
OPERATION_LAYER_TYPES = Config.load('layer-types', 'operation', 'items')

SCALE_Y = float(Config.load('diagram', 'coordinate-system', 'y', 'value'))

FONT_SIZE = 10  # pt
INNER_SEP = int(Config.load('default-style', 'options', 'inner sep')[:-2])  # remove pt
