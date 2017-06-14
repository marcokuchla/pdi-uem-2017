#!/usr/bin/env python3
"""Assignment 01: 'I love Hue' game's grid."""
import cv2
import numpy as np

def main():
    """Entry point."""
    # tl = np.array([0, 0, 0])
    # tr = np.array([85, 85, 85])
    # br = np.array([170, 170, 170])
    # bl = np.array([255, 255, 255])
    tl = np.random.randint(0, 255, 3)
    tr = np.random.randint(0, 255, 3)
    bl = np.random.randint(0, 255, 3)
    br = np.random.randint(0, 255, 3)
    img = up_sampling(get_image(5, 5, tl, tr, br, bl))
    img2 = up_sampling(get_image_old(5, 5, tl, tr, br, bl))
    cv2.imshow('image', img)
    cv2.imshow('image2', img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_image(width, height, color_tl, color_tr, color_br, color_bl):
    """Creates game image (optimized)."""
    colors = np.array([color_tl, color_tr, color_br, color_bl])
    w_matrix = get_weight_matrix(width, height)
    return np.uint8(np.matmul(w_matrix, colors))

def get_weight_matrix(width, height):
    """Calculates the weights' matrix."""
    colvals = np.linspace(0, 1, width)
    rowvals = np.linspace(0, 1, height)
    xx, yy = np.meshgrid(rowvals, colvals)
    # bottom right weight matrix
    brw = xx * yy
    #bottom left weight matrix
    blw = np.fliplr(brw)
    # top right weight matrix
    trw = np.flipud(brw)
    # top left weight matrix
    tlw = np.fliplr(trw)
    return np.dstack((tlw, trw, brw, blw))

def up_sampling(image, new_width=640, new_height=640):
    """Up sampling image by repeat."""
    (width, height, _) = image.shape
    scale_x = int(new_width / width)
    scale_y = int(new_height / height)
    return np.repeat(np.repeat(image, scale_x, axis=0), scale_y, axis=1)

def get_image_old(width, height, color_tl, color_tr, color_br, color_bl):
    """Creates game image."""
    l_col = get_colors(color_tl, color_bl, height)
    r_col = get_colors(color_tr, color_br, height)
    rows = [get_colors(c1, c2, width) for (c1, c2) in zip(l_col, r_col)]
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
    """Calculates linspace given values."""
    if value1 < value2:
        return np.linspace(value1, value2, num)
    return np.linspace(value2, value1, num)[::-1]

if __name__ == '__main__':
    main()
