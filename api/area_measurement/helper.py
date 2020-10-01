import argparse
import numpy as np
import cv2


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
