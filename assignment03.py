#!/usr/bin/env python
"""
Assignment 03: Contrast correction in dark regions with histogram
equalization.
"""
import argparse

import cv2
import numpy as np


def main():
    parser = argparse.ArgumentParser(
        description="Dark regions contrast corrector.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-i', '--inputImage',
        default='resources/low-contrast.png',
        help="Input image's path.")
    args = parser.parse_args()
    img = cv2.imread(args.inputImage)
    if img is None:
        raise RuntimeError('Image could not be loaded.')
    img2 = correct_contrast(img)
    cv2.imshow('input', img)
    cv2.imshow('output', img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def correct_contrast(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    (h, s, v) = cv2.split(hsv)
    cv2.imshow('value in', v)
    thr_val, thr_img = cv2.threshold(v, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    thr_val = int(thr_val)
    print('Otsu threshold: {}'.format(thr_val))
    hist, bins = np.histogram(v.flatten(), 256, [0, 256])
    hist = hist[:thr_val]
    cum_hist = np.cumsum(hist)
    cum_hist_norm = cum_hist * (thr_val - 1) / cum_hist[-1]  # hist.max() == thr_val - 1
    lut = np.arange(256, dtype=np.uint8)  # lut = [0, 1, 2, ..., 255]
    lut[:len(cum_hist_norm)] = cum_hist_norm  # override equalized values
    v = lut[v]
    cv2.imshow('value out', v)
    hsv = cv2.merge((h, s, v))
    img_out = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return img_out

if __name__ == '__main__':
    main()
