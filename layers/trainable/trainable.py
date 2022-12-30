import keras.layers

from layers.layer import Layer
from tikz.edges.edge import Edge
from tikz.util.position import Position
from tikz.util.style import create_node_style


class TrainableLayer(Layer):
    sort_order = 9996
    node_distance = 2
    style = create_node_style("blue", node_distance)

    def __init__(self, layer: keras.layers.Layer):
        self.num_params = layer.count_params()
        super().__init__(layer)

    @property
    def layer_description(self) -> tuple:
        return self.type, f"input shape: {self.input_shape}", f"output shape: {self.output_shape}"

    def create_edges(self):
        edges = []
        for inbound_layer in self.inbound_layers:
            edges.append(Edge(inbound_layer.name, self.name, format(self.num_params, ",d")))
        return edges

    def get_position(self):
        inbound_layers = self.inbound_layers_names
        num_inbound_layers = len(inbound_layers)
        first_inbound_layer = inbound_layers[0] if len(inbound_layers) > 0 else None
        siblings = self._get_siblings()

        if len(siblings) == 1:
            if len(inbound_layers) == 0:
                return Position()

            if num_inbound_layers == 1:
                self.add_dependency_layer(first_inbound_layer)
                return Position(below_of=first_inbound_layer)

            if num_inbound_layers % 2 == 1:
                middle_layer = inbound_layers[num_inbound_layers // 2]
                self.add_dependency_layer(middle_layer)
                return Position(below_of=middle_layer)

            middle_left = inbound_layers[num_inbound_layers // 2 - 1]
            middle_right = inbound_layers[num_inbound_layers // 2]
            self.add_dependency_layer(middle_left)
            self.add_dependency_layer(middle_right)
            return Position(below_of=f"$({middle_left}!0.5!{middle_right})$")

        siblings = list(siblings)
        sibling_index = siblings.index(self.name)
        self.add_dependency_layer(first_inbound_layer)

        if sibling_index == 0:
            return Position(below_of=first_inbound_layer)

        if sibling_index == 1:
            self.add_dependency_layer(siblings[0])
            return Position(below_of=first_inbound_layer, left_of=siblings[0])

        if sibling_index % 2 == 1:
            self.add_dependency_layer(siblings[sibling_index - 2])
            return Position(below_of=first_inbound_layer, left_of=siblings[sibling_index - 2])

        self.add_dependency_layer(siblings[sibling_index - 2])
        return Position(below_of=first_inbound_layer, right_of=siblings[sibling_index - 2])