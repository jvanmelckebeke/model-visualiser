import os

from keras.models import load_model

from layers.operation.operation import OperationLayer
from layers.trainable.trainable import TrainableLayer
from layers.utility.utility import UtilityLayer
from tikz.diagram import Diagram
from tikz.document import Document
from tikz.edges.edge import Edge
from tikz.util.style import TikzStyle
from tools import load_from_config

UTILITY_LAYER_TYPES = load_from_config('layer-types', 'utility', 'items')
OPERATION_LAYER_TYPES = load_from_config('layer-types', 'operation', 'items')

styles = {
    "default_edge":
        TikzStyle("thick",
                  **{
                      "out": -90,
                      "in": 90,
                      "out distance": f"2cm",
                      "in distance": f"2cm",
                  }),
    "default_label": TikzStyle("auto", pos=0.65)
}


def create_pdf(document: Document):
    with open('generated_graph.tex', 'w') as f:
        f.write(document.generate_code())

    exit_code = os.system(
        'pdflatex -file-line-error -interaction=nonstopmode -synctex=1 -output-format=pdf -output-directory=out '
        'generated_graph.tex')
    if exit_code != 0:
        raise Exception("Error while generating pdf")


def get_parent_layer(layer):
    if len(layer.inbound_nodes) == 0:
        return None
    if layer.inbound_nodes:
        layers_in = layer.inbound_nodes[0].inbound_layers
        if isinstance(layers_in, list):
            if len(layers_in) > 0:
                return layers_in[0].name
            return None
        return layers_in.name
    return None


def get_child_layers(layer):
    if len(layer.outbound_nodes) == 0:
        return None

    if layer.outbound_nodes and len(layer.outbound_nodes) > 0:
        children = []
        for node in layer.outbound_nodes:
            layer_out = node.outbound_layer
            children.append(layer_out.name)
        return children
    return None


def get_child_layer_edges(layer):
    if len(layer.outbound_nodes) == 0:
        return []

    if layer.outbound_nodes and len(layer.outbound_nodes) > 0:
        children = []
        for node in layer.outbound_nodes:
            layer_out = node.outbound_layer
            layer_out_type = layer_out.__class__.__name__
            trainable_num = 0
            for weight in layer_out.weights:
                if weight.trainable:
                    trainable_num += weight.shape.num_elements()

            label = format(trainable_num, ',d') if trainable_num > 0 else ''
            if len(layer.outbound_nodes) > 1 or layer_out_type not in UTILITY_LAYER_TYPES:
                children.append(Edge(layer.name, layer_out.name, label=label))
        return children
    return []


model = load_model("model.h5")

parent_map = {}
child_map = {}

layers = []

document = Document()
document.add_styles(styles)

diagram = Diagram()
for layer in model.layers:

    layer_type = layer.__class__.__name__

    if layer_type in UTILITY_LAYER_TYPES:
        layers.append(UtilityLayer(layer))
    elif layer_type in OPERATION_LAYER_TYPES:
        layers.append(OperationLayer(layer))
    else:
        layers.append(TrainableLayer(layer))

for layer in layers:
    document.add_style(layer.get_style_name(), layer.get_style())
    diagram.add_node(layer.create_node())
    diagram.add_edges(layer.create_edges())

document.add_element(diagram)

model.summary(line_length=222)
create_pdf(document)
