import keras.layers

from visualizer.util.tools import str_shape
from visualizer.backend.node import Node, NodeGroup
from visualizer.backend.misc.position import Position


class Layer:
    sort_order = 9999

    @classmethod
    def get_style_name(cls) -> str:
        return f"{cls.__name__}_style"

    @classmethod
    def get_keras_output_layers(cls, layer: keras.layers.Layer):
        outbound_layers = []
        for outbound_node in layer.outbound_nodes:
            outbound_layers.append(outbound_node.outbound_layer)

        return outbound_layers

    @classmethod
    def get_keras_input_layers(cls, layer: keras.layers.Layer):
        inbound_layers = []
        for inbound_node in layer.inbound_nodes:
            if isinstance(inbound_node.inbound_layers, list):
                for inbound_layer in inbound_node.inbound_layers:
                    inbound_layers.append(inbound_layer)
            else:
                inbound_layers.append(inbound_node.inbound_layers)

        return inbound_layers

    def __init__(self, layer: keras.layers.Layer):
        self.layer = layer
        self.name: str = layer.name
        self.type: str = layer.__class__.__name__
        self.type_group: str = self.__class__.__name__
        self.position = Position()

        self.inbound_layers_names = []
        self.outbound_layers_names = []
        self.dependency_layers = set()

        self._parse_input_layers()
        self._parse_output_layers()

    @property
    def trainable_params(self) -> int:
        trainable_params = 0
        for weight in self.layer.weights:
            if weight.trainable:
                trainable_params += weight.shape.num_elements()
        return trainable_params

    @property
    def keras_input_layers(self):
        return self.get_keras_input_layers(self.layer)

    @property
    def keras_output_layers(self):
        return self.get_keras_output_layers(self.layer)

    @property
    def output_shape(self):
        return str_shape(self.layer.output_shape)

    @property
    def input_shape(self):
        return str_shape(self.layer.input_shape)

    def _parse_input_layers(self):
        if len(self.layer.inbound_nodes) == 0:
            return
        for inbound_node in self.layer.inbound_nodes:
            inbound_layers = inbound_node.inbound_layers
            if isinstance(inbound_layers, list):
                for inbound_layer in inbound_layers:
                    self.inbound_layers_names.append(inbound_layer.name)
            else:
                self.inbound_layers_names.append(inbound_layers.name)

    def _parse_output_layers(self):
        if len(self.layer.outbound_nodes) == 0:
            return
        for outbound_node in self.layer.outbound_nodes:
            outbound_layer = outbound_node.outbound_layer
            self.outbound_layers_names.append(outbound_layer.name)

    def _get_siblings(self):
        siblings = set()
        if len(self.keras_input_layers) != 0:
            for inbound_layer in self.keras_input_layers:
                for sibling in self.get_keras_output_layers(inbound_layer):
                    siblings.add(sibling)

        if len(self.keras_output_layers) != 0:
            for outbound_layer in self.keras_output_layers:
                for sibling in self.get_keras_input_layers(outbound_layer):
                    siblings.add(sibling)
        print(f"Siblings of {self.name}: {siblings}")
        siblings = list(siblings)
        siblings.sort(key=lambda x: x.name)
        return [sibling.name for sibling in siblings]

    def add_dependency_layer(self, layer):
        if isinstance(layer, Layer):
            self.dependency_layers.add(layer.name)
        else:
            self.dependency_layers.add(layer)

    @property
    def layer_description(self) -> tuple:
        return self.type, f"output_shape: {self.output_shape}"

    def create_node(self, position: Position = None):

        return Node(self.name,
                    *self.layer_description,
                    node_style_name=self.get_style_name(),
                    position=position,
                    depends_on=[])

    def create_edges(self):
        return []

    def __str__(self):
        return f"Layer(name={self.name}, type={self.type})"

    def __lt__(self, other):
        return self.sort_order < other.sort_order or (self.sort_order == other.sort_order and self.name < other.name)


class LayerGroup:
    def __init__(self, primary_layer: Layer, layer_before: Layer = None, layer_after: Layer = None, name: str = None):
        if name is None:
            name = f"{primary_layer.name}_group"
        self.name = name
        self.primary_layer = primary_layer
        self.layer_before = layer_before
        self.layer_after = layer_after

        self.layers = [primary_layer, layer_before, layer_after]
        self.layers = [l for l in self.layers if l is not None]

    def create_node_group(self, position: Position = None):
        return NodeGroup(self.primary_layer.create_node(position=position),
                         node_before=self.layer_before.create_node() if self.layer_before is not None else None,
                         node_after=self.layer_after.create_node() if self.layer_after is not None else None)

    @property
    def top_layer_name(self):
        if self.layer_before is not None:
            return self.layer_before.name
        return self.primary_layer.name

    @property
    def bottom_layer_name(self):
        if self.layer_after is not None:
            return self.layer_after.name
        return self.primary_layer.name

    @property
    def input_layers(self) -> list[str]:
        if self.layer_before is None:
            return [l.name for l in self.primary_layer.keras_input_layers]
        return [l.name for l in self.layer_before.keras_input_layers]

    @property
    def output_layers(self) -> list[str]:
        if self.layer_after is None:
            return [l.name for l in self.primary_layer.keras_output_layers]
        return [l.name for l in self.layer_after.keras_output_layers]

    def contains_layer_name(self, name):
        return any([l.name == name for l in self.layers])
