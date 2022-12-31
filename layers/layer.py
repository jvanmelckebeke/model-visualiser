import keras.layers

from tikz.util.style import load_style_from_config
from tools import str_shape
from tikz.node import Node
from tikz.util.position import Position


def get_layer_outbound_layers(layer: keras.layers.Layer):
    outbound_layers = []
    for outbound_node in layer.outbound_nodes:
        outbound_layers.append(outbound_node.outbound_layer)

    return outbound_layers


def get_layer_inbound_layers(layer: keras.layers.Layer):
    inbound_layers = []
    for inbound_node in layer.inbound_nodes:
        if isinstance(inbound_node.inbound_layers, list):
            for inbound_layer in inbound_node.inbound_layers:
                inbound_layers.append(inbound_layer)
        else:
            inbound_layers.append(inbound_node.inbound_layers)

    return inbound_layers


class Layer:
    sort_order = 9999

    @classmethod
    def get_style_name(cls) -> str:
        return f"{cls.__name__}_style"

    @classmethod
    def get_style(cls):
        return load_style_from_config(cls.get_style_name())

    def __init__(self, layer: keras.layers.Layer):
        self.layer = layer
        self.name = layer.name
        self.type = layer.__class__.__name__

        self.inbound_layers_names = []
        self.outbound_layers_names = []
        self.dependency_layers = set()

        self._parse_inbound_layers()
        self._parse_outbound_layers()

    @property
    def trainable_params(self) -> int:
        trainable_params = 0
        for weight in self.layer.weights:
            if weight.trainable:
                trainable_params += weight.shape.num_elements()
        return trainable_params

    @property
    def inbound_layers(self):
        return get_layer_inbound_layers(self.layer)

    @property
    def outbound_layers(self):
        return get_layer_outbound_layers(self.layer)

    @property
    def output_shape(self):
        return str_shape(self.layer.output_shape)

    @property
    def input_shape(self):
        return str_shape(self.layer.input_shape)

    def _parse_inbound_layers(self):
        if len(self.layer.inbound_nodes) == 0:
            return
        for inbound_node in self.layer.inbound_nodes:
            inbound_layers = inbound_node.inbound_layers
            if isinstance(inbound_layers, list):
                for inbound_layer in inbound_layers:
                    self.inbound_layers_names.append(inbound_layer.name)
            else:
                self.inbound_layers_names.append(inbound_layers.name)

    def _parse_outbound_layers(self):
        if len(self.layer.outbound_nodes) == 0:
            return
        for outbound_node in self.layer.outbound_nodes:
            outbound_layer = outbound_node.outbound_layer
            self.outbound_layers_names.append(outbound_layer.name)

    def _get_siblings(self):
        siblings = set()
        if len(self.inbound_layers) != 0:
            for inbound_layer in self.inbound_layers:
                for sibling in get_layer_outbound_layers(inbound_layer):
                    siblings.add(sibling)

        if len(self.outbound_layers) != 0:
            for outbound_layer in self.outbound_layers:
                for sibling in get_layer_inbound_layers(outbound_layer):
                    siblings.add(sibling)
        print(f"Siblings of {self.name}: {siblings}")
        siblings = list(siblings)
        siblings.sort(key=lambda x: x.name)
        return [sibling.name for sibling in siblings]

    def get_position(self):
        inbound_layers = self.inbound_layers_names
        num_inbound_layers = len(inbound_layers)
        first_inbound_layer = inbound_layers[0] if len(inbound_layers) > 0 else None

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
        return Position(below_right_of=middle_left)

    def add_dependency_layer(self, layer):
        if isinstance(layer, Layer):
            self.dependency_layers.add(layer.name)
        else:
            self.dependency_layers.add(layer)

    @property
    def layer_description(self) -> tuple:
        return self.type, f"output_shape: {self.output_shape}"

    def create_node(self):

        return Node(self.name,
                    *self.layer_description,
                    node_style=self.get_style_name(),
                    position=self.get_position(),
                    depends_on=self.dependency_layers)

    def create_edges(self):
        return []

    def __str__(self):
        return f"Layer(name={self.name}, type={self.type})"

    def __lt__(self, other):
        return self.sort_order < other.sort_order or (self.sort_order == other.sort_order and self.name < other.name)
