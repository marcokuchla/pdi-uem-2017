#!/usr/bin/python3
import argparse

import cv2
import numpy as np
  

def main():
  parser = argparse.ArgumentParser(
    description='Scale up/down an image.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('input_image_filename', help='Input image filename')
  parser.add_argument('scale_x', type=float, help='X scale')
  parser.add_argument('scale_y', type=float, help='Y scale')
  args = parser.parse_args()
  input_image = cv2.imread(args.input_image_filename)
  if input_image is None:
    error('Image not found!')
  
  output_image = scale(input_image, args.scale_x, args.scale_y)
  cv2.imshow('input', input_image)
  cv2.imshow('output', output_image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def error(msg):
  print(msg)
  exit(1)

def scale(image, scale_x, scale_y):
  if scale_x <= 0 or scale_y <= 0:
    error('Scales must be positive!')
  if scale_x == 1 and scale_y == 1:
    return image
  (in_height, in_width) = image.shape[:2]
  out_height = np.int32(scale_y * in_height)
  out_width = np.int32(scale_x * in_width)
  print('Input image size (WxH):', (in_width, in_height))
  print('Output image size (WxH):', (out_width, out_height))
  rows = np.arange(out_height)
  cols = np.arange(out_width)
  cols_indexes, rows_indexes = np.meshgrid(cols, rows)
  rows_mapping = np.int32(rows_indexes / scale_y)
  cols_mapping = np.int32(cols_indexes / scale_x)
  output_image = image[rows_mapping, cols_mapping]
  return output_image

if __name__=='__main__':
  main()
