#!/usr/bin/python3
import argparse

import cv2
import numpy as np
  

def main():
  parser = argparse.ArgumentParser(
    description='Rotates an image.',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('input_image_filename', help='Input image filename')
  parser.add_argument('angle', type=float, help='Angle of rotation in degree')
  args = parser.parse_args()
  input_image = cv2.imread(args.input_image_filename)
  if input_image is None:
    error('Image not found!') 
  output_image = rotate(input_image, args.angle)
  cv2.imshow('input', input_image)
  cv2.imshow('output', output_image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def error(msg):
  print(msg)
  exit(1)


def rotate(image, angle_degree):
  angle_degree %= 360
  if angle_degree == 0:
    print('Doing nothing, angle is zero!')
    return image
  
  angle_radian = np.radian(angle_degree)

   
if __name__=='__main__':
  main()
