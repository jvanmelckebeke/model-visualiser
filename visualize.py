import os

from keras.models import load_model

from visualizer.backend.diagram import Diagram
from visualizer.backend.document import Document
from visualizer.backend.misc.position import Position
from visualizer.layers.operation.operation import OperationLayer
from visualizer.layers.trainable.trainable import TrainableLayer
from visualizer.layers.utility.utility import UtilityLayer
from visualizer.util.config import Config
from visualizer.util.const import UTILITY_LAYER_TYPES, OPERATION_LAYER_TYPES
from visualizer.util.tools import get_trainable_layer_output_layers


def create_pdf(document: Document):
    with open('generated_graph.tex', 'w') as f:
        f.write(document.generate_code())

    exit_code = os.system(
        'pdflatex -file-line-error -interaction=nonstopmode -synctex=1 -output-format=pdf -output-directory=out '
        'generated_graph.tex')
    if exit_code != 0:
        raise Exception("Error while generating pdf")


def create_diagram_layers(model):
    _layers = []
    for layer in model.layers:
        layer_type = layer.__class__.__name__

        if layer_type in UTILITY_LAYER_TYPES:
            _layers.append(UtilityLayer(layer))
        elif layer_type in OPERATION_LAYER_TYPES:
            _layers.append(OperationLayer(layer))
        else:
            _layers.append(TrainableLayer(layer))

    return _layers


def create_graph(model):
    adjacency_list = {}
    for _layer in model.layers:
        if _layer.__class__.__name__ in UTILITY_LAYER_TYPES:
            continue
        adjacency_list[_layer.name] = [v.name for v in get_trainable_layer_output_layers(_layer)]

    return nx.from_dict_of_lists(adjacency_list)


model = load_model("model.h5")
graph = create_graph(model)

document = Document()
diagram = Diagram()
document.add_styles(Config.load_styles())

diagram_layers = create_diagram_layers(model)

dot_args = Config.load_dot_args()

pos = nx.nx_agraph.graphviz_layout(graph, prog='dot', args=dot_args)

print(pos)
scale_factor = 20
dx, dy = 0, 0
for layer in diagram_layers:
    if layer.type in UTILITY_LAYER_TYPES:
        continue

    x = pos[layer.name][0]
    y = pos[layer.name][1]

    x /= scale_factor
    y /= scale_factor

    y += dy

    diagram.add_node(layer.create_node(Position(x, y)))
    if layer.type == 'Dropout':
        continue
    diagram.add_edges(layer.create_edges())

document.add_element(diagram)

model.summary(line_length=222)
create_pdf(document)
