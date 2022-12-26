import os

from tensorflow.keras.models import load_model


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


DEFAULT_NODE_STYLE = "rectangle split, rectangle split ignore empty parts, rectangle split parts=2, draw=blue!60, " \
                     "fill=blue!5, very thick, minimum width={width(\"Batch Normalisation\") + 8pt}, node distance=2," \
                     " outer sep=0pt"
DEFAULT_PATH_STYLE = "thick, out=-90, in=90, out distance=1cm, in distance=1cm"

TEXT_BEFORE = r"\documentclass{standalone}" \
              "\n" \
              r"\usepackage{tikz}" \
              "\n" \
              r"\usetikzlibrary{positioning}" \
              "\n" \
              r"\usetikzlibrary{shapes.multipart}" \
              "\n" \
              r"\usetikzlibrary{calc}" \
              "\n" \
              r"\usetikzlibrary{graphs}" \
              "\n" \
              r"\usetikzlibrary{graphs.standard}" \
              "\n" \
              r"\begin{document}" \
              "\n" \
              r"\begin{tikzpicture}" \
              "\n" \
              f"[default_node/.style={{{DEFAULT_NODE_STYLE}}}, " \
              f"default_path/.style={{{DEFAULT_PATH_STYLE}}}]\n "

TEXT_AFTER = r"\end{tikzpicture}" \
             r"\end{document}"


def create_pdf(graph_code: str):
    with open('generated_graph.tex', 'w') as f:
        f.write(TEXT_BEFORE)
        f.write(graph_code)
        f.write(TEXT_AFTER)

    os.system(
        'pdflatex -file-line-error -interaction=nonstopmode -synctex=1 -output-format=pdf -output-directory=out '
        'generated_graph.tex')


def generate_layer_node(_layer,
                        below_of=None,
                        right_of=None,
                        left_of=None,
                        node_style="default_node"):
    layer_type = _layer.__class__.__name__
    layer_shape = str_shape(_layer.output_shape)

    position_args_list = []
    if below_of:
        position_args_list.append(f"below= of {below_of}")
    if right_of:
        position_args_list.append(f"right= of {right_of}")
    if left_of:
        position_args_list.append(f"left= of {left_of}")

    position_args = ", ".join(position_args_list)

    position_text = f"[{position_args}]" if position_args else ""

    layer_description = fr"{layer_type}\nodepart{{two}}output shape: {layer_shape}"

    return rf"\node[{node_style}] ({_layer.name}) {position_text} {{{layer_description}}};" + "\n"


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


model = load_model("model.h5")

parent_map = {}
child_map = {}

graph_code = ""
for layer in model.layers:
    parent_layer = get_parent_layer(layer)
    child_layers = get_child_layers(layer)

    if child_layers:
        child_map[layer.name] = child_layers

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
                print("layer name: ", layer.name, "right of: ", right_of_layer, "adjecency list: ",
                      parent_map[parent_layer])
            else:
                left_of_layer = parent_map[parent_layer][-3]
                print("layer name: ", layer.name, "left of: ", left_of_layer, "adjecency list: ",
                      parent_map[parent_layer])

    graph_code += generate_layer_node(layer, below_of=below_of_layer, left_of=left_of_layer, right_of=right_of_layer)

for key, value in child_map.items():
    for child in value:
        graph_code += rf"\draw[->, default_path] ({key}) to ({child});" + "\n"

create_pdf(graph_code)
