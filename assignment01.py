#!/usr/bin/env python3
"""Trabalho 'I love Hue'"""
import cv2
import numpy as np

def main():
    c1 = np.random.randint(0, 255, 3)
    c2 = np.random.randint(0, 255, 3)
    c3 = np.random.randint(0, 255, 3)
    c4 = np.random.randint(0, 255, 3)
    img = up_sampling(get_image(5, 5, c1, c2, c3, c4))
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def up_sampling(image, new_width=640, new_height=640):
    """Up sampling image by repeat."""
    (width, height, _) = image.shape
    scale_x = int(new_width / width)
    scale_y = int(new_height / height)
    return np.repeat(np.repeat(image, scale_x, axis=0), scale_y, axis=1)

def get_image(width, height, color_tl, color_tr, color_br, color_bl):
    """Create game image."""
    l_col = get_colors(color_tl, color_bl, height)
    r_col = get_colors(color_tr, color_br, height)
    rows = [get_colors(c1, c2, width) for (c1, c2) in zip(r_col, l_col)]
    return np.array(rows)

def get_colors(rgb1, rgb2, num):
    """Returns the colors """
    red1, green1, blue1 = rgb1
    red2, green2, blue2 = rgb2
    reds = np.uint8(get_linspace(red1, red2, num))
    greens = np.uint8(get_linspace(green1, green2, num))
    blues = np.uint8(get_linspace(blue1, blue2, num))
    return np.stack((blues, greens, reds), axis=1)

def get_linspace(value1, value2, num):
    """Calculate linspace given values."""
    if value1 < value2:
        return np.linspace(value1, value2, num)
    return np.linspace(value2, value1, num)

if __name__ == '__main__':
    main()
