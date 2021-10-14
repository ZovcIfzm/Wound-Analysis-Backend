import cv2
import numpy as np

import imutils
from imutils import perspective
from imutils import contours

import zipfile

# Function imports

import processing_helpers
import helpers
from constants import DEF_LOWER_RANGE, DEF_UPPER_RANGE, AREA_UPPER_LIMIT

'''
import wound_analysis.api.processing_helpers as processing_helpers
import wound_analysis.api.helpers as helpers

# Constants import
from wound_analysis.api.constants import DEF_LOWER_RANGE, DEF_UPPER_RANGE, AREA_UPPER_LIMIT
'''


def measurement(image, rec_image, sq_ratio, lower_range, upper_range):
    overlay_img = rec_image.copy()
    _image = image.copy()
    _image = processing_helpers.apply_mask(lower_range, upper_range, _image)
    gray = cv2.cvtColor(_image, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 50, 100)

    edged = cv2.dilate(edged, None, iterations=2)
    edged = cv2.erode(edged, None, iterations=2)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnts)
    try:
        (cnts, _) = contours.sort_contours(cnts)
    except:
        return {"drawn_image": overlay_img,
                "areas": [],
                "lower_range": lower_range,
                "upper_range": upper_range,
                "sq_ratio": sq_ratio,
                "error": True}

    areas = processing_helpers.measure_area(cnts, sq_ratio)
    # helpers.display_image(edged)
    helpers.draw_contours(overlay_img, cnts, sq_ratio)

    return {"drawn_image": overlay_img,
            "areas": areas,
            "lower_range": lower_range,
            "upper_range": upper_range,
            "edged_image": edged,
            "sq_ratio": sq_ratio,
            "error": False}


def custom_measure(image, rec_image, sq_ratio, mask):
    cur_lower_range = np.array(
        [np.array(mask["lower_range"]["first"]), np.array(mask["lower_range"]["second"])])
    cur_upper_range = np.array(
        [np.array(mask["upper_range"]["first"]), np.array(mask["upper_range"]["second"])])

    data = measurement(image, rec_image, sq_ratio,
                       cur_lower_range, cur_upper_range)

    if data["error"] is False:
        return {"drawn_image": helpers.convertNumpyImageToString(data["drawn_image"]),
                "edged_image": helpers.convertNumpyImageToString(data["edged_image"]),
                "areas": data["areas"],
                "lower_range": cur_lower_range.tolist(),
                "upper_range": cur_upper_range.tolist(),
                "sq_ratio": sq_ratio,
                "error": False}
    else:
        return {"error": True, "error_message": "Can't find wounds"}


def grid_measurement(image, mask, width=2.54, manual=False):
    masks = processing_helpers.extend_mask_search(mask)
    matrix = []
    try:
        sq_ratio = None
        rec_image = None
        if not manual:
            ratio, rec_image = processing_helpers.find_real_size(image, width)
            sq_ratio = ratio*ratio
        else:
            sq_ratio = helpers.find_sq_ratio(image, width)
            rec_image = image

        for i in range(3):
            row = []
            for j in range(3):
                obj = custom_measure(image, rec_image, sq_ratio, masks[i][j])
                row.append(obj)
            matrix.append(row)
    except:
        matrix = []
        for i in range(3):
            row = []
            for j in range(3):
                row.append(
                    {"error": True, "error_message": "Can't identify green line. Please set to manual."})
            matrix.append(row)

    return matrix


def zip_measurement(image, mask, width=2.54, manual=False):
    try:
        sq_ratio = None
        rec_image = None
        if not manual:
            ratio, rec_image = processing_helpers.find_real_size(image, width)
            sq_ratio = ratio*ratio
        else:
            sq_ratio = helpers.find_sq_ratio(image, width)
            rec_image = image
        return_object = custom_measure(image, rec_image, sq_ratio, mask)
        return return_object
    except:
        return {"error": True, "error_message": "Can't identify green line."}


def manual_area_adjustment(prev_data, increase_sat):

    if increase_sat:
        prev_data["lower_range"][0][1] *= 1.05
        prev_data["lower_range"][1][1] *= 1.05
    else:
        prev_data["lower_range"][0][1] *= 0.95
        prev_data["lower_range"][1][1] *= 0.95

    data = measurement(
        prev_data["original_image"], prev_data["sq_ratio"], prev_data["lower_range"], prev_data["upper_range"])
    # if not data["error"]:
    #    helpers.display_image(data["drawn_image"])
    return data
