from visualizer.backend.node_group import NodeGroup
from visualizer.backend.misc.position import Position
from visualizer.diagram.layers.layer import Layer


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

    def __repr__(self):
        return f"LayerGroup({self.name}) primary layer {self.primary_layer.name} with before: " \
               f"{self.layer_before.name if self.layer_before is not None else None}, with after: " \
               f"{self.layer_after.name if self.layer_after is not None else None})"

    def __str__(self):
        return self.__repr__()
