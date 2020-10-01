# Imports
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2
import math

# Function imports
from area_optimization import default_measurement
from img_processing_methods import apply_mask, sharpen, blur
from helper import parse_arguments
# Basic definitions

#
# SETUP
#

args = parse_arguments()
image = cv2.imread(args["image"])
real_width = args["width"]
orig = image.copy()

# Define display window dimensions
height, width = image.shape[:2]
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('jpg', width, height)

measurements = default_measurement(image, real_width)
print(measurements["areas"])
cv2.imshow("Image", measurements["drawn_image"])
cv2.waitKey(0)
