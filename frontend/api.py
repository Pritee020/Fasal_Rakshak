from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import tensorflow as tf
import numpy as np
import json
import os
import ast

app = Flask(__name__)
CORS(app)

# -----------------------------
# Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "crop_disease_model.h5")
CLASS_NAMES_PATH = os.path.join(BASE_DIR, "class_names.json")
APP_PATH = os.path.join(BASE_DIR, "app.py")


# -----------------------------
# Load Model
# -----------------------------
model = tf.keras.models.load_model(MODEL_PATH)

with open(CLASS_NAMES_PATH, "r", encoding="utf-8") as f:
    class_names = json.load(f)

if isinstance(class_names, dict):
    class_names = list(class_names.keys())


# -----------------------------
# Load existing solutions
# from original app.py
# -----------------------------
def load_solutions():
    with open(APP_PATH, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)

    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "solutions":
                    return ast.literal_eval(node.value)

    return {}


solutions = load_solutions()


# -----------------------------
# Prediction API
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():

    if "file" not in request.files:
        return jsonify({
            "success": False,
            "error": "No image file received"
        }), 400

    file = request.files["file"]

    try:
        image = Image.open(file).convert("RGB")
        image = image.resize((224, 224))

        image_array = np.array(image, dtype=np.float32)

        image_array = tf.keras.applications.mobilenet_v2.preprocess_input(
            image_array
        )

        image_array = np.expand_dims(image_array, axis=0)

        predictions = model.predict(image_array, verbose=0)

        predicted_index = int(np.argmax(predictions[0]))
        confidence = float(np.max(predictions[0]) * 100)

        disease = class_names[predicted_index]

        # Get information from original app.py database
        info = solutions.get(disease, {})

        return jsonify({
            "success": True,
            "plant": disease.split("___")[0].replace("_", " "),
            "disease": disease,
            "confidence": round(confidence, 2),
            "cause": info.get("cause", "Information not available."),
            "solution": info.get("solution", "Information not available."),
            "recovery": info.get(
                "recovery_chance",
                "Information not available."
            )
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# -----------------------------
# Test Route
# -----------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Fasal Rakshak API is running!"
    })


# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )