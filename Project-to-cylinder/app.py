# -*- coding: utf-8 -*-
# @Time    : 2021/5/10 18:28
# @Author  : STY
# @Email   : 1455670697@qq.com
# @File    : app.py
# @Software: PyCharm
import json
import os
from flask import Flask, make_response, request, redirect, url_for, send_from_directory
import numpy as np
import pandas as pd
from flask_cors import CORS
import cv2
from main import themain
import base64

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/index', methods=['POST', 'GET'])
def question1():
    # file = request.files['file']
    # file.save(os.getcwd() + '/' + file.filename)

    data = json.loads(str(request.data, 'utf-8'))

    for i in range(len(data)):
        img_decode = base64.b64decode(data[i][22:])
        img_array = np.frombuffer(img_decode, np.uint8)  # 转换np序列
        imageA = cv2.imdecode(img_array, cv2.COLOR_BGR2RGB)  # 转换Opencv格式
        cv2.imwrite("./images/"+str(i+2)+".png", imageA)
    try:
        themain()
    except Exception:
        pass
    result = cv2.imread("cropped.jpg")
    result = np.rot90(result)
    result = np.rot90(result)
    result = np.rot90(result)
    result = cv2.imencode('.jpg', result)[1]
    base64_data = str(base64.b64encode(result))[2:-1]

    response = make_response({"result1": base64_data})
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
