import cv2
import numpy as np
from scipy.spatial import distance as dist

import wound_analysis.api.constants as k
import copy

from imutils import perspective
from imutils import contours
import imutils

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

def find_real_size(img, width):
    # load the image, convert it to grayscale, and blur it slightly
    image = img.copy()
    overlay_img = img.copy()

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, (20,60,60), (50,140,170))
    image = cv2.bitwise_and(image, image, mask=mask)
    #image[mask > 0] = (255, 255, 255)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    # perform edge detection, then perform a dilation + erosion to
    # close gaps in between object edges
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    # find contours in the edge map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # sort the contours from left-to-right and initialize the
    # 'pixels per metric' calibration variable
    (cnts, _) = contours.sort_contours(cnts)
    pixelsPerMetric = None
    # loop over the contours individually
    orig = overlay_img.copy()
    for c in cnts:
        # if the contour is not sufficiently large, ignore it
        if cv2.contourArea(c) < 10000:
            continue
        # compute the rotated bounding box of the contour
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        # order the points in the contour such that they appear
        # in top-left, top-right, bottom-right, and bottom-left
        # order, then draw the outline of the rotated bounding
        # box
        
        box = perspective.order_points(box)
        
        cv2.drawContours(orig, [box.astype("int")], -1, (255, 0, 0), 2)
        # Also draw for returned image (normal image + lines)
        cv2.drawContours(overlay_img, [box.astype("int")], -1, (255, 0, 0), 2)

        # loop over the original points and draw them
        for (x, y) in box:
            cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)
        
        # unpack the ordered bounding box, then compute the midpoint
        # between the top-left and top-right coordinates, followed by
        # the midpoint between bottom-left and bottom-right coordinates
        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)
        # compute the midpoint between the top-left and top-right points,
        # followed by the midpoint between the top-righ and bottom-right
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)
        

        # draw the midpoints on the image
        cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)
        # draw lines between the midpoints
        cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
            (255, 0, 255), 2)
        cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
            (255, 0, 255), 2)
        
        # compute the Euclidean distance between the midpoints
        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
        # if the pixels per metric has not been initialized, then
        # compute it as the ratio of pixels to supplied metric
        # (in this case, inches)
        if dA > dB:
            pixelsPerMetric = dA / width
        else:
            pixelsPerMetric = dB / width

        # compute the size of the object
        dimA = dA / pixelsPerMetric
        dimB = dB / pixelsPerMetric
        

        # draw the object sizes on the image
        cv2.putText(orig, "{:.1f}u".format(dimB),
            (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
            0.65, (255, 255, 255), 2)
        cv2.putText(orig, "{:.1f}u".format(dimA),
            (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
            0.65, (255, 255, 255), 2)

        # show the output image
        #_orig = cv2.resize(orig, (1250,1250))
        #cv2.imshow("Image", _orig) 
        #cv2.waitKey(0)

    return pixelsPerMetric, orig


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