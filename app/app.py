from flask import Flask, render_template, request
import pandas as pd
from app.models import preprocess_text, extract_entities, analyse_sentiment, get_lexical_richness

app = Flask(__name__)


@app.route('/')
def index():
    # return "Hello"
    input_text = preprocess_text("texts/example1.txt")
    sentiment = analyse_sentiment(input_text)
    entities = extract_entities(input_text)
    lexic = get_lexical_richness(input_text)

    return render_template(
        'index.html',
        title="TLDR",
        input_text=input_text,
        entities=entities)


if __name__ == "__main__":
    app.run(debug=True, port=5000)