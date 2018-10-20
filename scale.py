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
  if args.scale_x <= 0 or args.scale_y <= 0:
    error('Scales must be positive!')
  print('Input image shape:', input_image.shape)
  scales = np.array([args.scale_x, args.scale_y, 1])
  output_shape = np.int32(scales * input_image.shape)
  print('Output image shape:', output_shape)
  rows = np.arange(output_shape[0])
  cols = np.arange(output_shape[1])
  rows_indexes, cols_indexes = np.meshgrid(cols, rows)
  rows_mapping = np.int32(np.floor(rows_indexes / scales[0]))
  cols_mapping = np.int32(np.floor(cols_indexes / scales[1]))
  output_image = input_image[cols_mapping, rows_mapping]
  cv2.imshow('input', input_image)
  cv2.imshow('output', output_image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def error(msg):
  print(msg)
  exit(1)

if __name__=='__main__':
  main()
