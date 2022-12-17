import math

from PIL import ImageFont, Image, ImageOps, ImageDraw

from const import LAYER_RECTANGLE_WIDTH, LAYER_RECTANGLE_HEIGHT, MAX_VIEWABLE_NEURONS_COLS, ARROW_SIZE, ARROW_COLOR, \
    SIDE_SPACE, LAYER_RECTANGLE_MARGIN, MAX_VIEWABLE_NEURONS_ROWS, hex_to_rgb, COLOR_BLUE, COLOR_WHITESMOKE, BOLD_FONT, \
    MAX_VIEWABLE_CHANNELS, DEFAULT_CHANNEL_COLORS
from draw_basic import draw_text, draw_arrow, draw_annotated_rectangle, draw_rectangle
from layers.layer_representation import BasicLayer
import random as rnd


class DropoutLayer(BasicLayer):
    def __init__(self, layer):
        super().__init__(layer)
        self.layer_output_dim = 1 if isinstance(self.layer_output_shape, int) else len(self.layer_output_shape)
        self.dropout_rate = layer['config']['rate']

    def _draw_dropout_neurons_row(self, ctx, x, y, num_neurons, color_opaque, color_transparent, circle_radius,
                                  col_margin, row=0):
        for i in range(num_neurons):
            if rnd.random() < self.dropout_rate:
                fill_color = color_transparent
            else:
                fill_color = color_opaque
            ctx.ellipse((x + i * circle_radius * 2 + i * col_margin - circle_radius,
                         y - circle_radius,
                         x + i * circle_radius * 2 + i * col_margin + circle_radius,
                         y + circle_radius), fill=fill_color, outline=fill_color)

    def _draw_dropout_neurons_field(self, ctx, x, y, num_rows, num_cols, color_opaque, color_transparent,
                                    circle_radius, col_margin, row_margin, channel=0):
        for i in range(num_rows):
            row_y = y + LAYER_RECTANGLE_HEIGHT / 2 + i * circle_radius * 2 + (i - 2) * row_margin + 10
            self._draw_dropout_neurons_row(ctx, x, row_y, num_cols, color_opaque, color_transparent,
                                           circle_radius, col_margin, row=i)

    def _draw_layer_side_info(self, ctx, sx, sy):
        super()._draw_layer_side_info(ctx, sx, sy)
        draw_text(ctx, sx, sy + 20, f"Rate: {self.dropout_rate}", anchor='lm', color=(0, 0, 0), font_size=18)

    def _draw_one_dimensional(self, ctx, sx, sy):

        height = LAYER_RECTANGLE_HEIGHT

        num_neurons = min(MAX_VIEWABLE_NEURONS_COLS, self.layer_output_shape)

        color_transparent = (204, 204, 204)
        color_opaque = COLOR_BLUE

        circle_radius = 10
        circle_margin = 50

        start_x = LAYER_RECTANGLE_WIDTH / 2 - (
                num_neurons * circle_radius * 2 + (num_neurons - 1) * circle_margin) / 2 + sx

        draw_annotated_rectangle(ctx, sx, sy, LAYER_RECTANGLE_WIDTH, height, self.layer_type, font_size=18)

        self._draw_dropout_neurons_row(ctx, start_x,
                                       sy + LAYER_RECTANGLE_HEIGHT / 2,
                                       num_neurons, color_opaque, color_transparent,
                                       circle_radius, circle_margin)
        return sy + height / 2 + 50

    def _draw_two_dimensional(self, ctx: ImageDraw, sx, sy):
        y = sy

        num_neurons = min(MAX_VIEWABLE_NEURONS_COLS, self.layer_output_shape[1])
        num_rows = min(MAX_VIEWABLE_NEURONS_ROWS, self.layer_output_shape[0])

        color_transparent = (204, 204, 204)
        color_opaque = COLOR_BLUE

        circle_radius = 10
        circle_col_margin = 50
        circle_row_margin = 10

        start_x = LAYER_RECTANGLE_WIDTH / 2 - (
                num_neurons * circle_radius * 2 + (num_neurons - 1) * circle_col_margin) / 2 + sx

        total_height = num_rows * circle_radius * 2 + num_rows * circle_row_margin + 20

        draw_annotated_rectangle(ctx, sx, sy, LAYER_RECTANGLE_WIDTH, total_height, self.layer_type, font_size=18)

        self._draw_dropout_neurons_field(ctx, start_x, y, num_rows, num_neurons, color_opaque, color_transparent,
                                         circle_radius, circle_col_margin, circle_row_margin)

        return sy + total_height

    def _draw_three_dimensional(self, ctx: ImageDraw, sx, sy):
        num_neurons = min(MAX_VIEWABLE_NEURONS_COLS, self.layer_output_shape[1])
        num_rows = min(MAX_VIEWABLE_NEURONS_ROWS, self.layer_output_shape[0])
        num_channels = min(MAX_VIEWABLE_CHANNELS, self.layer_output_shape[2])

        color_transparent = (204, 204, 204)
        color_opaque = COLOR_BLUE

        circle_radius = 10
        circle_col_margin = 25
        circle_row_margin = 10
        channel_margin = 10
        channel_rectangle_margin = 20

        channel_rectangle_width = num_neurons * circle_radius * 2 + (num_neurons - 1) * circle_col_margin + 40
        channel_rectangle_height = num_rows * circle_radius * 2 + (num_rows - 1) * circle_row_margin + 40

        total_height = channel_rectangle_height + channel_margin + channel_rectangle_margin * (
                num_channels - 1)

        draw_annotated_rectangle(ctx, sx, sy, LAYER_RECTANGLE_WIDTH, total_height, self.layer_type, font_size=18)

        for channel in range(num_channels):
            ch_x = sx + LAYER_RECTANGLE_WIDTH / 2 - channel_rectangle_width / 2 - channel * channel_margin
            ch_y = sy + LAYER_RECTANGLE_HEIGHT / 2 - channel_rectangle_height / 2 - channel * channel_margin + channel_rectangle_margin * num_channels
            ch_color = DEFAULT_CHANNEL_COLORS[channel]

            draw_rectangle(ctx, ch_x, ch_y, channel_rectangle_width, channel_rectangle_height, fill_color=ch_color,
                           stroke_color=ch_color)
            if channel == num_channels - 1:
                self._draw_dropout_neurons_field(ctx, ch_x + channel_margin * 2, ch_y, num_rows, num_neurons, color_opaque,
                                                 color_transparent, circle_radius, circle_col_margin,
                                                 circle_row_margin)
            # for i in range(num_rows):
            #     row_y = ch_y + 10 + i * circle_radius * 2 + (i - 2) * circle_row_margin
            #     self.__draw_dropout_neurons_row(ctx, start_x, row_y, num_neurons, color_opaque, color_transparent,
            #                                     circle_radius, circle_col_margin)

        return sy + total_height

    def draw_layer(self, ctx, sy=0) -> int:
        sx = 0
        if self.layer_output_dim == 1:
            end_y = self._draw_one_dimensional(ctx, sx, sy)
        elif self.layer_output_dim == 2:
            end_y = self._draw_two_dimensional(ctx, sx, sy)
        else:
            end_y = self._draw_three_dimensional(ctx, sx, sy)

        self._draw_layer_side_info(ctx, sx + LAYER_RECTANGLE_WIDTH + SIDE_SPACE
                                   , sy + LAYER_RECTANGLE_MARGIN + 10)
        return end_y + LAYER_RECTANGLE_MARGIN * 1
