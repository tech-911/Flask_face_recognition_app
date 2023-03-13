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
from face_recognition_knn import train, predict, show_prediction_labels_on_image



app = Flask(__name__)
CORS(app)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
datasets = os.path.join(BASE_DIR, 'users/train')


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
        path = os.path.join(os.getcwd(), "users/train", folder)
        if not os.path.exists(path):
            return jsonify({"error": "Create Folder"}), 400
        else:
            with open(f"{path}/{folder}{imageId}.jpeg", "wb") as f:
                f.write(decoded_string)
            return f"{folder}{imageId} saved in {folder}"


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        user_name = request.json["folder_name"]
        if user_name == "":
            return jsonify({"error": "specify a folder name"}), 400

        else:
            user_name = user_name.strip().lower()
            # user_folder = pathlib.Path(app.config['UPLOADED_FILES'], user_name).mkdir(exist_ok=True)
            path = os.path.join(os.getcwd(), "users/train", user_name)
            modelpath = os.path.join(os.getcwd(), "users", "model")
            if not os.path.exists(path):
                os.makedirs(path)
                if not os.path.exists(modelpath):
                    os.makedirs(modelpath) 
                    return jsonify(message="folder created")
                else:
                    return jsonify(message="folder created")
            else:
                return jsonify({"error": "folder already exists"}), 400




@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    path = os.path.join(os.getcwd(), "users/test")
    if not os.path.exists(path):
        os.makedirs(path)
    file.save('users/test/' + filename)
    return 'File uploaded successfully'




@app.route('/train', methods=["POST"])
def training():
    if request.method == "POST":
        "write a code to save the model"
        print("Training KNN classifier...")
        classifier, message = train(datasets, model_save_path="users/model/trained_knn_model.clf", n_neighbors=2)
        if message == "Done":
            return jsonify("Training complete!")
        else:
            return "an error occurred while training"


@app.route('/predict', methods=["POST"])
def prediction():
    error = 'error'
    target_img = os.path.join(os.getcwd(), 'users/test')
    if not os.path.exists(target_img):
        os.makedirs(target_img)
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save('users/test/' + file.filename)
            img_path = os.path.join(target_img, file.filename)
            img = file.filename
            print("Looking for faces in {}".format(img))
            predictions = predict(img_path, model_path="users/model/trained_knn_model.clf")

        else:
            error = "Please upload images of jpg , jfif, jpeg and png extension only"
        
        for name, (top, right, bottom, left) in predictions:
            predictedImage=show_prediction_labels_on_image(img_path, predictions)
            return jsonify({"result": {"name": f"{name}", "left": f"{left}", "top": f"{top}"}, "message":"Access granted", "image": f"{predictedImage}"})
   
        else: 
            return jsonify(error=error), 400


@app.route('/ping', methods=["GET"])
def pingpong():
    if request.method == "GET":
        print("pong")
        return "pong"


if __name__ == "__main__":
    # app.run(debug=False, host='0.0.0.0')
    app.run(debug=True)

