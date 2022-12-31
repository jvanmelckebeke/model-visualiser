import keras.layers

from layers.layer import Layer
from tikz.edges.edge import Edge


class OperationLayer(Layer):
    sort_order = 9997

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
