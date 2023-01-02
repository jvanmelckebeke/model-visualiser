import keras.layers

from visualizer.layers.layer import Layer
from visualizer.backend.edge import Edge
from visualizer.util.const import UTILITY_LAYER_TYPES


class TrainableLayer(Layer):
    sort_order = 9996

    @classmethod
    def get_trainable_keras_output_layers(cls, layer: keras.layers.Layer):
        outbound_layers = []
        for outbound_layer in cls.get_keras_output_layers(layer):
            if outbound_layer.__class__.__name__ in UTILITY_LAYER_TYPES:
                outbound_layers.extend(cls.get_trainable_keras_output_layers(outbound_layer))
            else:
                outbound_layers.append(outbound_layer)
        return outbound_layers

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
