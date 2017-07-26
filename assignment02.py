#!/usr/bin/env python3
"""Assignment 02: Chroma Subsampling."""
import argparse

import cv2
import numpy as np

import util

def main():
    parser = argparse.ArgumentParser(
        description="Downsampling vs Chroma Subsampling.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--imgpath', default='resources/grid-444.png',
                        help="Input image's path.")
    parser.add_argument('-s', '--subsampling', default='444',
                        choices=['444', '440', '422', '420', '411', '410'],
                        help="Subsampling type.")
    parser.add_argument('--width', type=int, default=800,
                        help="Output image's width.")
    parser.add_argument('--height', type=int, default=800,
                        help="Output image's height.")
    args = parser.parse_args()
    img = cv2.imread(args.imgpath)
    if img is None:
        print('Image not found.')
        return
    cv2.imshow('original', util.upSampling(img, args.width, args.height))
    chromaSubsampling = SUBSAMPLING_TYPES[args.subsampling]
    result = chromaSubsampling(img)
    result = util.upSampling(result, args.width, args.height)
    cv2.imshow('chromaSubsampling' + args.subsampling, result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def chromaSubsamplingFactory(a, b):
    """Creates the subsampling function."""
    def _subsamplingChannel(channel):
        if a == 1 and b == 1:
            return channel
        channel = channel[::a, ::b]
        return channel
    def _subsampling(img):
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        (y, cr, cb) = cv2.split(ycrcb)
        cv2.imshow('ycrcb', np.hstack((y, cr, cb)))
        cr = _subsamplingChannel(cr)
        cb = _subsamplingChannel(cb)
        cv2.imshow('y_result', y)
        cv2.imshow('cr_result', cr)
        cv2.imshow('cb_result', cb)
        result = decodeSampled(y, cr, cb, a, b)
        return cv2.cvtColor(result, cv2.COLOR_YCrCb2BGR)
    return _subsampling

def decodeSampled(y, cr, cb, a, b):
    """Decodes the sampled image back to its full size."""
    def _decoding(channel):
        channel = np.repeat(channel, b, axis=1)
        rem = width % b
        if rem > 0:
            # if not multiple of b columns needs to remove extra columns
            extra_cols = b - rem
            channel = channel[:, :-extra_cols]
        channel = np.repeat(channel, a, axis=0)
        rem = height % a
        if rem > 0:
            # if not multiple of a columns needs to remove extra columns
            extra_rows = a - rem
            channel = channel[:-extra_rows, :]
        return channel
    width, height = y.shape
    cr = _decoding(cr)
    cb = _decoding(cb)
    return cv2.merge((y, cr, cb))

SUBSAMPLING_TYPES = {
    '444': chromaSubsamplingFactory(1, 1),
    '440': chromaSubsamplingFactory(2, 1),
    '422': chromaSubsamplingFactory(1, 2),
    '420': chromaSubsamplingFactory(2, 2),
    '411': chromaSubsamplingFactory(1, 4),
    '410': chromaSubsamplingFactory(2, 4),
}

if __name__ == '__main__':
    main()
