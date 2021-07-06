import base64
import numpy as np
from pyimagesearch.panorama import Stitcher
import imutils
import cv2


def cv_stitching(img_l, img_r):
    img_l_decode = base64.b64decode(img_l)
    img_r_decode = base64.b64decode(img_r)
    img_l_array = np.frombuffer(img_l_decode, np.uint8)  # 转换np序列
    imageA = cv2.imdecode(img_l_array, cv2.COLOR_BGR2RGB)  # 转换Opencv格式
    img_r_array = np.frombuffer(img_r_decode, np.uint8)  # 转换np序列
    imageB = cv2.imdecode(img_r_array, cv2.COLOR_BGR2RGB)  # 转换Opencv格式
    imageA = imutils.resize(imageA, width=400)
    imageB = imutils.resize(imageB, width=400)
    stitcher = Stitcher()
    (result, vis) = stitcher.stitch([imageA, imageB], showMatches=True)
    image = cv2.imencode('.jpg', result)[1]
    base64_data = str(base64.b64encode(image))[2:-1]
    return base64_data
