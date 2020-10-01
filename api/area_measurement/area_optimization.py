import cv2
import numpy as np

import imutils
from imutils import perspective
from imutils import contours

# Function imports
from img_processing_methods import apply_mask, sharpen, blur, measure_area, draw_contours
from helper import find_sq_ratio, display_image

# Constants import
from constants import default_lower_range, default_upper_range, AREA_UPPER_LIMIT


def default_measurement(image, real_width):
    #
    # Image processing
    #

    original = image.copy()
    _image = image.copy()

    # SHARPEN & BLUR
    display_image(_image)
    #_image = sharpen(_image)
    # _image = blur(_image)

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
    draw_contours(original, cnts, sq_ratio)

    return {"drawn_image": original, "areas": areas}


def optimized_masking_measurement(image, real_width):
    original = image.copy()
    _image = image.copy()
    cur_lower_range = default_lower_range
    cur_upper_range = default_upper_range
    cnts = []
    sq_ratio = find_sq_ratio(_image, real_width)
    for i in range(10):
        # standard image processing
        # reset image each time
        _image = image.copy()
        _image = apply_mask(cur_lower_range, cur_upper_range, _image)
        gray = cv2.cvtColor(_image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 50, 100)
        edged = cv2.dilate(edged, None, iterations=5)
        edged = cv2.erode(edged, None, iterations=3)
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        areas = measure_area(original, cnts, sq_ratio)

        # modify mask, reduce saturation limit
        if areas == []:
            cur_lower_range[0][1] *= 0.8
            cur_lower_range[1][1] *= 0.8
        elif areas[len(areas)-1] > AREA_UPPER_LIMIT:
            cur_lower_range[0][1] *= 1.2
            cur_lower_range[1][1] *= 1.2
        else:
            break

    draw_contours(original, cnts, sq_ratio)
    return {"drawn_image": original, "areas": areas}
