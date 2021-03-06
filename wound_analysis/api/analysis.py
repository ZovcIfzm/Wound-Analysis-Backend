import cv2
import numpy as np

import imutils
from imutils import perspective
from imutils import contours

import zipfile

# Function imports
import wound_analysis.api.processing_helpers as processing_helpers
import wound_analysis.api.helpers as helpers

# Constants import
from wound_analysis.api.constants import DEF_LOWER_RANGE, DEF_UPPER_RANGE, AREA_UPPER_LIMIT

def measurement(image, sq_ratio, lower_range, upper_range):
    overlay_img = image.copy()
    _image = image.copy()
    _image = processing_helpers.apply_mask(lower_range, upper_range, _image)
    gray = cv2.cvtColor(_image, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=9)
    edged = cv2.erode(edged, None, iterations=7)
    
    edged = cv2.dilate(edged, None, iterations=1)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    try:
        (cnts, _) = contours.sort_contours(cnts)
    except:
        return {"drawn_image": overlay_img,
            "areas": [],
            "lower_range": lower_range,
            "upper_range": upper_range,
            "original_image": image,
            "sq_ratio": sq_ratio,
            "error": False}
        
    
    areas = processing_helpers.measure_area(cnts, sq_ratio)
    #helpers.display_image(edged)
    helpers.draw_contours(overlay_img, cnts, sq_ratio)

    return {"drawn_image": overlay_img,
            "areas": areas,
            "lower_range": lower_range,
            "upper_range": upper_range,
            "original_image": image,
            "edged_image": edged,
            "sq_ratio": sq_ratio,
            "error": False}


def optimized_masking_measurement(image, real_width):
    cur_lower_range = DEF_LOWER_RANGE
    cur_upper_range = DEF_UPPER_RANGE
    sq_ratio = helpers.find_sq_ratio(image, real_width)
    for i in range(10):
        data = measurement(image, sq_ratio, cur_lower_range, cur_upper_range)
        areas = data["areas"]
        if areas == []:
            cur_lower_range[0][1] *= 0.9
            cur_lower_range[1][1] *= 0.9
            print("increasing num")
        elif areas[len(areas)-1] > AREA_UPPER_LIMIT:
            cur_lower_range[0][1] *= 1.1
            cur_lower_range[1][1] *= 1.1
            print("decreasing num")
        else:
            break
        
    if data is not {}:
        return {"drawn_image": data["drawn_image"],
                "areas": areas,
                "lower_range": cur_lower_range,
                "upper_range": cur_upper_range,
                "original_image": image,
                "sq_ratio": sq_ratio,
                "error": False}
    else:
        return {"error": True}

def custom_measure(image, sq_ratio, mask):
    cur_lower_range = np.array([np.array(mask["lower_range"]["first"]), np.array(mask["lower_range"]["second"])])
    cur_upper_range = np.array([np.array(mask["upper_range"]["first"]), np.array(mask["upper_range"]["second"])])
    
    #sq_ratio = helpers.find_sq_ratio(image, real_width)
    '''
    for i in range(10):
        data = measurement(image, sq_ratio, cur_lower_range, cur_upper_range)
        areas = data["areas"]
        if areas == []:
            cur_lower_range[0][1] *= 0.9
            cur_lower_range[1][1] *= 0.9
            print("increasing num")
        elif areas[len(areas)-1] > AREA_UPPER_LIMIT:
            cur_lower_range[0][1] *= 1.1
            cur_lower_range[1][1] *= 1.1
            print("decreasing num")
        else:
            break
    '''
    
    data = measurement(image, sq_ratio, cur_lower_range, cur_upper_range) 
    areas = data["areas"]
    if data is not {}:
        return {"drawn_image": helpers.convertNumpyImageToString(data["drawn_image"]),
                "edged_image": helpers.convertNumpyImageToString(data["edged_image"]),
                "areas": areas,
                "lower_range": cur_lower_range.tolist(),
                "upper_range": cur_upper_range.tolist(),
                "sq_ratio": sq_ratio,
                "error": False}
    else:
        return {"error": True}

def grid_measurement(image, mask):
    masks = processing_helpers.extend_mask_search(mask)
    ratio, image = processing_helpers.find_real_size(image, 2.54)
    sq_ratio = ratio*ratio
    matrix = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append(custom_measure(image, sq_ratio, masks[i][j]))
        matrix.append(row)

    return matrix
    '''
    return custom_measure(image, real_width, mask)
    '''

def zip_measurement(image, mask):
    try:
        ratio, image = processing_helpers.find_real_size(image, 2.54)
        sq_ratio = ratio*ratio    
        return_object = custom_measure(image, sq_ratio, mask)
        return return_object
    except:
        return "Error in image measurement"

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
