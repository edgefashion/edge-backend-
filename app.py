from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import cv2
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files['image']
    gender = request.form['gender']
    occasion = request.form['occasion']
    style = request.form['style']

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # Basic image processing
    img = cv2.imread(filepath)
    skin_tone = detect_skin_tone(img)
    body_shape = detect_body_shape(img)

    suggestions = generate_suggestions(body_shape, skin_tone, gender, occasion, style)

    return jsonify({
        "body_shape": body_shape,
        "skin_tone": skin_tone,
        "style_suggestion": suggestions
    })

def detect_skin_tone(image):
    face = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixels = face.reshape((-1, 3))
    avg_color = np.mean(pixels, axis=0)
    r, g, b = avg_color
    if r > 200 and g > 180:
        return "fair"
    elif r > 150:
        return "wheatish"
    else:
        return "dusky"

def detect_body_shape(image):
    height, width = image.shape[:2]
    if height > width * 1.5:
        return "rectangle"
    else:
        return "pear"

def generate_suggestions(shape, tone, gender, occasion, style):
    tips = []
    if shape == "rectangle":
        tips.append("Try structured blazers and defined waistlines.")
    elif shape == "pear":
        tips.append("Highlight your upper body with light-colored tops.")

    if tone == "fair":
        tips.append("Try pastel or soft tones.")
    elif tone == "wheatish":
        tips.append("Go for earthy tones and neutrals.")
    else:
        tips.append("Bold and deep colors suit you best.")

    if style == "streetwear":
        tips.append("Add oversized graphic tees and sneakers.")
    elif style == "minimalist":
        tips.append("Go with clean lines and neutral shades.")
    elif style == "traditional":
        tips.append("Incorporate ethnic prints and drapes.")

    return tips

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

