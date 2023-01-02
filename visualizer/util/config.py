import yaml


class Config:
    config = None

    @classmethod
    def load_from_config(cls, *properties):
        if cls.config is None:
            with open('config.yaml') as f:
                cls.config = yaml.full_load(f)
        value = cls.config
        for prop in properties:
            value = value[prop]
        return value

    @classmethod
    def load_dot_args(cls):
        dot_config = cls.load_from_config('dot')
        dot_args = ""

        for arg_group, options in dot_config.items():
            arg_prefix = arg_group[0].upper()  # it is dirty but works
            for option, value in options.items():
                dot_args += f"-{arg_prefix}{option}={value} "
        return dot_args

    @classmethod
    def load_styles(cls):
        from visualizer.backend.misc.style import TikzStyle

        cfg_styles = cls.load_from_config('styles')
        styles = {}
        for item in cfg_styles:
            style = item['style']
            style_name = item['name']
            styles[style_name] = TikzStyle(*style['flags'], **style['options'])

        return styles
