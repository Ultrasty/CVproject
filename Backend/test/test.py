import cv2
import base64

import numpy as np

img_file = open('images/bryce_left_01.png', 'rb')  # 二进制打开图片文件
img_b64encode = base64.b64encode(img_file.read())  # base64编码

imgData = base64.b64decode(img_b64encode)
nparr = np.fromstring(imgData, np.uint8)
img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

image = cv2.imencode('.jpg', img_np)[1]
base64_data = str(base64.b64encode(image))[2:-1]
print(base64_data)

imgData = base64.b64decode(base64_data)
nparr = np.fromstring(imgData, np.uint8)
img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
cv2.imshow('result', img_np)
cv2.waitKey(0)
