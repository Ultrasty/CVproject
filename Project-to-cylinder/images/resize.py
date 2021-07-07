import imutils
import cv2

# construct the argument parse and parse the arguments

for i in range(5):

    imageA = cv2.imread("a"+str(i+1)+".jpg")

    imageA = imutils.resize(imageA, height=1100)

    cv2.imwrite(str(i+1)+".jpg", imageA)


