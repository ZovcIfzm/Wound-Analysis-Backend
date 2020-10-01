import cv2
import numpy as np

import imutils
from imutils import perspective
from imutils import contours

# Function imports
from img_processing_methods import apply_mask, sharpen, blur, measure_area
from helper import find_sq_ratio

# Constants import
from constants import default_lower_range, default_upper_range


def default_measurement(image, real_width):
    #
    # Image processing
    #

    original = image.copy()
    _image = image.copy()

    # SHARPEN & BLUR
    _image = sharpen(_image)
    _image = blur(_image)

    # Apply Mask
    _image = apply_mask(default_lower_range, default_upper_range, _image)

    # Convert to grayscale
    gray = cv2.cvtColor(_image, cv2.COLOR_BGR2GRAY)

    # perform edge detection, then perform a dilation + erosion to
    # close gaps in between object edges
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=5)
    edged = cv2.erode(edged, None, iterations=3)

    # find contours in the edge map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    sq_ratio = find_sq_ratio(_image, real_width)

    areas = measure_area(original, cnts, sq_ratio)

    return {"drawn_image": original, "areas": areas}
