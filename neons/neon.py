#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
"""
Generative art practice
https://www.youtube.com/watch?v=BMq2Jrvp9AA&ab_channel=Pixegami
"""
# pylint: disable=W0311
# pylint: disable=W0611
#
# Standard Imports (can be added as needed)
#
import argparse
import ast
from curses import start_color
from datetime import date, datetime
import json
import logging
import os
from pathlib import Path
import sys

#
# Non-standard Imports (can be added as needed)
#
from PIL import Image as image, ImageDraw as imaged, ImageChops as imagec
import random
import colorsys
#
######################################################################
#
# Global variables
#
DEFAULT_LOG_LEVEL = 'WARNING'
DEFAULT_NUM_IMAGE = 4
DEFAULT_PATH = os.path.dirname(os.path.realpath(__file__)) + '/img/'
DEFAULT_SCALE = 2
DEFAULT_SIZE = 256
DEFAULT_PADDING = 24
DEFAULT_THICKNESS_MIN = 2
DEFAULT_THICKNESS_MAX = 32

#
######################################################################
#
# randomize_point()
#
def generate_bg(c1: tuple[int, int, int],
                c2: tuple[int, int, int],
                size: int) -> image:
  """
  Randomize points to draw the lines
  Args:
    c1: first color
    c2: second color
    size: size of the background image
  Returns:
    the gradient color of c2 on top c1
  Raises:
    Nothing
  """

  base = image.new('RGB', size=(size, size), color=c1)
  top = image.new('RGB', size=(size, size), color=c2)
  mask = image.new('L', (size, size))
  mask_data = []
  for i in range(size):
    mask_data.extend([int(255 * (i / size))] * size)
  mask.putdata(mask_data)
  base.paste(top, (0, 0), mask)

  return base

#
######################################################################
#
# randomize_point()
#
def randomize_point(padding_px: int, size_px: int) -> tuple[int, int]:
  """
  Randomize points to draw the lines
    Args:
      padding_px: range from 0-size_px as padding
      size_px: largest possible pixel
  Returns:
      tuple of x,y coordinate within start and (end-start)
  Raises:
      Nothing
  """

  return (random.randint(padding_px, size_px-padding_px), random.randint(padding_px, size_px-padding_px))

#
######################################################################
#
# randomize_color()
#
def randomize_color() -> tuple[int, int, int]:
  """
  Randomize color of the line
    Args:
      Nothing
  Returns:
      tuple of r,g,b values
  Raises:
      Nothing
  """

  # Initialize HSV to be converted to RGB
  h = random.random()
  s = random.uniform(0.5, 1)
  v = random.uniform(0.5, 1)

  # Convert HSV to RGB
  float_rgb = colorsys.hsv_to_rgb(h, s, v)
  r = 255 * float_rgb[0]
  g = 255 * float_rgb[1]
  b = 255 * float_rgb[2]
  return (r, g, b)

#
######################################################################
#
# gradient_color()
#
def gradient_color(c1: tuple[int, int, int],
                  c2: tuple[int, int, int],
                  factor: float) -> tuple[int, int, int]:
  """
  Generate gradient color within start color and end color.
    Args:
      c1: starting color range
      c2: ending color range
      factor: the offset of the end color from the start color
  Returns:
      tuple of r,g,b values
  Raises:
      Nothing
  """

  reciprocal = 1-factor
  r = round((c1[0] * reciprocal) + (c2[0] * factor))
  g = round((c1[1] * reciprocal) + (c2[1] * factor))
  b = round((c1[2] * reciprocal) + (c2[2] * factor))
  return (r, g, b)

#
######################################################################
#
# generate_lines()
#
def generate_lines(num_lines: int,
                  padding_px: int,
                  size_px: int) -> list[tuple[
                                    tuple[int, int],
                                    tuple[int, int]]]:
  """
  Generate num_lines lines to draw on the background
    Args:
      num_lines: number of lines to draw
      padding_px: padding offset from the frame
      size_px: size of the background image
  Returns:
      list of tuples of lines in form [((x1,y1), (x2,y2)), ... ((xn,yn), (xm,ym))]
  Raises:
      Nothing
  """

  line_list = []
  for i in range(num_lines):
    if i == 0:
      pt1 = randomize_point(padding_px, size_px)
      pt2 = randomize_point(padding_px, size_px)
    elif i == num_lines-1:
      pt1 = pt2
      pt2 = randomize_point(padding_px, size_px)
    else:
      pt1 = pt2
      pt2 = randomize_point(padding_px, size_px)

    line_list.append((pt1, pt2))

  return line_list

#
######################################################################
#
# get_point()
#
def get_point(point_list: list[tuple[
                          tuple[int, int],
                          tuple[int, int]]],
              flag: int) -> list[int]:
  """
  Get all the points coordinate into a list
    Args:
      point_list: list of points
      flag: get x coordinate if given '0', and y if given '1'
  Returns:
      a list of either all x or y coordinate from point_list
  Raises:
      Nothing
  """

  point_result = []
  for p1, p2 in point_list:
    point_result.append(p1[flag])
    point_result.append(p1[flag])

  return point_result

