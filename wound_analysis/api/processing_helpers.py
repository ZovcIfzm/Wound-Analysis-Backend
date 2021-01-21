import cv2
import numpy as np
from scipy.spatial import distance as dist

import wound_analysis.api.constants as k
import copy

def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


def apply_mask(lower_range, upper_range, image):
    # Convert image to hsv file
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_mask = cv2.inRange(hsv, lower_range[0], upper_range[0])
    upper_mask = cv2.inRange(hsv, lower_range[1], upper_range[1])
    mask = cv2.bitwise_or(lower_mask, upper_mask)
    image = cv2.bitwise_and(image, image, mask=mask)
    image[mask > 0] = (255, 255, 255)

    return image


def sharpen(image):
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    return cv2.filter2D(image, -1, kernel)


def blur(image):
    return cv2.GaussianBlur(image, (3, 3), 0)


def measure_area(contours, sq_ratio):
    areas = []
    for cont in contours:
        cont_area = cv2.contourArea(cont)/sq_ratio
        # if the contour is not sufficiently large, ignore it
        if cont_area < k.AREA_LOWER_LIMIT:
            continue

        areas.append(cont_area)
    return areas

def extend_mask_search(mask):
    lower_mask_one = np.array(mask["lower_range"]["first"])
    lower_mask_two = np.array(mask["lower_range"]["second"])
    upper_mask_one = np.array(mask["upper_range"]["first"])
    upper_mask_two = np.array(mask["upper_range"]["second"])
    '''
    step_dictionary = {
        "Sat_0": -k.SAT_STEP_3,
        "Sat_1": -k.SAT_STEP_2,
        "Sat_2": -k.SAT_STEP_1,
        "Sat_3": 0,
        "Sat_4": k.SAT_STEP_1,
        "Sat_5": k.SAT_STEP_2,
        "Sat_6": k.SAT_STEP_3,
        "Val_0": -k.VAL_STEP_3,
        "Val_1": -k.VAL_STEP_2,
        "Val_2": -k.VAL_STEP_1,
        "Val_3": 0,
        "Val_4": k.VAL_STEP_1,
        "Val_5": k.VAL_STEP_2,
        "Val_6": k.VAL_STEP_3
    }
    
    step_dictionary = {
        "Sat_0": -k.SAT_STEP_2,
        "Sat_1": -k.SAT_STEP_1,
        "Sat_2": 0,
        "Sat_3": k.SAT_STEP_1,
        "Sat_4": k.SAT_STEP_2,
        "Val_0": -k.VAL_STEP_2,
        "Val_1": -k.VAL_STEP_1,
        "Val_2": 0,
        "Val_3": k.VAL_STEP_1,
        "Val_4": k.VAL_STEP_2,
    }
    '''
    step_dictionary = {
        "Sat_0": -k.SAT_STEP_3,
        "Sat_1": 0,
        "Sat_2": k.SAT_STEP_3,
        "Val_0": -k.VAL_STEP_3,
        "Val_1": 0,
        "Val_2": k.VAL_STEP_3
    }
    masks = {
        "lower_range": {
            "first": None,
            "second": None
        },
        "upper_range": {
            "first": None,
            "second": None,
        }
        
    }
    masks["lower_range"]["first"] = lower_mask_one
    masks["lower_range"]["second"] = lower_mask_two
    masks["upper_range"]["first"] = upper_mask_one
    masks["upper_range"]["second"] = upper_mask_two
    
    matrix = []
    for i in range(3):
        row = []
        for j in range(3):
            new_mask = copy.deepcopy(masks)
            new_mask["upper_range"]["first"][1] += step_dictionary["Sat_" + str(i)]
            new_mask["upper_range"]["first"][2] += step_dictionary["Val_" + str(j)]
            new_mask["upper_range"]["second"][1] += step_dictionary["Sat_" + str(i)]
            new_mask["upper_range"]["second"][2] += step_dictionary["Val_" + str(j)]
            row.append(copy.deepcopy(new_mask))
        matrix.append(copy.deepcopy(row))

    return matrix
    '''
    for i, row in enumerate(matrix):
        for j, col in enumerate(row):
            print(matrix[i][j])
    '''

if __name__ == "__main__":
    mask = {
        "lower_range": {
            "first": [0, 100, 20],
            "second": [150, 100, 20]
        },
        "upper_range": {
            "first": [30, 255, 177],
            "second": [180, 255, 177]
        }
    }
    extend_mask_search(mask)