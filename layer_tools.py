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
