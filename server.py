from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

model = tf.keras.models.load_model("training/model.h5")

@app.route("/predict", methods=["OPTIONS"])
def predict_options():
    return '', 200

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json["image"]

    img = np.array(data).reshape(1, 28, 28).astype("float32")

    pred = model.predict(img)
    result = int(np.argmax(pred))

    return jsonify({"digit": result})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
