import uuid
import yaml

INDENT_SIZE = 4
INDENT_STR = ' ' * INDENT_SIZE

def str_shape(shape):
    if isinstance(shape, tuple):
        if shape[0] is None:
            return str_shape(shape[1:])
        if len(shape) == 1:
            return str(shape[0])
        return str(shape)
    elif isinstance(shape, list):
        if len(shape) == 1:
            return str_shape(shape[0])
        return str([str_shape(s) for s in shape])
    else:
        return str(shape)


def generate_uuid():
    return str(uuid.uuid4())[:8]


config = None


def load_from_config(*properties):
    global config
    if config is None:
        with open('config.yaml') as f:
            config = yaml.full_load(f)
    value = config
    for prop in properties:
        value = value[prop]
    return value
