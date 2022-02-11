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
  return (random.randint(start_size, end_size-start_size), random.randint(start_size, end_size-start_size))

def randomize_color():
  return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def gradient_color(start, end, factor):
  reciprocal = 1-factor
  r = (start[0] * reciprocal) + (end[0] * factor)
  g = (start[1] * reciprocal) + (end[1] * factor)
  b = (start[2] * reciprocal) + (end[2] * factor)
  return (r, g, b)

def generate_art():
  # Base image
  img_size = 128
  padding = 12
  img_bg_color = (255, 255, 255)
  img = image.new('RGB', size=(img_size, img_size), color=img_bg_color)
  
  # Draw lines over background
  draw = imaged.Draw(img)
  rand1 = randomize_point(padding, img_size)
  rand2 = randomize_point(padding, img_size)
  line_thickness = 1
  dec = False
  start_color = randomize_color()
  end_color = randomize_color()

  for i in range(10):

    # Connect the start of new line to the end of old line
    if i == 0:
      pt1, pt2 = rand1, rand2
    elif i == 9:
      pt1 = pt2
      pt2 = rand1
    else:
      pt1 = pt2
      pt2 = randomize_point(padding, img_size)

    # Vary line thickness
    if line_thickness > 5:
      dec = True
    if dec: 
      line_thickness -=1 
    else: 
      line_thickness += 1

    line_xy = (pt1, pt2)
    color_factor = random.randint(0,1)
    line_color = gradient_color(start_color, end_color, color_factor)
    draw.line(line_xy, fill=line_color, width=line_thickness)

  img.save('test_image3.png', quality=95)

#
######################################################################
#
# Call the main function
#
if __name__ == '__main__':
  main()
