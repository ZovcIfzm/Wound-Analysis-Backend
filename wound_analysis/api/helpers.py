import argparse
import numpy as np
import cv2
import base64

import wound_analysis.api.constants as k


def parse_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
                    help="path to the input image")
    ap.add_argument("-w", "--width", type=float, required=True,
                    help="width of the left-most object in the image (in inches)")
    return vars(ap.parse_args())


def find_sq_ratio(image, real_width):
    img_width = image.shape[:2][1]
    return np.square(img_width/real_width)


def display_image(image):
    height, width = image.shape[:2]
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('jpg', width, height)
    cv2.imshow("Image", image)
    cv2.waitKey(0)


def display_overlay(image, contours, sq_ratio):
    height, width = image.shape[:2]
    cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('jpg', width, height)

    _image = image.copy()
    draw_contours(_image, contours, sq_ratio)

    cv2.imshow("Image", _image)
    cv2.waitKey(0)


def draw_contours(image_background, contours, sq_ratio):
    for cont in contours:
        cont_area = cv2.contourArea(cont)/sq_ratio

        # if the contour is not sufficiently large, ignore it
        if cont_area < k.AREA_LOWER_LIMIT:
            continue

        cv2.drawContours(image_background, cont, -1, (0, 255, 0), 2)


def convertStringToNumpyArray(mask_string):
    string_list = list(mask_string.split(','))
    number_list = [int(str) for str in string_list]
    numpy = np.array(number_list)
    return numpy

def convertNumpyImageToString(numpy_image):
    _, im_arr = cv2.imencode('.jpg', numpy_image)  # im_arr: image in Numpy one-dim array format.
    base64_bytes = base64.b64encode(im_arr)
    jpg_as_string = "data:image/jpg;base64," + base64_bytes.decode('utf-8')
    return jpg_as_string

def dayMaskMapper(day):
    if day == 0:
        return k.A_LR, k.A_UR
    elif day == 1:
        return k.B_LR, k.B_UR
    else:
        return k.C_LR, k.C_UR