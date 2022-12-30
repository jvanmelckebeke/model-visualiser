from layers.layer import Layer
from tikz.edges.edge import Edge
from tikz.util.style import create_node_style
import keras.layers


class UtilityLayer(Layer):
    sort_order = 9998
    node_distance = 0
    style = create_node_style("gray", node_distance)

    def __init__(self, layer: keras.layers.Layer):
        super().__init__(layer)

    @property
    def layer_description(self) -> tuple:
        return self.type,

    def create_edges(self):
        edges = []
        if self.get_position().left_of is None and self.get_position().right_of is None:
            return edges

        for inbound_layer in self.inbound_layers:
            edges.append(Edge(inbound_layer.name, self.name))
        return edges
