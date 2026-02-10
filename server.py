from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

model = tf.keras.models.load_model("training/model.h5")

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json["image"]

    img = np.array(data).reshape(1, 28, 28).astype("float32")

    print("MIN:", np.min(img))
    print("MAX:", np.max(img))
    print("SUM:", np.sum(img))

    pred = model.predict(img)
    result = int(np.argmax(pred))

    return jsonify({"digit": result})


app.run(host="127.0.0.1", port=5000)

