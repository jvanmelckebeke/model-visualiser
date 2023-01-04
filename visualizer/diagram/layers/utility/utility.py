from visualizer.diagram.layers.layer import Layer
from visualizer.backend.edge import Edge
import keras.layers


class UtilityLayer(Layer):
    sort_order = 9998

    def __init__(self, layer: keras.layers.Layer):
        super().__init__(layer)

    def create_edges(self):
        edges = []

        for inbound_layer in self.keras_input_layers:
            edges.append(Edge(inbound_layer.name, self.name))
        return edges
