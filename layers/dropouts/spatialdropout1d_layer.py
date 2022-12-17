import numpy as np

from const import LAYER_RECTANGLE_WIDTH, SIDE_SPACE, LAYER_RECTANGLE_MARGIN, LAYER_RECTANGLE_HEIGHT, \
    MAX_VIEWABLE_NEURONS_ROWS, MAX_VIEWABLE_NEURONS_COLS
from layers.dropouts.dropout_layer import DropoutLayer
import random as rnd


class SpatialDropout1DLayer(DropoutLayer):
    def __init__(self, layer):
        super().__init__(layer)
        self.layer_output_dim = 2  # for a SpatialDropout1D layer, the output is always 2D
        self.dropout_rate = layer['config']['rate']
        self.dropout_map = np.ones((MAX_VIEWABLE_NEURONS_ROWS, MAX_VIEWABLE_NEURONS_COLS))

    def _draw_dropout_neurons_row(self, ctx, x, y, num_neurons, color_opaque, color_transparent, circle_radius,
                                  col_margin, row=0):
        for i in range(num_neurons):
            if self.dropout_map[row, i] == 0:
                fill_color = color_transparent
            else:
                fill_color = color_opaque
            ctx.ellipse((x + i * circle_radius * 2 + i * col_margin - circle_radius,
                         y - circle_radius,
                         x + i * circle_radius * 2 + i * col_margin + circle_radius,
                         y + circle_radius), fill=fill_color, outline=fill_color)

    def _draw_dropout_neurons_field(self, ctx, x, y, num_rows, num_cols, color_opaque, color_transparent,
                                    circle_radius, col_margin, row_margin, channel=0):
        for i in range(num_cols):
            if rnd.random() < self.dropout_rate:
                self.dropout_map[:, i] = 0
            else:
                self.dropout_map[:, i] = 1

        super()._draw_dropout_neurons_field(ctx, x, y, num_rows, num_cols, color_opaque, color_transparent,
                                             circle_radius,
                                             col_margin, row_margin)

    def draw_layer(self, ctx, sy=0) -> int:
        sx = 0
        end_y = self._draw_two_dimensional(ctx, sx, sy)

        self._draw_layer_side_info(ctx, sx + LAYER_RECTANGLE_WIDTH + SIDE_SPACE
                                   , sy + LAYER_RECTANGLE_MARGIN + 10)
        return end_y + LAYER_RECTANGLE_MARGIN * 1
