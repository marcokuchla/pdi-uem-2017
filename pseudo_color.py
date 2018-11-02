#!/usr/bin/python3
"""Coloring a gray-scaled movie using an user-defined palette."""
import argparse

import cv2
import numpy as np
import imageio

def main():
  """Entry point."""
  parser = argparse.ArgumentParser(
    description="Pseudo-Colorer",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('video', help='Video input')
  parser.add_argument('--gif-out', default='resources/out.gif', help='GIF output name')
  args = parser.parse_args()
  cap = cv2.VideoCapture()
  if not cap.open(args.video):
    print('Could not open video')
    exit(-1)
  video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
  fps = int(cap.get(cv2.CAP_PROP_FPS))
  hues = generate_pseudocolors(video_length)
  writer = imageio.get_writer(args.gif_out, mode='I', fps=fps)
  for i in range(video_length):
    success, frame = cap.read() 
    if not success:
      break
    pallete = generate_pallete(hues[i])
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    color_hls_frame = pallete[gray_frame]
    color_bgr_frame = cv2.cvtColor(color_hls_frame, cv2.COLOR_HLS2BGR)
    color_rgb_frame = cv2.cvtColor(color_bgr_frame, cv2.COLOR_BGR2RGB)
    writer.append_data(color_rgb_frame)
    cv2.imshow('frame', frame)
    cv2.imshow('color', color_bgr_frame)
    key = cv2.waitKey(1)
    if key == ord('q'):
      break
  writer.close()
  cv2.destroyAllWindows()


def generate_pseudocolors(number_frames):
  """Generate pseudo_colors HSL colors."""
  start_hue = np.random.randint(0, 180)
  end_hue = np.random.randint(0, 180)
  hues = np.uint8(np.linspace(start_hue, end_hue, number_frames))
  return hues

def generate_pallete(hue): 
  bottom_half = [(hue, i, 255) for i in range(0, 256, 2)]
  top_half = [(hue, 255, i) for i in range(256, 0, -2)]
  hls_pallete = np.array(bottom_half + top_half, dtype=np.uint8)
  return hls_pallete


def show_palletes(palletes):
  for p, i in enumerate(palletes):
    image = pallete.reshape((255, 1, 3))
    image = np.repeat(image, 50, axis=1)
    cv2.imshow('pallete' + str(i), cv2.cvtColor(image, cv2.COLOR_HLS2BGR))

if __name__ == '__main__':
    main()
