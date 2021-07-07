# USAGE
# python stitch.py --first images/bryce_left_01.png --second images/bryce_right_01.png 

# import the necessary packages
from pyimagesearch.panorama import Stitcher
import argparse
import imutils
import cv2
import matplotlib.pyplot as plt

# construct the argument parse and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-f", "--first", required=True,
#                 help="path to the first image")
# ap.add_argument("-s", "--second", required=True,
#                 help="path to the second image")
# args = vars(ap.parse_args())

# load the two images and resize them to have a width of 400 pixels
# (for faster processing)
imageA = cv2.imread("1.jpg")
imageB = cv2.imread("2.jpg")
imageC = cv2.imread("3.jpg")
imageA = imutils.resize(imageA, height=400)
imageB = imutils.resize(imageB, height=400)
imageC = imutils.resize(imageC, height=400)

# stitch the images together to create a panorama
stitcher = Stitcher()
(result, vis) = stitcher.stitch([imageA, imageB], showMatches=True)
print(result)
cv2.imshow('result', result)


(result, vis) = stitcher.stitch([result, imageC], showMatches=True)
cv2.imshow('result', result)


cv2.waitKey(0)
