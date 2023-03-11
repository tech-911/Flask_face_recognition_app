# -*- coding: utf-8 -*-
"""
Created on Sat Jan  7 10:09:44 2023

@author: Nenchin
"""

from flask import Flask, request, jsonify
import os
import base64
from flask_cors import CORS
import os.path
from face_recognition_knn import train, predict



app = Flask(__name__)
CORS(app)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
datasets = os.path.join(BASE_DIR, 'user_data')


class_names = []
for folder in datasets:
    class_names.append(folder)


ALLOWED_EXT = set(['jpg', 'jpeg', 'png', 'jfif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXT



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
        "write a code to save the model"
        print("Training KNN classifier...")
        classifier, message = train(datasets, model_save_path="trained_knn_model.clf", n_neighbors=2)
        if message == "Done":
            return jsonify("Training complete!", classifier)
        else:
            return "an error occurred while training"


@app.route('/predict', methods=["POST"])
def prediction():
    error = ''
    target_img = os.path.join(os.getcwd(), 'static/images')
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save(os.path.join(target_img, file.filename))
            img_path = os.path.join(target_img, file.filename)
            img = file.filename
            name, (top, right, bottom, left) = predict(img_path, model_path="trained_knn_model.clf")

        else:
            error = "Please upload images of jpg , jfif, jpeg and png extension only"
        if (len(error) == 0):
            if name in class_names:
                return jsonify(img=img, success_message="Access granted")
            if name == "unknown":
                return jsonify(img=img, error="Access denied")
        else:
            return jsonify(error=error)


@app.route('/ping', methods=["GET"])
def pingpong():
    if request.method == "GET":
        print("pong")
        return "pong"


if __name__ == "__main__":
    # app.run(debug=False, host='0.0.0.0')
    app.run(debug=True)

