import cv2
import numpy as np
from tensorflow.keras.models import load_model

model = load_model("stroke_model.h5")

def predict_image(path):

    img = cv2.imread(path)

    # check if image loaded properly
    if img is None:
        return "Invalid or Unsupported Image", 0

    img = cv2.resize(img,(224,224))
    img = img/255.0
    img = np.reshape(img,(1,224,224,3))

    prediction = model.predict(img)

    confidence = float(prediction[0][0]) * 100

    if prediction[0][0] > 0.5:
        result = "Stroke Detected"
    else:
        result = "Normal Brain"

    return result, round(confidence,2)