import os.path

import yaml

RESOURCE_PATH = os.path.join(os.path.dirname(__file__), '..', 'resources')


class Config:
    config = None
    config_file = os.path.join(RESOURCE_PATH, 'config', 'config.yaml')

    @classmethod
    def load(cls, *properties):
        with open(cls.config_file) as f:
            cls.config = yaml.full_load(f)
        value = cls.config
        for prop in properties:
            value = value[prop]
        return value

    @classmethod
    def load_int(cls, *properties):
        return int(cls.load(*properties))

    @classmethod
    def load_float(cls, *properties):
        return float(cls.load(*properties))

    @classmethod
    def load_str(cls, *properties):
        return str(cls.load(*properties))


class GeneralConfig(Config):
    config_file = os.path.join(RESOURCE_PATH, 'config', 'config.yaml')


class StyleConfig(Config):
    config_file = os.path.join(RESOURCE_PATH, 'config', 'style.yaml')

    @classmethod
    def load_styles(cls):
        from visualizer.backend.misc.style import TikzStyle

        cfg_styles = cls.load('styles')
        styles = {}
        for item in cfg_styles:
            style = item['style']
            style_name = item['name']
            styles[style_name] = TikzStyle(*style['flags'], **style['options'])

        return styles


class LayerConfig(Config):
    config_file = os.path.join(RESOURCE_PATH, 'config', 'layers.yaml')


class DotConfig(Config):
    config_file = os.path.join(RESOURCE_PATH, 'config', 'dot.yaml')

    @classmethod
    def load_dot_args(cls):
        dot_config = cls.load('dot')
        dot_args = ""

        for arg_group, options in dot_config.items():
            arg_prefix = arg_group[0].upper()  # it is dirty but works
            for option, value in options.items():
                dot_args += f"-{arg_prefix}{option}={value} "
        return dot_args
