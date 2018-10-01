#!/usr/bin/python3
"""Assignment 02: Chroma Subsampling."""
import argparse

import cv2
import numpy as np


def main():
  parser = argparse.ArgumentParser(
    description="Downsampling vs Chroma Subsampling.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('-i', '--imgpath', default='resources/grid-444.png',
                      help="Input image's path.")
  parser.add_argument('-s', '--subsampling', default='444',
                      choices=['444', '440', '422', '420', '411', '410'],
                      help="Subsampling type.")
  args = parser.parse_args()
  original = cv2.imread(args.imgpath)
  if original is None:
    print('Image not found.')
    return
  cv2.imshow('original', original)
  height, width = original.shape[:2] 
  chroma_subsampling = SUBSAMPLING_TYPES[args.subsampling]
  result = chroma_subsampling(original)
  result = up_sampling(result, width, height)
  mse, psnr = calculate_error(original, result)
  print('Mean Squared Error = ', mse)
  print('Peak Signal to Noise Error = ', psnr)
  cv2.imshow('chroma_subsampling' + args.subsampling, result)
  cv2.waitKey(0)
  cv2.destroyAllWindows()


def chroma_subsampling_factory(a, b):
  """Creates the subsampling function."""
    
  def _subsampling_channel(channel):
    if a == 1 and b == 1:
      return channel
    return channel[::a, ::b]
    
  def _subsampling(img):
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    (y, cr, cb) = cv2.split(ycrcb)
    cv2.imshow('ycrcb', np.hstack((y, cr, cb)))
    crs = _subsampling_channel(cr)
    cbs = _subsampling_channel(cb)
    cv2.imshow('y_result', y)
    cv2.imshow('cr_result', crs)
    cv2.imshow('cb_result', cbs)
    result = decode_sampled(y, crs, cbs, a, b)
    return cv2.cvtColor(result, cv2.COLOR_YCrCb2BGR)
    
  return _subsampling


def decode_sampled(y, cr, cb, a, b):
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
  '444': chroma_subsampling_factory(1, 1),
  '440': chroma_subsampling_factory(2, 1),
  '422': chroma_subsampling_factory(1, 2),
  '420': chroma_subsampling_factory(2, 2),
  '411': chroma_subsampling_factory(1, 4),
  '410': chroma_subsampling_factory(2, 4),
}


def up_sampling(image, new_width, new_height):
  """Up sampling image by repeat."""
  (height, width) = image.shape[:2]
  scale_x = int(new_width / width)
  scale_y = int(new_height / height)
  return np.repeat(np.repeat(image, scale_x, axis=1), scale_y, axis=0)


def calculate_error(original, subsampled):
  height, width = original.shape[:2]
  diff = original.astype(np.float32) - subsampled.astype(np.float32)
  mse = np.sum(diff**2) / (height * width)
  psne = 20 * np.log10(255 / np.sqrt(mse / 3))
  return mse, psne
  
if __name__ == '__main__':
    main()
