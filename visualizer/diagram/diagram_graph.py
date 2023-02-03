import math

import keras.layers
import networkx as nx

from visualizer.backend.base import TikzOptions
from visualizer.backend.edge import Edge
from visualizer.backend.misc.position import Position
from visualizer.diagram.layers.layer import Layer
from visualizer.diagram.layers.layer_group import LayerGroup

from visualizer.util.config import Config, DotConfig

import seaborn as sns
import numpy as np

from visualizer.util.const import COLOR_MAP


def is_trainable_layer(layer: Layer):
    return not is_operation_layer(layer) and not is_utility_layer(layer)


def is_operation_layer(layer: Layer):
    return layer.type_group == 'operation'


def is_utility_layer(layer: Layer):
    return layer.type_group == 'utility'


class DiagramGraph:
    @classmethod
    def create_layer(cls, layer: keras.layers.Layer) -> Layer:
        return Layer(layer)

    def __init__(self, input_keras_layer: keras.layers.Layer, output_keras_layer: keras.layers.Layer, canvas_width=None,
                 canvas_height=None):

        self.edge_colors = COLOR_MAP
        self._input_keras_layer = input_keras_layer
        self._output_keras_layer = output_keras_layer

        self.input_layer = self.create_layer(input_keras_layer)
        self.output_layer = self.create_layer(output_keras_layer)

        self.canvas_width = canvas_width if canvas_width is not None else Config.load_int('canvas', 'width')
        self.canvas_height = canvas_height if canvas_height is not None else Config.load_int('canvas', 'height')

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

        # scale positions to fit in the canvas
        min_x = min([pos[0] for pos in self.positions.values()])
        min_y = min([pos[1] for pos in self.positions.values()])
        max_x = max([pos[0] for pos in self.positions.values()])
        max_y = max([pos[1] for pos in self.positions.values()])

        for group_name, pos in self.positions.items():
            new_x = (pos[0] - min_x) / (max_x - min_x) * self.canvas_width if max_x != min_x else 0
            new_y = (pos[1] - min_y) / (max_y - min_y) * self.canvas_height if max_y != min_y else 0

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
        raise ValueError(f'Layer {layer_name} not found')

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

    def edge_is_skip_connection(self, parent_layer_name, child_layer_name):
        parent_position = self.positions[parent_layer_name]
        child_position = self.positions[child_layer_name]

        if parent_position.x - 0.5 <= child_position.x <= parent_position.x + 0.5:
            range_rectangle = (
                Position(min(parent_position.x, child_position.x) - 1, min(parent_position.y, child_position.y)),
                Position(max(parent_position.x, child_position.x) + 1, max(parent_position.y, child_position.y)))

            for layer_group, position in self.positions.items():
                if layer_group == parent_layer_name or layer_group == child_layer_name:
                    continue
                if (range_rectangle[0].x <= position.x <= range_rectangle[1].x and
                        range_rectangle[0].y <= position.y <= range_rectangle[1].y):
                    # print(f'edge {parent_layer_name} -> {child_layer_name} is crossing {layer_group}')
                    return True

    def calc_bend_direction(self, parent_layer_name, child_layer_name):
        # get other children / parents of parent / child
        parent_children = self.group_child_list[parent_layer_name]
        child_parents = self.group_parent_list[child_layer_name]

        # filter out the current layer
        parent_children = [layer for layer in parent_children if layer != child_layer_name]
        child_parents = [layer for layer in child_parents if layer != parent_layer_name]

        # combine the two lists
        other_layers = parent_children + child_parents

        # average x position of the other layers
        other_layers_x = [self.positions[layer].x for layer in other_layers]
        if len(other_layers_x) == 0:
            return 'right'
        other_layers_x_avg = sum(other_layers_x) / len(other_layers_x)

        # if the average x position is smaller than the child layer, the bend direction is left
        if other_layers_x_avg < self.positions[child_layer_name].x:
            return 'left'
        else:
            return 'right'

    def calc_extra_edge_args(self, parent_layer_name, child_layer_name):
        options = TikzOptions()
        parent_position = self.positions[parent_layer_name]
        child_position = self.positions[child_layer_name]

        parent_child_list = self.group_child_list[parent_layer_name]
        child_parent_list = self.group_parent_list[child_layer_name]

        parent_child_distances = [parent_position.y_distance(self.positions[layer_name]) for layer_name in
                                  parent_child_list]

        child_parent_distances = [child_position.y_distance(self.positions[layer_name]) for layer_name in
                                  child_parent_list]

        min_parent_child_distance = min(parent_child_distances)
        min_child_parent_distance = min(child_parent_distances)
        # y_distance = round(parent_position.y_distance(child_position), 3)
        x_distance = round(parent_position.x_distance(child_position), 3)
        # distance = round(parent_position.distance(child_position), 3)

        ratio_in = 0.3
        ratio_out = 0.3

        if 0 < x_distance < 1:
            ratio_in = ratio_out = 0.1

        if min_parent_child_distance >= 1.5 * min_child_parent_distance:
            # print(f"edge between {parent_layer_name} and {child_layer_name} is a long edge (out)")
            ratio_out = 0.5
        elif min_child_parent_distance >= 1.5 * min_parent_child_distance:
            # print(f"edge between {parent_layer_name} and {child_layer_name} is a long edge (in)")
            ratio_in = 0.5

        in_distance = round(min_child_parent_distance * ratio_in, 2)
        out_distance = round(min_parent_child_distance * ratio_out, 2)

        if self.edge_is_skip_connection(parent_layer_name, child_layer_name):
            in_distance *= 1.25
            out_distance *= 1.25
            bend_direction = self.calc_bend_direction(parent_layer_name, child_layer_name)

            options.add_option(f'bend {bend_direction}', '70')
            options.add_option('in', '180')

        # print(f"between {parent_layer_name} and {child_layer_name} "
        #       f"(y distance: {y_distance}, x distance: {x_distance}, distance: {distance}) "
        #       f"in_distance: {in_distance} out_distance: {out_distance}")

        options.add_option('in distance', f"{in_distance}cm")
        options.add_option('out distance', f"{out_distance}cm")
        return options

    def create_edges(self, use_color=False):
        amount_of_bins = len(self.edge_colors)
        eligible_trainable_layers = [layer for layer in self.layers if is_trainable_layer(layer)]
        trainable_params_list = [layer.trainable_params for layer in eligible_trainable_layers]
        trainable_params_list = [params for params in trainable_params_list if params != 0]

        trainable_params_list = sorted(trainable_params_list)
        if use_color:
            bins = np.array_split(trainable_params_list, amount_of_bins - 1)
            trainable_params_list_bins = [bin[0] for bin in bins]
            # print(sorted(trainable_params_list))

            # trainable_params_list_bins = np.cumsum(trainable_params_list_bins)
            # print("bins:", trainable_params_list_bins)

        def get_edge_color(edge_weight):
            if not use_color or edge_weight == 0:
                return "black"
            # calculate the bin index of the edge weight
            bin_index = np.digitize(edge_weight, trainable_params_list_bins)
            # print(f"edge weight {edge_weight} is in bin {bin_index}")
            return f"COLOR{bin_index}"

        edges = []
        for layer_group in self.layer_groups:
            for child_layer_group_name in self.group_child_list[layer_group.name]:
                child_group = self.layer_groups_map[child_layer_group_name]
                label = child_group.primary_layer.trainable_params

                color = get_edge_color(label)

                label = f'{label:,}' if label != 0 else ''
                extra_args = self.calc_extra_edge_args(layer_group.name, child_layer_group_name)

                edges.append(
                    Edge(layer_group.bottom_layer_name,
                         child_group.top_layer_name,
                         label=label, color=color, extra_args=extra_args))
        return edges
