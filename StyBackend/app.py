# -*- coding: utf-8 -*-
# @Time    : 2021/5/10 18:28
# @Author  : STY
# @Email   : 1455670697@qq.com
# @File    : app.py
# @Software: PyCharm
import json
import os
from flask import Flask, make_response, request, redirect, url_for, send_from_directory
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/upload', methods=['POST', 'GET'])
def question1():
    # file = request.files['file']
    # file.save(os.getcwd() + '/' + file.filename)

    data = json.loads(str(request.data, 'utf-8'))

    for i in range(len(data)):
        print(data[i])

    response = make_response({"data": "success"})
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0')
