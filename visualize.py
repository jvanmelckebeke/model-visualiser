import matplotlib.pyplot as plt
import json

from PIL import Image, ImageDraw

from const import IMAGE_WIDTH
from layers.dropouts.dropout_layer import DropoutLayer
from layers.dropouts.spatialdropout1d_layer import SpatialDropout1DLayer
from layers.layer_representation import BasicLayer
from layers.dropouts.spatialdropout2d_layer import SpatialDropout2DLayer

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
    elif layer_type == "SpatialDropout2D":
        draw_layers.append(SpatialDropout2DLayer(layer))
    elif layer_type == 'SpatialDropout1D':
        draw_layers.append(SpatialDropout1DLayer(layer))
    else:
        draw_layers.append(BasicLayer(layer))

total_height = 0
for layer in draw_layers:
    total_height += layer.get_height()

with Image.new('RGBA', (IMAGE_WIDTH, total_height), color=(1, 1, 1, 1)) as im:
    ctx = ImageDraw.Draw(im)
    current_y = 0
    for layer in draw_layers:
        current_y = layer.draw_layer(ctx, current_y)

    plt.figure(figsize=(22, 25))
    plt.imshow(im)
    plt.axis('off')
    plt.grid(False)
    plt.tight_layout()
    plt.show()
