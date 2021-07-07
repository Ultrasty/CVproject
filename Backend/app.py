import os
import json
from flask import Flask, request, jsonify
import panorama_stitching
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/index', methods=['POST'])
def get_content():

    data = json.loads(str(request.data, 'utf-8'))
    img_l = data["img_l"]
    img_r = data["img_r"]
    result = panorama_stitching.cv_stitching(img_l, img_r)
    return jsonify({'result': result})


if __name__ == '__main__':
    app.run()
