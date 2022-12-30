import keras.layers

from layers.layer import Layer
from tikz.edges.edge import Edge
from tikz.util.style import create_node_style


class OperationLayer(Layer):
    sort_order = 9997
    node_distance = 1
    style = create_node_style("violet", node_distance)

    def __init__(self, layer: keras.layers.Layer):
        super().__init__(layer)

    def create_edges(self):
        edges = []
        for inbound_layer in self.inbound_layers:
            edges.append(Edge(inbound_layer.name, self.name))
        return edges

    @property
    def layer_description(self) -> tuple:
        return self.type,
