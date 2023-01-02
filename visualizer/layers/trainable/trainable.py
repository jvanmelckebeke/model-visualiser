import keras.layers

from visualizer.layers.layer import Layer
from visualizer.backend.edge import Edge


class TrainableLayer(Layer):
    sort_order = 9996

    def __init__(self, layer: keras.layers.Layer):
        self.num_params = layer.count_params()
        super().__init__(layer)

    @property
    def layer_description(self) -> tuple:
        return self.type, f"input shape: {self.input_shape}", f"output shape: {self.output_shape}"

    def create_edges(self):
        edges = []
        for inbound_layer in self.input_layers:
            edges.append(Edge(inbound_layer.name, self.name, format(self.num_params, ",d")))
        return edges


