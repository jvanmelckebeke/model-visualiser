import os

from visualizer.util.config import Config, StyleConfig, LayerConfig

UTILITY_LAYER_TYPES = LayerConfig.load('layer-types', 'utility', 'items')
OPERATION_LAYER_TYPES = LayerConfig.load('layer-types', 'operation', 'items')

SCALE_Y = float(Config.load('diagram', 'coordinate-system', 'y', 'value'))

FONT_SIZE = 10  # pt
INNER_SEP = int(StyleConfig.load('default-style', 'options', 'inner sep')[:-2])  # remove pt
