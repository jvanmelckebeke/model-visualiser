import math
import random as rnd
import cairo

from constants import LAYER_RECTANGLE_WIDTH, LAYER_RECTANGLE_HEIGHT, COLOR_WHITESMOKE, COLOR_ORANGE, LAYER_SHAPE_HEIGHT, \
    LAYER_RECTANGLE_MARGIN
from draw_basic import draw_annotated_rectangle, draw_text
from tools import process_shape


def draw_fallback_layer(ctx: cairo.Context, layer, sx=0, sy=0):
    x, y = sx, sy
    width, height = LAYER_RECTANGLE_WIDTH, LAYER_RECTANGLE_HEIGHT
    layer_output_shape = process_shape(layer['output_shape'])
    draw_annotated_rectangle(ctx, x, y,
                             width=LAYER_RECTANGLE_WIDTH,
                             height=LAYER_RECTANGLE_HEIGHT,
                             label=layer['type'],
                             fill_color=COLOR_WHITESMOKE)
    draw_annotated_rectangle(ctx, x=x,
                             y=y + height,
                             width=LAYER_RECTANGLE_WIDTH,
                             height=LAYER_SHAPE_HEIGHT,
                             label=f"Output Shape: {layer_output_shape}",
                             fill_color=COLOR_ORANGE)
    ctx.save()

    x = sx + width + 100
    y = sy + height / 2
    draw_text(ctx, x, y, layer['name'], align='left', color=(0, 0, 0), font_size=20)
    ctx.save()
    total_height = LAYER_RECTANGLE_HEIGHT + LAYER_SHAPE_HEIGHT
    return sx, sy + total_height + LAYER_RECTANGLE_MARGIN


def draw_dropout_layer(ctx: cairo.Context, layer, sx=0, sy=0):
    x, y = sx, sy
    width, height = LAYER_RECTANGLE_WIDTH, LAYER_RECTANGLE_HEIGHT
    layer_output_shape = process_shape(layer['output_shape'])
    layer_output_dim = 1 if isinstance(layer_output_shape, int) else len(layer_output_shape)
    draw_annotated_rectangle(ctx, x, y, LAYER_RECTANGLE_WIDTH, LAYER_RECTANGLE_HEIGHT, layer['type'],
                             fill_color=COLOR_WHITESMOKE, align_text_vertical='top')

    if layer_output_dim == 1:
        ctx.move_to(x + 50, y + height / 2)
        num_neurons = min(10, layer_output_shape)
        rate_transparent = layer['config']['rate']
        color_transparent = (0.8, 0.8, 0.8)
        color_opaque = (0.5, 0.5, 0.5)
        circle_radius = 10
        circle_margin = 50

        start_x = LAYER_RECTANGLE_WIDTH / 2 - (
                num_neurons * circle_radius * 2 + (num_neurons - 1) * circle_margin) / 2 + sx

        for i in range(num_neurons):
            if rnd.random() < rate_transparent:
                ctx.set_source_rgb(*color_transparent)
            else:
                ctx.set_source_rgb(*color_opaque)
            ctx.arc(start_x + i * circle_radius * 2 + i * circle_margin, y + height / 2 + 10, circle_radius, 0,
                    2 * math.pi)
            ctx.fill()
            ctx.stroke()
        ctx.save()

    draw_annotated_rectangle(ctx, x, y + height, LAYER_RECTANGLE_WIDTH, LAYER_SHAPE_HEIGHT,
                             f"Output Shape: {layer_output_shape}",
                             fill_color=COLOR_ORANGE)

    ctx.save()

    x = sx + width + 100
    y = sy + height / 2
    draw_text(ctx, x, y, layer['name'], align='left', color=(0, 0, 0), font_size=20)
    ctx.save()
    total_height = LAYER_RECTANGLE_HEIGHT + LAYER_SHAPE_HEIGHT
    return sx, sy + total_height + LAYER_RECTANGLE_MARGIN
