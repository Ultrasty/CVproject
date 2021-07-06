import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/index', methods=['POST'])
def get_content():
    img_l = request.json.get('img_l')
    img_r = request.json.get('img_r')
    return jsonify({img_l: img_r})


if __name__ == '__main__':
    app.run()
