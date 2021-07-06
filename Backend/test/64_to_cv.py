import base64
import numpy as np
import cv2
from PIL import Image
import io
import PIL

img_file = open('images/bryce_left_01.png', 'rb')  # 二进制打开图片文件
img_b64encode = base64.b64encode(img_file.read())  # base64编码
print(img_b64encode)
img_file.close()  # 文件关闭

img_b64decode = base64.b64decode(img_b64encode)  # base64解码

img_array = np.frombuffer(img_b64decode, np.uint8)  # 转换np序列
img = cv2.imdecode(img_array, cv2.COLOR_BGR2RGB)  # 转换Opencv格式
print(img)
cv2.imshow('result', img)
cv2.waitKey(0)

image = io.BytesIO(img_b64decode)
good_image = Image.open(image)  # PIL