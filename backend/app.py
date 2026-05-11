import os

from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image

app = Flask(__name__)
CORS(app)

# =========================
# LOAD MODEL
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = tf.keras.models.load_model(
    os.path.join(BASE_DIR, "models", "cotton_disease_model.h5")
)

# =========================
# CLASS NAMES
# =========================

CLASS_NAMES = [
    "aug_Alternaria_Leaf",
    "aug_Bacterial_Blight",
    "aug_Fusarium_Wilt",
    "aug_Healthy_Leaf",
    "aug_Verticillium_Wilt",
]

# =========================
# DISEASE INFORMATION
# =========================

DISEASE_INFO = {

    "aug_Bacterial_Blight": {
        "display_name": "Bacterial Blight",
        "healthy": False,
        "description":
            "Angular water-soaked lesions caused by Xanthomonas citri pv. malvacearum.",
        "treatment":
            "Apply copper-based bactericide. Remove and destroy infected plant parts. Avoid overhead irrigation.",
    },

    "aug_Fusarium_Wilt": {
        "display_name": "Fusarium Wilt",
        "healthy": False,
        "description":
            "Soil-borne fungal disease causing vascular browning, yellowing, and wilting.",
        "treatment":
            "Use resistant varieties. Treat soil with fungicide before planting. Practice crop rotation.",
    },

    "aug_Alternaria_Leaf": {
        "display_name": "Alternaria Leaf Spot",
        "healthy": False,
        "description":
            "Circular brown spots with yellow halos caused by Alternaria macrospora.",
        "treatment":
            "Apply mancozeb or iprodione fungicide. Improve air circulation. Avoid prolonged leaf wetness.",
    },

    "aug_Healthy_Leaf": {
        "display_name": "Healthy Leaf",
        "healthy": True,
        "description":
            "No disease detected. The leaf appears healthy with normal coloration and texture.",
        "treatment":
            "No treatment required. Continue regular monitoring and preventive care.",
    },

    "aug_Verticillium_Wilt": {
        "display_name": "Verticillium Wilt",
        "healthy": False,
        "description":
            "Soil-borne pathogen causing 'half-leaf' symptoms and premature defoliation.",
        "treatment":
            "Use resistant cultivars. Implement soil fumigation. Remove infected debris. Practice long crop rotations.",
    },
}

IMG_SIZE = 224

# =========================
# IMAGE PREPROCESS
# =========================

def preprocess_image(image):

    image = image.resize((IMG_SIZE, IMG_SIZE))

    image = np.array(image) / 255.0

    image = np.expand_dims(image, axis=0)

    return image

# =========================
# HOME ROUTE
# =========================

@app.route("/")
def home():

    return "Cotton Disease Detection API Running"

# =========================
# PREDICT ROUTE
# =========================

@app.route("/predict", methods=["POST"])
def predict():

    if "file" not in request.files:

        return jsonify({
            "error": "No file uploaded"
        })

    file = request.files["file"]

    try:

        # Open Image
        image = Image.open(file).convert("RGB")

        # Preprocess
        processed = preprocess_image(image)

        # Predict
        prediction = model.predict(processed)

        predicted_index = np.argmax(prediction)

        predicted_class = CLASS_NAMES[predicted_index]

        confidence = float(np.max(prediction)) * 100

        # Get Disease Details
        disease_data = DISEASE_INFO[predicted_class]

        # Response
        return jsonify({

            "prediction": disease_data["display_name"],

            "healthy": disease_data["healthy"],

            "confidence": round(confidence, 2),

            "description": disease_data["description"],

            "treatment": disease_data["treatment"]

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

# =========================
# RUN SERVER
# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)