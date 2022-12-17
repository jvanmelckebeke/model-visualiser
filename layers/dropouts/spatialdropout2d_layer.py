from const import LAYER_RECTANGLE_WIDTH, SIDE_SPACE, LAYER_RECTANGLE_MARGIN
from layers.dropouts.dropout_layer import DropoutLayer


class SpatialDropout2DLayer(DropoutLayer):
    def __init__(self, layer):
        super().__init__(layer)
        self.layer_output_dim = 3  # for a SpatialDropout2D layer, the output is always 3D
        self.dropout_rate = layer['config']['rate']

    def draw_layer(self, ctx, sy=0) -> int:
        sx = 0
        end_y = self._draw_three_dimensional(ctx, sx, sy)

        self._draw_layer_side_info(ctx, sx + LAYER_RECTANGLE_WIDTH + SIDE_SPACE
                                   , sy + LAYER_RECTANGLE_MARGIN + 10)
        return end_y + LAYER_RECTANGLE_MARGIN * 1
