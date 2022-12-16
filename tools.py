import numpy as np


def process_shape(shape):
    try:
        if len(shape) == 1:
            return process_shape(shape[0])

        if shape[0] is None:
            return process_shape(shape[1:])
        return shape
    except TypeError:
        return shape


def surface_to_npim(surface):
    """ Transforms a Cairo surface into a numpy array. """
    im = +np.frombuffer(surface.get_data(), np.uint8)
    H, W = surface.get_height(), surface.get_width()
    im.shape = (H, W, 4)  # for RGBA
    return im[:, :, :3]
