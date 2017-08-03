#!/usr/bin/python3
"""
Assignment 03: Contrast correction in dark regions with histogram
equalization.
"""
import argparse

import cv2
import numpy as np


def main():
    """Entry-point"""
    parser = argparse.ArgumentParser(
        description="Dark regions contrast corrector.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-i', '--inputImage',
        default='resources/low-contrast.png',
        help="Input image's path.")
    parser.add_argument(
        '--gray',
        action='store_const',
        const=True,
        help="Read image as grayscale (flag).")
    args = parser.parse_args()
    flag = cv2.IMREAD_GRAYSCALE if args.gray else cv2.IMREAD_COLOR
    img = cv2.imread(args.inputImage, flag)
    if img is None:
        raise RuntimeError('Image could not be loaded.')
    img2 = correct_contrast(img)
    cv2.imshow('input', img)
    cv2.imshow('output', img2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def correct_contrast(img):
    """Corrects the constrast of dark regions on the image color or gray."""
    if len(img.shape) > 2:
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        (h, s, v) = cv2.split(hsv)
        cv2.imshow('value in', v)
        v = do_correct_contrast(v)
        cv2.imshow('value out', v)
        hsv = cv2.merge((h, s, v))
        img_out = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    else:
        img_out = do_correct_contrast(img)
    return img_out


def do_correct_contrast(img):
    """Corrects the constrast of dark regions on the gray image."""
    thr_val, thr_img = cv2.threshold(img, 0, 255,
                                     cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    thr_val = int(thr_val)
    print('Otsu threshold: {}'.format(thr_val))
    hist, bins = np.histogram(img.flatten(), 256, [0, 256])
    hist = hist[:thr_val]
    cum_hist = np.cumsum(hist)
    cum_hist_norm = cum_hist * (thr_val - 1) / cum_hist[-1]  # hist.max() == thr_val - 1
    lut = np.arange(256, dtype=np.uint8)  # lut = [0, 1, 2, ..., 255]
    lut[:len(cum_hist_norm)] = cum_hist_norm  # override equalized values
    return lut[img]

if __name__ == '__main__':
    main()
