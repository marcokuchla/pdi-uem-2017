"""Módulo de utilidades para processamento de imagens."""
import numpy as np


def up_sampling(image, new_width, new_height):
    """Up sampling image by repeat."""
    (height, width) = image.shape[:2]
    scale_x = int(new_width / width)
    scale_y = int(new_height / height)
    return np.repeat(np.repeat(image, scale_x, axis=1), scale_y, axis=0)

def downSampling(image):
    pass
