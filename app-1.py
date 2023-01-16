# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 10:09:44 2023

@author: Nenchin
"""

from flask import Flask, request, render_template, jsonify
import os
import pathlib
import base64
from werkzeug.utils import secure_filename
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = 'static/users/'
datasets = os.path.join(BASE_DIR, 'user_data')


class_names = []
for data in datasets:
    class_names.append(data)

for folder in app.config['UPLOAD_FOLDER']:
    class_names.append(folder)

ALLOWED_EXT = set(['jpg', 'jpeg', 'png', 'jfif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT


def train(data):
    try:

        "code for data preprocessing and training"

    except Exception as e:
        print(e)
    return "Done", model


def predict(filename, model):
    img = load_img(filename, target_size=(120, 120))
    img = img_to_array(img)
    img = img.reshape(1, 120, 120, 3)

    img = img.astype('float32')
    img = img / 255.0
    model = load_model(os.path.join(BASE_DIR, 'model_name'))
    result = model.predict(img)
    return result


@app.route('/')
def home():
    return jsonify('Welcome to Image Recognition Endpoint')


@app.route('/capture', methods=['GET', 'POST'])
def capture():
    if request.method == 'POST':
        imageId = request.json['id']
        folder = request.json['folder_name']
        encoded_string = request.json['image']
        decoded_string = base64.b64decode(encoded_string)
        path = os.path.join(os.getcwd(), "users", folder)
        if not os.path.exists(path):
            return jsonify({"error": "Create Folder"}), 400
        else:
            with open(f"{path}/{folder}-{imageId}.jpg", "wb") as f:
                f.write(decoded_string)
            return f"{folder}-{imageId} saved in {folder}"


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        user_name = request.json["folder_name"]
        if user_name == "":
            return jsonify({"error": "specify a folder name"}), 400

        else:
            user_name = user_name.strip().lower()
            # user_folder = pathlib.Path(app.config['UPLOADED_FILES'], user_name).mkdir(exist_ok=True)
            path = os.path.join(os.getcwd(), "users", user_name)
            if not os.path.exists(path):
                os.makedirs(path)
                return jsonify(message="folder created")
            else:
                return jsonify({"error": "folder already exists"}), 400




@app.route('/train', methods=["POST"])
def training():
    if request.method == "POST":
        message, model == train(app.config['UPLOAD_FOLDER'])
        "write a code to save the model"
        if message == "Done":
            return jsonify("training successful")
        else:
            return "an error occurred while training"


@app.route('/predict', methods=["POST"])
def prediction():
    target_img = os.path.join(os.getcwd(), 'static/images')
    error = ''
    target_img = os.path.join(os.getcwd(), 'static/images')
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save(os.path.join(target_img, file.filename))
            img_path = os.path.join(target_img, file.filename)
            img = file.filename
            pred_result = predict(img_path)
        else:
            error = "Please upload images of jpg , jfif, jpeg and png extension only"
        if (len(error) == 0):
            if pred_result not in class_names:
                return jsonify(img=img, error="Access denied")
            else:
                return jsonify(img=img, success_message="Access granted")
        else:
            return jsonify(error=error)


@app.route('/ping', methods=["GET"])
def pingpong():
    if request.method == "GET":
        print("pong")
        return "pong"


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0')
