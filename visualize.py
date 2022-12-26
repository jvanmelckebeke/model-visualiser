import os

from tensorflow.keras.models import load_model

from tikz.diagram import Diagram
from tikz.document import Document
from tikz.base import TikzOptions
from tikz.edges.edge import Edge
from tikz.nodes.base_node import Node
from tikz.nodes.operation import OperationNode
from tikz.nodes.utility import UtilityNode
from tikz.nodes.trainable import TrainableNode
from tikz.style import TikzStyle

UTILITY_LAYER_TYPES = ['Dropout', 'BatchNormalization', 'SpatialDropout2D', 'SpatialDropout3D', 'AlphaDropout',
                       'SpatialDropout1D', 'GaussianDropout', 'GaussianNoise', 'ActivityRegularization', 'Masking']

OPERATION_LAYER_TYPES = ['Add', 'Flatten', 'Concatenate', 'Average', 'Maximum', 'Minimum', 'Multiply', 'Subtract']

node_distance = 2

styles = {
    "trainable_node":
        TikzStyle("rectangle split",
                  "rectangle split ignore empty parts",
                  "very thick",
                  **{
                      "rectangle split parts": 2,
                      "draw": "blue!60",
                      "fill": "blue!5",
                      "minimum width": "{width(\"Batch Normalisation\") + 8pt}",
                      "node distance": node_distance,
                      "outer sep": "0pt"
                  }),
    "utility_node":
        TikzStyle("rectangle split",
                  "rectangle split ignore empty parts",
                  "very thick",
                  **{
                      "rectangle split parts": 2,
                      "draw": "gray!60",
                      "fill": "gray!5",
                      "minimum width": "{width(\"Batch Normalisation\") + 8pt}",
                      "node distance": node_distance,
                      "outer sep": "0pt"
                  }),
    "operation_node":
        TikzStyle("rectangle split",
                  "rectangle split ignore empty parts",
                  "very thick",
                  **{
                      "rectangle split parts": 2,
                      "draw": "violet!60",
                      "fill": "violet!5",
                      "minimum width": "{width(\"Batch Normalisation\") + 8pt}",
                      "node distance": node_distance,
                      "outer sep": "0pt"
                  }),
    "default_edge":
        TikzStyle("thick",
                  **{
                      "out": -90,
                      "in": 90,
                      "out distance": f"{node_distance}cm",
                      "in distance": f"{node_distance}cm",
                  }),
    "default_label": TikzStyle("midway", "auto")
}

TEXT_AFTER = r"\end{tikzpicture}" \
             r"\end{document}"


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

document = Document()
document.add_styles(styles)

diagram = Diagram()
for layer in model.layers:

    layer_type = layer.__class__.__name__

    parent_layer = get_parent_layer(layer)
    child_layers = get_child_layers(layer)

    diagram.add_edges(get_child_layer_edges(layer))

    below_of_layer = parent_layer
    right_of_layer = None
    left_of_layer = None

    if parent_layer:
        if parent_layer not in parent_map:
            parent_map[parent_layer] = [layer.name]
        else:
            parent_map[parent_layer].append(layer.name)

            num_neighbours = len(parent_map[parent_layer])
            if num_neighbours < 3:
                right_of_layer = parent_map[parent_layer][0]
            elif num_neighbours % 2 == 0:
                right_of_layer = parent_map[parent_layer][-3]
            else:
                left_of_layer = parent_map[parent_layer][-3]

    if layer_type in UTILITY_LAYER_TYPES:
        diagram.add_node(UtilityNode(layer.name, layer,
                                     below_of=below_of_layer,
                                     right_of=right_of_layer,
                                     left_of=left_of_layer))
    elif layer_type in OPERATION_LAYER_TYPES:
        diagram.add_node(OperationNode(layer.name, layer,
                                       below_of=below_of_layer,
                                       right_of=right_of_layer,
                                       left_of=left_of_layer))
    else:
        diagram.add_node(TrainableNode(layer.name, layer,
                                       below_of=below_of_layer,
                                       right_of=right_of_layer,
                                       left_of=left_of_layer))

document.add_elements(diagram.get_elements())

model.summary(line_length=222)
create_pdf(document)
