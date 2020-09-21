# IMPORTS
# import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import math

# MIDPOINT


def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


# ARGUMENT PARSING
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to the input image")
ap.add_argument("-w", "--width", type=float, required=True,
                help="width of the left-most object in the image (in inches)")
args = vars(ap.parse_args())

# MASKING
# start convert
# covert anything slightly red into super red
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# lower red
lower_red = np.array([0, 50, 50])
upper_red = np.array([30, 255, 255])

# upper red
lower_red2 = np.array([150, 50, 50])
upper_red2 = np.array([180, 255, 255])

mask = cv2.inRange(hsv, lower_red, upper_red)

# Change image to red where we found brown
image[mask > 0] = (0, 0, 255)

mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

# Change image to red where we found brown
image[mask2 > 0] = (0, 0, 255)
# end convert

# SHARPENING
# sharpen image
kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
image = cv2.filter2D(image, -1, kernel)

# BLURRING
gray = cv2.GaussianBlur(gray, (7, 7), 0)

# GRAYSCALE
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# EDGE DETECTION

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

# DISPLAYING
height, width = image.shape[:2]
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)
cv2.resizeWindow('jpg', width, height)
cv2.imshow("Image", orig2)
cv2.waitKey(0)
