"""Módulo de utilidades para processamento de imagens."""
import numpy as np


def upSampling(image, newWidth, newHeight):
    """Up sampling image by repeat."""
    (height, width) = image.shape[:2]
    scaleX = int(newWidth / width)
    scaleY = int(newHeight / height)
    return np.repeat(np.repeat(image, scaleX, axis=1), scaleY, axis=0)

def downSampling(image):
    pass
