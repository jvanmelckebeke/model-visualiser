import cairo
import matplotlib.pyplot as plt
import json

from draw_layers import draw_dropout_layer, draw_fallback_layer
from tools import surface_to_npim

surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1200, 3000)
ctx = cairo.Context(surface)

ctx.scale(1, 1)
ctx.set_source_rgb(1, 1, 1)
ctx.paint()

ctx.set_line_width(1)

with open("model.json") as f:
    model = json.load(f)

x, y = 0, 0

for layer in model:
    layer_name = layer['name']
    layer_type = layer['type']
    layer_input_shape = layer['input_shape']
    layer_output_shape = layer['output_shape']
    layer_config = layer['config']

    if layer_type == "Bidirectional":
        inner_layer_type = layer_config['layer']['class_name']
        layer_type = f"{layer_type}({inner_layer_type})"

    if layer_type == "Dropout":
        x, y = draw_dropout_layer(ctx, layer, x, y)
    else:
        x, y = draw_fallback_layer(ctx, layer, x, y)

# make surface fit to drawing
# surface.
plt.figure(figsize=(12, 25))
plt.imshow(surface_to_npim(surface))
plt.axis('off')
plt.grid(False)
plt.tight_layout()
plt.show()
