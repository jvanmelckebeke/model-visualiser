import os
import uuid

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


def latexify(text):
    text = text.replace("_", r"-")
    text = text.replace(".", r"-")
    return text


def generate_uuid():
    return str(uuid.uuid4())[:8]


def run_command(cmd):
    exit_code = os.system(cmd)
    if exit_code != 0:
        raise Exception("Error while running command: " + cmd)


def pt_to_mm(pt):
    return pt / 2.834645669


def pretty_print(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + "\"" + str(key) + "\":")
        if isinstance(value, dict):
            pretty_print(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))
