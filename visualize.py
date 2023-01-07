from keras.models import load_model
from wand.image import Image as WImage
from wand.color import Color
from visualizer.backend.diagram import Diagram
from visualizer.backend.document import Document
from visualizer.diagram.diagram_graph import DiagramGraph
from visualizer.util.config import StyleConfig
from visualizer.util.tools import run_command


def create_pdf(document: Document):
    with open('generated_graph.tex', 'w') as f:
        f.write(document.generate_code())
    run_command(
        'pdflatex -file-line-error -interaction=nonstopmode -synctex=1 -output-format=pdf -output-directory=out '
        'generated_graph.tex')
    # run_command('pdf2svg out/generated_graph.pdf out/generated_graph.svg')


def visualize(model, resolution=200):
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
    img = WImage(filename='out/generated_graph.pdf', resolution=resolution)
    img.background_color = Color('white')
    img.alpha_channel = 'remove'
    return img


if __name__ == '__main__':
    model = load_model('model.h5')
    visualize(model)
