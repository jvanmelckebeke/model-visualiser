import uuid

import keras.layers

from visualizer.util.const import UTILITY_LAYER_TYPES

INDENT_SIZE = 4
INDENT_STR = ' ' * INDENT_SIZE


def str_shape(shape):
    if isinstance(shape, tuple):
        if shape[0] is None:
            return str_shape(shape[1:])
        if len(shape) == 1:
            return str(shape[0])
        return str(shape)
    elif isinstance(shape, list):
        if len(shape) == 1:
            return str_shape(shape[0])
        return str([str_shape(s) for s in shape])
    else:
        return str(shape)


def generate_uuid():
    return str(uuid.uuid4())[:8]


def get_layer_output_layers(layer: keras.layers.Layer):
    outbound_layers = []
    for outbound_node in layer.outbound_nodes:
        outbound_layers.append(outbound_node.outbound_layer)

    return outbound_layers


def get_trainable_layer_output_layers(layer: keras.layers.Layer):
    outbound_layers = []
    for outbound_layer in get_layer_output_layers(layer):
        if outbound_layer.__class__.__name__ in UTILITY_LAYER_TYPES:
            outbound_layers.extend(get_trainable_layer_output_layers(outbound_layer))
        else:
            outbound_layers.append(outbound_layer)
    return outbound_layers


def get_layer_input_layers(layer: keras.layers.Layer):
    inbound_layers = []
    for inbound_node in layer.inbound_nodes:
        if isinstance(inbound_node.inbound_layers, list):
            for inbound_layer in inbound_node.inbound_layers:
                inbound_layers.append(inbound_layer)
        else:
            inbound_layers.append(inbound_node.inbound_layers)

    return inbound_layers
