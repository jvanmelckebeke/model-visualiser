import cairo
import matplotlib.pyplot as plt
import json

from layers.dropout_layer import DropoutLayer
from layers.layer_representation import BasicLayer
from tools import surface_to_npim

with open("model.json") as f:
    model = json.load(f)

draw_layers = []

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
        draw_layers.append(DropoutLayer(layer))
    else:
        draw_layers.append(BasicLayer(layer))

total_height = 0
for layer in draw_layers:
    total_height += layer.get_height()

with cairo.ImageSurface(cairo.FORMAT_ARGB32, 1300, total_height) as surface:
    ctx = cairo.Context(surface)
    ctx.set_source_rgb(1, 1, 1)
    ctx.paint()
    y = 0
    for layer in draw_layers:
        y = layer.draw(ctx, sy=y)
    im = surface_to_npim(surface)

plt.figure(figsize=(22, 25))
plt.imshow(im)
plt.axis('off')
plt.grid(False)
plt.tight_layout()
plt.show()
