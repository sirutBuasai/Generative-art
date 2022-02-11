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
from PIL import Image as image, ImageDraw as imaged
import random
#
######################################################################
#
# Global variables
#
DEFAULT_LOG_LEVEL = 'WARNING'

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
 
  generate_art()

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

  return parser.parse_args()

def randomize_point(start_size, end_size):
  """
  Randomize points to draw the lines
    Args:
      start_size: range from 0-end_size as padding
      end_size: largest possible pixel
  Returns:
      tuple of x,y coordinate within start and (end-start)
  Raises:
      Nothing
  """

  return (random.randint(start_size, end_size-start_size), random.randint(start_size, end_size-start_size))

def randomize_color():
  """
  Randomize color of the line
    Args:
      Nothing
  Returns:
      tuple of r,g,b values
  Raises:
      Nothing
  """

  return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def gradient_color(start, end, factor):
  """
  Generate gradient color within start color and end color.
    Args:
      start: starting color range
      end: ending color range
      factor: the offset of the end color from the start color
  Returns:
      tuple of r,g,b values
  Raises:
      Nothing
  """

  reciprocal = 1-factor
  r = round((start[0] * reciprocal) + (end[0] * factor))
  g = round((start[1] * reciprocal) + (end[1] * factor))
  b = round((start[2] * reciprocal) + (end[2] * factor))
  return (r, g, b)

def get_point(point_list, flag):
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

def generate_art():
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

  # Base image
  img_size = 128
  padding = 12
  img_bg_color = (255, 255, 255)
  img = image.new('RGB', size=(img_size, img_size), color=img_bg_color)
  
  # Lines variables initilization
  draw = imaged.Draw(img)
  start_color = randomize_color()
  end_color = randomize_color()

  # Generate all points
  points = []
  for i in range(10):
    if i == 0:
      pt1 = randomize_point(padding, img_size)
      pt2 = randomize_point(padding, img_size)
    elif i == 9:
      pt1 = pt2
      pt2 = randomize_point(padding, img_size)
    else:
      pt1 = pt2
      pt2 = randomize_point(padding, img_size)

    points.append((pt1, pt2))

  # Get the min and max of the points
  x_coord = get_point(points, 0)
  y_coord = get_point(points, 1)
  min_x = min(x_coord)
  max_x = max(x_coord)
  min_y = min(y_coord)
  max_y = max(y_coord)

  # Centering the image
  delta_x = min_x - (img_size - max_x)
  delta_y = min_y - (img_size - max_y)
  lines = []
  for i, tuple in enumerate(points):
    lines.append(
      ((tuple[0][0] - delta_x // 2,
      tuple[0][1] - delta_y // 2),
      (tuple[1][0] - delta_x // 2,
      tuple[1][1] - delta_y // 2)))

  for i in range(len(points)):
    # Setp up parameters and draw
    line_thickness = random.randint(1,10)
    line_xy = lines[i]
    color_factor = random.random()
    line_color = gradient_color(start_color, end_color, color_factor)
    draw.line(line_xy, fill=line_color, width=line_thickness)

  img.save('test_image.png', quality=95)

#
######################################################################
#
# Call the main function
#
if __name__ == '__main__':
  main()
