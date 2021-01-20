# Imports
'''
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2
import math

# Function imports
from wound_analysis.api.analysis import optimized_masking_measurement
from wound_analysis.api.processing_helpers import apply_mask, sharpen, blur
from wound_analysis.api.helpers import parse_arguments, display_image
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
'''