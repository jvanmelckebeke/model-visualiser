import json

import keras.applications
from keras.models import load_model

from visualizer.backend.diagram import Diagram
from visualizer.backend.document import Document
from visualizer.backend.misc.grid import Grid
from visualizer.diagram.diagram_graph import DiagramGraph
from visualizer.util.config import Config, StyleConfig
from visualizer.util.tools import run_command


def create_pdf(document: Document):
    with open('generated_graph.tex', 'w') as f:
        f.write(document.generate_code())
    run_command(
        'pdflatex -file-line-error -interaction=nonstopmode -synctex=1 -output-format=pdf -output-directory=out '
        'generated_graph.tex')
    # run_command('pdf2svg out/generated_graph.pdf out/generated_graph.svg')


def visualize(model):
    print(model.get_config())
    input_layer = model.get_layer(name=model.inputs[0].name)
    output_layer = model.get_layer(index=-1)
    diagram_graph = DiagramGraph(input_layer, output_layer)

    document = Document()
    diagram = Diagram()
    document.add_styles(StyleConfig.load_styles())

    # document.add_elements(create_grids())

    utility_layers_done = set()

    for node in diagram_graph.create_nodes():
        diagram.add_node(node)
    diagram.add_edges(diagram_graph.create_edges())

    document.add_element(diagram)

    # model.summary(line_length=222)
    create_pdf(document)


model = load_model('model.h5')
# model = keras.applications.Xception(weights=None)
visualize(model)
