#!/usr/bin/env python3
"""Assignment 01: 'I love Hue' game's grid."""
import argparse

import cv2
import numpy as np

import util

def main():
    """Entry point."""
    parser = argparse.ArgumentParser(
        description="'I love Hue' game board generator.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('rows', type=int,
                        help='Number of rows of the Matrix.')
    parser.add_argument('cols', type=int,
                        help='Number of colums of the Matrix.')
    parser.add_argument('--width', type=int, default=640,
                        help="Output image's width.")
    parser.add_argument('--height', type=int, default=640,
                        help="Output image's height.")
    args = parser.parse_args()
    (tl, tr, bl, br) = gen_colors()
    img = gen_image(args.rows, args.cols, tl, tr, br, bl)
    img = util.upSampling(img, args.width, args.height)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def gen_colors():
    """Generate four random BGR colors."""
    tl = np.random.randint(0, 255, 3)
    tr = np.random.randint(0, 255, 3)
    bl = np.random.randint(0, 255, 3)
    br = np.random.randint(0, 255, 3)
    return (tl, tr, bl, br)

def gen_image(rows, cols, color_tl, color_tr, color_br, color_bl):
    """Creates game image (optimized)."""
    colors = np.array([color_tl, color_tr, color_br, color_bl])
    w_matrix = get_weight_matrix(rows, cols)
    return np.uint8(np.matmul(w_matrix, colors))

def get_weight_matrix(rows, cols):
    """Calculates the weights' matrix."""
    colvals = np.linspace(0, 1, cols)
    rowvals = np.linspace(0, 1, rows)
    xx, yy = np.meshgrid(rowvals, colvals)
    # bottom right weight matrix
    brw = xx * yy
    # bottom left weight matrix
    blw = np.fliplr(brw)
    # top right weight matrix
    trw = np.flipud(brw)
    # top left weight matrix
    tlw = np.fliplr(trw)
    return np.dstack((tlw, trw, brw, blw))

if __name__ == '__main__':
    main()
