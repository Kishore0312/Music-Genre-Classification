import os
import random

from flask import Flask, request, jsonify, render_template
from genre_rec_service import Genre_Recognition_Service

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict():

    audio_file = request.files["UploadedAudio"]
    file_name = str(random.randint(0, 100000))
    audio_file.save(file_name)

    from cryptography.fernet import Fernet

    key = Fernet.generate_key()
    fernet = Fernet(key)

    with open("key.key", "wb") as filekey:
        filekey.write(key)

    with open("key.key", "rb") as filekey:
        key = filekey.read()

    with open(file_name, "rb") as file:
        originalaudio = file.read()

    encrypted = fernet.encrypt(originalaudio)

    with open(file_name, "wb") as encrypted_file:
        encrypted_file.write(encrypted)

    fernet = Fernet(key)
    with open(encrypted, "rb") as enc_file:
        encrypted = enc_file.read()

    grs = Genre_Recognition_Service()
    prediction = grs.predict(file_name)
    os.remove(file_name)

    prediction_message = f"""
    The song is predicted to be in the {prediction} genre.
    """
    return render_template("index.html", prediction_text=prediction_message)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=False)
