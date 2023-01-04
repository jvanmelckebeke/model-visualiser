import keras.layers
import networkx as nx

from visualizer.backend.edge import Edge
from visualizer.backend.misc.position import Position
from visualizer.diagram.layers.layer import Layer
from visualizer.diagram.layers.layer_group import LayerGroup

from visualizer.diagram.layers.operation.operation import OperationLayer
from visualizer.diagram.layers.trainable.trainable import TrainableLayer
from visualizer.diagram.layers.utility.utility import UtilityLayer
from visualizer.util.config import Config, DotConfig
from visualizer.util.const import UTILITY_LAYER_TYPES, OPERATION_LAYER_TYPES


def is_trainable_layer(layer: Layer):
    return isinstance(layer, TrainableLayer)


def is_operation_layer(layer: Layer):
    return isinstance(layer, OperationLayer)


def is_utility_layer(layer: Layer):
    return isinstance(layer, UtilityLayer)


class DiagramGraph:
    @classmethod
    def create_layer(cls, layer: keras.layers.Layer) -> Layer:
        layer_type = layer.__class__.__name__
        if layer_type in UTILITY_LAYER_TYPES:
            return UtilityLayer(layer)
        elif layer_type in OPERATION_LAYER_TYPES:
            return OperationLayer(layer)
        else:
            return TrainableLayer(layer)

    def __init__(self, input_keras_layer: keras.layers.Layer, output_keras_layer: keras.layers.Layer):
        self._input_keras_layer = input_keras_layer
        self._output_keras_layer = output_keras_layer

        self.input_layer = self.create_layer(input_keras_layer)
        self.output_layer = self.create_layer(output_keras_layer)

        self.layers = []
        self.layer_groups: list[LayerGroup] = []
        self.layer_groups_map = {}
        self.graph = None
        self.positions = None
        self.layer_map = {}

        self.child_list = {}
        self.parent_list = {}

        self.group_child_list = {}
        self.group_parent_list = {}

        self._preprocess_layers()
        self._build_layer_groups()
        self._preprocess_layer_groups()
        self._build_graph()

    def _preprocess_layers(self):
        self.layers = []

        queue = [self._input_keras_layer]

        while len(queue) > 0:
            layer = queue.pop(0)
            if layer.name not in self.layer_map:
                diagram_layer = self.create_layer(layer)
                self.layers.append(diagram_layer)
                self.layer_map[diagram_layer.name] = diagram_layer
                self.child_list[diagram_layer.name] = [ol.name for ol in diagram_layer.keras_output_layers]
                self.parent_list[diagram_layer.name] = [il.name for il in diagram_layer.keras_input_layers]

                queue.extend(diagram_layer.keras_output_layers)

    def _preprocess_layer_groups(self):
        group_child_list = {}
        group_parent_list = {}

        for layer_group in self.layer_groups:
            group_child_list[layer_group.name] = []
            group_parent_list[layer_group.name] = []
            for layer_name in layer_group.output_layers:
                group_child_list[layer_group.name].append(self.get_group_by_layer_name(layer_name).name)

            for layer_name in layer_group.input_layers:
                group_parent_list[layer_group.name].append(self.get_group_by_layer_name(layer_name).name)

        self.group_child_list = group_child_list
        self.group_parent_list = group_parent_list

    def _build_graph(self):
        self.graph = nx.from_dict_of_lists(self.group_child_list, create_using=nx.DiGraph)
        self.positions = nx.nx_agraph.graphviz_layout(self.graph, prog='dot', args=DotConfig.load_dot_args())
        nx.nx_agraph.write_dot(self.graph, 'graph.dot')
        # scale positions to fit in the canvas
        min_x = min([pos[0] for pos in self.positions.values()])
        min_y = min([pos[1] for pos in self.positions.values()])
        max_x = max([pos[0] for pos in self.positions.values()])
        max_y = max([pos[1] for pos in self.positions.values()])

        canvas_width = Config.load_float('canvas', 'width')
        canvas_height = Config.load_float('canvas', 'height')

        for group_name, pos in self.positions.items():
            new_x = (pos[0] - min_x) / (max_x - min_x) * canvas_width if max_x != min_x else 0
            new_y = (pos[1] - min_y) / (max_y - min_y) * canvas_height if max_y != min_y else 0

            new_x = round(new_x, 2)
            new_y = round(new_y, 2)

            self.positions[group_name] = Position(new_x, new_y)

    def _build_layer_groups(self):
        self.layer_groups = []
        processed_layers = set()
        queue: list[Layer] = [self.input_layer]
        while len(queue) > 0:
            layer = queue.pop(0)

            for child_layer in self.get_child_layers(layer.name):
                if child_layer.name not in processed_layers:
                    queue.append(child_layer)

            if layer.name in processed_layers:
                continue

            children = self.get_child_layers(layer.name)
            parents = self.get_parent_layers(layer.name)

            if is_trainable_layer(layer):

                utility_before = None
                utility_after = None

                if len(children) == 1 and is_utility_layer(children[0]):
                    utility_after = children[0]
                if len(parents) == 1 and is_utility_layer(parents[0]):
                    utility_before = parents[0]

                if utility_before is not None:
                    if utility_before.name in processed_layers:
                        utility_before = None
                    else:
                        processed_layers.add(utility_before.name)

                if utility_after is not None:
                    if utility_after.name in processed_layers:
                        utility_after = None
                    else:
                        processed_layers.add(utility_after.name)

                layer_group = LayerGroup(layer, utility_before, utility_after)
                self.layer_groups.append(layer_group)
                self.layer_groups_map[layer_group.name] = layer_group
            elif not is_utility_layer(layer):
                layer_group = LayerGroup(layer)
                self.layer_groups.append(layer_group)
                self.layer_groups_map[layer_group.name] = layer_group
            else:
                if is_utility_layer(layer) and all([is_utility_layer(l) for l in children]):
                    layer_group = LayerGroup(layer)
                    self.layer_groups.append(layer_group)
                    self.layer_groups_map[layer_group.name] = layer_group
                    processed_layers.add(layer.name)
            if not is_utility_layer(layer):
                processed_layers.add(layer.name)

    def get_group_by_layer_name(self, layer_name: str) -> LayerGroup:
        for layer_group in self.layer_groups:
            if layer_group.contains_layer_name(layer_name):
                return layer_group

    def get_layer(self, name: str) -> Layer:
        return self.layer_map[name]

    def get_child_layers(self, name: str) -> list[Layer]:
        return [self.get_layer(layer_name) for layer_name in self.child_list[name]]

    def get_parent_layers(self, name: str) -> list[Layer]:
        return [self.get_layer(layer_name) for layer_name in self.parent_list[name]]

    def get_layer_by_type(self, layer_type: str) -> list[Layer]:
        return [layer for layer in self.layers if layer.type == layer_type]

    def create_nodes(self):
        nodes = []
        for layer_group in self.layer_groups:
            layer_position = self.positions[layer_group.name]
            nodes.append(layer_group.create_node_group(layer_position))
        return nodes

    def create_edges(self):
        edges = []
        for layer_group in self.layer_groups:
            for child_layer_group_name in self.group_child_list[layer_group.name]:
                child_group = self.layer_groups_map[child_layer_group_name]
                label = child_group.primary_layer.trainable_params
                label = f'{label:,}' if label != 0 else ''
                edges.append(Edge(layer_group.bottom_layer_name, child_group.top_layer_name, label=label))
        return edges
