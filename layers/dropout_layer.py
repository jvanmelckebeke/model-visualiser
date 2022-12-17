import math

from constants import LAYER_RECTANGLE_WIDTH, LAYER_RECTANGLE_HEIGHT, MAX_VIEWABLE_NEURONS_COLS, ARROW_SIZE, ARROW_COLOR, \
    SIDE_SPACE, LAYER_RECTANGLE_MARGIN, MAX_VIEWABLE_NEURONS_ROWS
from draw_basic import draw_text, draw_arrow
from layers.layer_representation import BasicLayer
import random as rnd


class DropoutLayer(BasicLayer):
    def __init__(self, layer):
        super().__init__(layer)
        self.layer_output_dim = 1 if isinstance(self.layer_output_shape, int) else len(self.layer_output_shape)
        self.dropout_rate = layer['config']['rate']

    def _draw_layer_side_info(self, ctx, sx, sy):
        super()._draw_layer_side_info(ctx, sx, sy)
        draw_text(ctx, sx, sy + 20, f"Rate: {self.dropout_rate}", align='left', color=(0, 0, 0), font_size=18)
        ctx.save()

    def __draw_one_dimensional(self, ctx, sx, sy):
        height = LAYER_RECTANGLE_HEIGHT
        ctx.move_to(sx + 50, sy + height / 2)
        num_neurons = min(MAX_VIEWABLE_NEURONS_COLS, self.layer_output_shape)

        color_transparent = (0.8, 0.8, 0.8)
        color_opaque = (0.5, 0.5, 0.5)

        circle_radius = 10
        circle_margin = 50

        start_x = LAYER_RECTANGLE_WIDTH / 2 - (
                num_neurons * circle_radius * 2 + (num_neurons - 1) * circle_margin) / 2 + sx

        for i in range(num_neurons):
            draw_arrow(ctx,
                       start_x + i * circle_radius * 2 + i * circle_margin,
                       sy + height / 2 - circle_radius - 50,
                       start_x + i * circle_radius * 2 + i * circle_margin,
                       sy + height / 2 - circle_radius,
                       arrow=True,
                       arrow_size=ARROW_SIZE,
                       head_orientation='down',
                       color=ARROW_COLOR)

            if rnd.random() < self.dropout_rate:
                ctx.set_source_rgb(*color_transparent)
            else:
                ctx.set_source_rgb(*color_opaque)
            ctx.arc(start_x + i * circle_radius * 2 + i * circle_margin,
                    sy + height / 2,
                    circle_radius,
                    0,
                    2 * math.pi)
            ctx.fill()
            draw_arrow(ctx, start_x + i * circle_radius * 2 + i * circle_margin,
                       sy + height / 2 + circle_radius,
                       start_x + i * circle_radius * 2 + i * circle_margin,
                       sy + height / 2 + 50,
                       arrow=False,
                       arrow_size=ARROW_SIZE,
                       head_orientation='down',
                       color=ARROW_COLOR)
        ctx.save()

        return sy + height / 2 + 50

    def __draw_two_dimensional(self, ctx, sx, sy):
        height = LAYER_RECTANGLE_HEIGHT
        y = sy
        x = sx
        ctx.move_to(x + 50, sy + LAYER_RECTANGLE_HEIGHT / 2)
        num_neurons = min(MAX_VIEWABLE_NEURONS_COLS, self.layer_output_shape[1])
        num_rows = min(MAX_VIEWABLE_NEURONS_ROWS, self.layer_output_shape[0])

        color_transparent = (0.8, 0.8, 0.8)
        color_opaque = (0.5, 0.5, 0.5)

        circle_radius = 10
        circle_col_margin = 50
        circle_row_margin = 10

        start_x = LAYER_RECTANGLE_WIDTH / 2 - (
                num_neurons * circle_radius * 2 + (num_neurons - 1) * circle_col_margin) / 2 + sx

        for i in range(num_rows):
            row_y = sy + height / 2 + i * circle_radius * 2 + (i - 2) * circle_row_margin
            for j in range(num_neurons):

                if rnd.random() < self.dropout_rate:
                    ctx.set_source_rgb(*color_transparent)
                else:
                    ctx.set_source_rgb(*color_opaque)
                ctx.arc(start_x + j * circle_radius * 2 + j * circle_col_margin,
                        row_y,
                        circle_radius,
                        0,
                        2 * math.pi)
                ctx.fill()
                draw_arrow(ctx, start_x + j * circle_radius * 2 + j * circle_col_margin,
                           y + height / 2 + circle_radius,
                           start_x + j * circle_radius * 2 + j * circle_col_margin,
                           y + height / 2 + 50,
                           arrow=False,
                           arrow_size=ARROW_SIZE,
                           head_orientation='down',
                           color=ARROW_COLOR)
        ctx.save()
        return y + height / 2 + 50 + circle_radius * 2 * num_rows + (num_rows - 1) * circle_row_margin

    def draw(self, ctx, sx=0, sy=0):
        x, y = sx, sy

        width, height = LAYER_RECTANGLE_WIDTH, LAYER_RECTANGLE_HEIGHT

        if self.layer_output_dim == 1:
            y = self.__draw_one_dimensional(ctx, sx, sy)
        elif self.layer_output_dim == 2:
            y = self.__draw_two_dimensional(ctx, sx, sy)

        x = sx + width + SIDE_SPACE
        y = sy + height / 2
        self._draw_layer_side_info(ctx, x, y)
        total_height = LAYER_RECTANGLE_HEIGHT
        return sy + total_height + LAYER_RECTANGLE_MARGIN
