from flask import Flask, redirect, request
from flask_cors import CORS

import json
import numpy as np

import bias
import news
import text_analysis

app = Flask(__name__)
CORS(app)

unique = bias.load_unique()
model = bias.load_model()


@app.route("/", methods=["GET", "POST"])
def article():
    if request.method == "GET":
        return redirect("https://perception.tk")

    url = request.data.decode()
    article = news.analyze(url)
    analysis = text_analysis.analyze(article["title"], article["text"])
    parsed = bias.parse_article(article["text"])
    formatted = bias.format_data(parsed, unique)
    predicted_bias = model.predict(formatted)[0].astype(np.float64)
    predicted_bias = {"left": predicted_bias[0], "right": predicted_bias[1]}

    return json.dumps({**article, **analysis, **predicted_bias})


@app.route("/text", methods=["GET", "POST"])
def text():
    if request.method == "GET":
        return redirect("https://perception.tk")

    text = request.data.decode()
    parsed = bias.parse_article(text)
    formatted = bias.format_data(parsed, unique)
    predicted_bias = model.predict(formatted)[0].astype(np.float64)
    predicted_bias = {"left": predicted_bias[0], "right": predicted_bias[1]}

    return json.dumps(predicted_bias)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
