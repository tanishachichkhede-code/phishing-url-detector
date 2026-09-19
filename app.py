from flask import Flask, request, jsonify, render_template
import joblib
from urllib.parse import urlparse


app = Flask(__name__)


model = joblib.load(
    "model/phishing_model.pkl"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    url = data.get("url")

    if not isinstance(url, str):
        return jsonify({
            "error": "URL must be a string"
        }), 400

    url = url.strip()

    if not url:
        return jsonify({
            "error": "URL is required"
        }), 400

    parsed_url = urlparse(url)

    if parsed_url.scheme not in ["http", "https"]:
        return jsonify({
            "error": "Please enter a valid URL starting with http:// or https://"
        }), 400

    if not parsed_url.netloc:
        return jsonify({
            "error": "Please enter a valid URL with a domain name"
        }), 400

    prediction = model.predict([url])[0]

    probabilities = model.predict_proba([url])[0]

    legitimate_probability = probabilities[0] * 100

    phishing_probability = probabilities[1] * 100

    if prediction == 1:
        result = "Phishing"
    else:
        result = "Legitimate"

    return jsonify({
        "url": url,
        "prediction": result,
        "legitimate_probability": round(
            legitimate_probability,
            2
        ),
        "phishing_probability": round(
            phishing_probability,
            2
        )
    })


if __name__ == "__main__":

    app.run(
        debug=True
    )