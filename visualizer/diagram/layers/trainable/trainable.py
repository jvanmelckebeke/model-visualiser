import keras.layers

from visualizer.diagram.layers.layer import Layer
from visualizer.backend.edge import Edge
from visualizer.util.config import LayerConfig
from visualizer.util.const import UTILITY_LAYER_TYPES
from visualizer.util.tools import str_shape


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

    def create_edges(self):
        edges = []
        for inbound_layer in self.keras_input_layers:
            edges.append(Edge(inbound_layer.name, self.name, format(self.num_params, ",d")))
        return edges
