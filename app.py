from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # hides most TensorFlow warnings
from predict import predict_image  # your prediction function

app = Flask(__name__)

# Folder to save uploaded images
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Allowed image extensions
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp"}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    confidence = None
    image_path = None
    error = None

    if request.method == "POST":
        if "image" not in request.files:
            error = "No file uploaded"
            return render_template("index.html", error=error)

        file = request.files["image"]

        if file.filename == "":
            error = "No file selected"
            return render_template("index.html", error=error)

        if not allowed_file(file.filename):
            error = "Only image files (png, jpg, jpeg, bmp) are allowed"
            return render_template("index.html", error=error)

        # Save uploaded file securely
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)

        # Predict using your model
        result, confidence = predict_image(filepath)
        image_path = filepath

    return render_template(
        "index.html",
        result=result,
        confidence=confidence,
        image=image_path,
        error=error
    )

if __name__ == "__main__":
    # host=0.0.0.0 makes it accessible on your LAN (phone + PC)
    app.run(host="0.0.0.0", port=5000, debug=True)