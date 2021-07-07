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
    img_l = img_l.split(",", 1)[1]
    img_r = img_r.split(",", 1)[1]
    (result1, result2) = panorama_stitching.cv_stitching(img_l, img_r)
    return jsonify({'result1': result1, "result2": result2 })


if __name__ == '__main__':
    app.run(host="0.0.0.0")