#
######################################################################
#
# center_image()
#
def center_image(x: int,
                y: int,
                list_list: list[tuple[
                            tuple[int, int],
                            tuple[int, int]]]) -> list[tuple[
                                                  tuple[int, int],
                                                  tuple[int, int]]]:
  """
  Get all the points coordinate into a list
    Args:
      x: the delta_x value to center the img
      y: the delta_y value to center the img
      list_list: list of original line coordinates
  Returns:
      a list centered coordinates
  Raises:
      Nothing
  """

  lines = []
  for i, coord in enumerate(list_list):
    lines.append(
      ((coord[0][0] - x // 2,
      coord[0][1] - y // 2),
      (coord[1][0] - x // 2,
      coord[1][1] - y // 2)))

  return lines

#
######################################################################
#
# generate_art()
#
def generate_art(img_num: int,
                path_dir: str,
                scale: int,
                target_size: int,
                target_padding: int,
                thickness_min: int,
                thickness_max: int) -> None:
  """
  Main function to generate the art
    Args:
      point_list: list of points
      flag: get x coordinate if given '0', and y if given '1'
  Returns:
      a list of either all x or y coordinate from point_list
  Raises:
      Nothing
  """

  # Background image
  img_size = target_size * scale
  padding = target_padding * scale
  img = generate_bg((0, 0, 0), (0, 0, 0), img_size)

  # Lines variables initilization
  draw = imaged.Draw(img)
  start_color = randomize_color()
  end_color = randomize_color()

  # Generate all lines to draw
  lines = generate_lines(10, padding, img_size)

  # Get the min and max of the all the lines
  x_coord = get_point(lines, 0)
  y_coord = get_point(lines, 1)
  min_x = min(x_coord)
  max_x = max(x_coord)
  min_y = min(y_coord)
  max_y = max(y_coord)

  # Centering the image
  delta_x = min_x - (img_size - max_x)
  delta_y = min_y - (img_size - max_y)
  lines = center_image(delta_x, delta_y, lines)

  # Draw the lines onto the background
  for i in range(len(lines)):
    # Overlay camvas
    overlay_img = generate_bg((0, 0, 0), (0,0,0), img_size)
    overlay_draw = imaged.Draw(overlay_img)


    # Set up parameters and draw
    line_thickness = random.randint(thickness_min*scale, thickness_max*scale)
    color_factor = random.random()
    line_color = gradient_color(start_color, end_color, color_factor)
    overlay_draw.line(lines[i], fill=line_color, width=line_thickness)
    img = imagec.add(img, overlay_img)

  img = img.resize((target_size, target_size), resample=image.ANTIALIAS)
  img.save(f'{path_dir}neon{str(img_num)}.png', quality=95)

#
######################################################################
#
# main()
#
def main():
  """
  Main function
    Args:
      No arg
  Returns:
      Nothing
  Raises:
      Nothing
  """

  # Configure logging and arguments
  args = handle_arguments()
  _clean_loggers(args.log_level.upper())
  logger = _get_logger()
  logger.info("Log level is '%s'", args.log_level.upper())

  img_num = args.img_num
  save_path = args.path
  scale = args.scale
  size = args.size
  padding = args.padding
  tmin = args.tmin
  tmax = args.tmax
  for i in range(img_num):
    generate_art(i, save_path, scale, size, padding, tmin, tmax)

#
######################################################################
# Helper methods
######################################################################
#
# _clean_loggers()
#
def _clean_loggers(log_level: str = 'WARNING'):
  """
  Clean logging messages and set logging format.
  """
  root = logging.getLogger()
  if root.handlers:
      for handler in root.handlers:
          root.removeHandler(handler)
  # try this here
  logging.basicConfig(format='%(asctime)s %(levelname)s:%(name)s.%(funcName)s:%(message)s',
                      level=getattr(logging, log_level.upper()))

#
######################################################################
#
# _get_logger()
#
def _get_logger():
  """
  Get the correct logger by name of current file
  Returns:
      logging.logger: Instance of logger in name of current file
  """
  return logging.getLogger(Path(__file__).resolve().name)

#
######################################################################
#
# handle_arguments()
#
def handle_arguments():
  """
  Handle CLI arguments
  Returns:
      parser.Namespace: Representation of the parsed arguments
  """
  #
  # Handle CLI args
  #
  parser = argparse.ArgumentParser(description=__doc__)

  parser.add_argument('-l', '--log-level',
                      action='store',
                      required=False,
                      choices=["debug", "info", "warning", "error", "critical"],
                      default=DEFAULT_LOG_LEVEL,
                      help='Logging verbosity. Default: %(default)s')

  parser.add_argument('-n', '--img-num',
                      action='store',
                      type=int,
                      required=False,
                      choices=range(1, 101),
                      default=DEFAULT_NUM_IMAGE,
                      help='Number of images to produce. Default: %(default)s')

  parser.add_argument('-p', '--path',
                      action='store',
                      type=str,
                      required=False,
                      default=DEFAULT_PATH,
                      help='Path to store all the images. Default: %(default)s')

  parser.add_argument('--scale',
                      action='store',
                      type=int,
                      required=False,
                      default=DEFAULT_SCALE,
                      help='Size of the image Default: %(default)s')

  parser.add_argument('--size',
                      action='store',
                      type=int,
                      required=False,
                      default=DEFAULT_SIZE,
                      help='Size of the image Default: %(default)s')

  parser.add_argument('--padding',
                      action='store',
                      type=int,
                      required=False,
                      default=DEFAULT_PADDING,
                      help='Size of the image Default: %(default)s')

  parser.add_argument('--tmin',
                      action='store',
                      type=int,
                      required=False,
                      default=DEFAULT_THICKNESS_MIN,
                      help='Size of the image Default: %(default)s')

  parser.add_argument('--tmax',
                      action='store',
                      type=int,
                      required=False,
                      default=DEFAULT_THICKNESS_MAX,
                      help='Size of the image Default: %(default)s')

  return parser.parse_args()

#
######################################################################
#
# Call the main function
#
if __name__ == '__main__':
  main()
