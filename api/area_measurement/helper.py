import argparse
import numpy as np


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
