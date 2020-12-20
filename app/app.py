
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


@app.route('/')
def index():
    """Display the most rated movies to the user
       and prompts the user to rate them: solves cold start problem.
    """
    top10 = most_rated