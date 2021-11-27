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
        # if cont_area < k.AREA_LOWER_LIMIT:
        #    continue

        areas.append(cont_area)
    return areas


def extend_mask_search(mask):
    lower_mask_one = np.array(mask["lower_range"]["first"])
    lower_mask_two = np.array(mask["lower_range"]["second"])
    upper_mask_one = np.array(mask["upper_range"]["first"])
    upper_mask_two = np.array(mask["upper_range"]["second"])

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
            new_mask["lower_range"]["first"][1] += step_dictionary["Sat_" +
                                                                   str(i)]
            new_mask["lower_range"]["first"][2] += step_dictionary["Val_" +
                                                                   str(j)]
            new_mask["lower_range"]["second"][1] += step_dictionary["Sat_" +
                                                                    str(i)]
            new_mask["lower_range"]["second"][2] += step_dictionary["Val_" +
                                                                    str(j)]
            row.append(copy.deepcopy(new_mask))
        matrix.append(copy.deepcopy(row))

    return matrix


def find_real_size(img, width, lineLowerBound=(40, 60, 60)):
    # load the image, convert it to grayscale, and blur it slightly
    image = img.copy()
    overlay_img = img.copy()

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lineLowerBound, (110, 255, 255))
    image = cv2.bitwise_and(image, image, mask=mask)
    # image[mask > 0] = (255, 255, 255)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    # perform edge detection, then perform a dilation + erosion to
    # close gaps in between object edges
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    # find contours in the edge map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_NONE)
    cnts = imutils.grab_contours(cnts)
    # sort the contours from left-to-right and initialize the
    # 'pixels per metric' calibration variable
    (cnts, _) = contours.sort_contours(cnts)
    pixelsPerMetric = None
    # loop over the contours individually
    orig = overlay_img.copy()
    for c in cnts:
        # if the contour is not sufficiently large, ignore it
        if cv2.contourArea(c) < 1000:
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

        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)
        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

        # check that this is the correct line:
        '''
        if not (dA/dB > width*2*0.8 or dB/dA > width*2*0.8):
            print("continued", dA/dB, dB/dA)
            continue
        else:
            print(dA/dB, dB/dA)
        '''

        cv2.drawContours(orig, [box.astype("int")], -1, (255, 0, 0), 1)
        cv2.drawContours(overlay_img, [box.astype("int")], -1, (255, 0, 0), 1)

        if dA > dB:
            pixelsPerMetric = dA / width
        else:
            pixelsPerMetric = dB / width

        # compute the size of the object
        dimA = dA / pixelsPerMetric
        dimB = dB / pixelsPerMetric

        # draw the object sizes on the image
        if (dA > dB):
            cv2.putText(orig, "{:.2f} cm".format(dimA),
                        (int(tltrX - 15), int(tltrY - 10)
                         ), cv2.FONT_HERSHEY_SIMPLEX,
                        0.65, (255, 0, 0), 2)
        else:
            cv2.putText(orig, "{:.2f} cm".format(dimB),
                        (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                        0.65, (255, 0, 0), 2)

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
