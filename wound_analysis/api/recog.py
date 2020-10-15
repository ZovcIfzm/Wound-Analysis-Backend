# Imports
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2
import math

# Function imports
from area_optimization import default_measurement, optimized_masking_measurement
from img_processing_methods import apply_mask, sharpen, blur
from helper import parse_arguments, display_image
# Basic definitions

#
# SETUP
#

args = parse_arguments()
image = cv2.imread(args["image"])
real_width = args["width"]
orig = image.copy()

data = optimized_masking_measurement(image, real_width)
# print(data["areas"])
display_image(data["drawn_image"])
