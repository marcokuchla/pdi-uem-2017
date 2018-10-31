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
  def rotate_point(x, y):
    rotated_x = cosine * (x - x_center) - sine * (y - y_center) + x_center
    rotated_y = sine * (x - x_center) + cosine * (y - y_center) + y_center
    return rotated_x, rotated_y
  
  def distance_points(p0, p1):
    (x0, y0) = p0
    (x1, y1) = p1
    euclidean_distance = np.linealg.norm([[x0, x1],
                                          [y0, y1]])
    return euclidean_distance

  def makeBorders():
    min_x, min_y = minimas
    max_x, max_y = maximas
    top = 0 if min_y >= 0 else -min_y
    left = 0 if min_x >=0 else -min_x
    bottom = 0 if max_y < height else max_y - (height - 1)
    right = 0 if max_x < width else max_x - (width - 1)
    return cv2.copyMakeBorder(image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=0)

  angle_degree %= 360
  if angle_degree == 0:
    print('Doing nothing, angle is zero!')
    return image
  print('Input shape:\n', image.shape)
  height, width = image.shape[:2]
  x_center = (width - 1) / 2
  y_center = (height - 1) / 2
  print('Center = ({},{})'.format(x_center, y_center))
  angle_radian = np.radians(angle_degree)
  cosine = np.cos(angle_radian)
  sine = np.sin(angle_radian)
  boundaries = np.array([[        0, 0],
                         [width - 1, 0],
                         [width - 1, height - 1], 
                         [        0, height -1 ]])
  print('Input Boundaries:\n', boundaries)
  rotated_boundaries = [rotate_point(x, y) for x, y in boundaries]
  print('Rotated Boundaries:\n', rotated_boundaries)

  def func(x):
    new_x = np.floor(x) if x < 0 else np.ceil(x)
    return new_x

  maximas = np.int32(np.ceil(np.max(rotated_boundaries, 0)))
  minimas = np.int32(np.floor(np.min(rotated_boundaries, 0)))
  print('TopLeft = ({}, {}) BottomRight = ({}, {})'.format(minimas[0], minimas[1], maximas[0], maximas[1]))
  cosine = np.cos(-angle_radian)
  sine = np.sin(-angle_radian)
  rotated_width = maximas[0] - minimas[0]
  rotated_height = maximas[1] - minimas[1]
  print('New Size: width: {}, height: {}'.format(rotated_width, rotated_height))
  cols_indexes, rows_indexes = np.meshgrid(np.arange(minimas[0], maximas[0] + 1), np.arange(minimas[1], maximas[1] + 1))
  cols_mapping = cosine * (cols_indexes - x_center) - sine * (rows_indexes - y_center) + x_center
  rows_mapping = sine * (cols_indexes - x_center) + cosine * (rows_indexes - y_center) + y_center
  print('cols mapping:\n', cols_mapping)
  print('rows_mapping:\n', rows_mapping)
  cols_mapping = np.int32(np.floor(cols_mapping))
  rows_mapping = np.int32(np.floor(rows_mapping))
  print('cols mapping:\n', cols_mapping)
  print('rows_mapping:\n', rows_mapping)
  output_image = np.zeros((rotated_height, rotated_width, 3), np.uint8)
  print(output_image.shape)
  for i, j, x, y in zip(cols_indexes.reshape(-1), rows_indexes.reshape(-1), cols_mapping.reshape(-1), rows_mapping.reshape(-1)):
    if 0 <= x < image.shape[1] and 0 <= y < image.shape[0]:
      output_image[i, j] = image[x, y]
  output_image = output_image[:image.shape[0], :image.shape[1]]
  print('Ouput shape:\n', output_image.shape)
  return output_image

   
if __name__=='__main__':
  main()
