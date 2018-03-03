from __future__ import print_function

import pdb
import json
import requests
import urllib

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

API_URL = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/extract"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recipeLink")
def process_recipe():
    recipe_url = urllib.quote(request.args.get('recipeLink'), safe='')
    headers = {"X-Mashape-Key" : "e3LHtLGp7Smshyw7E0qaeCjHiuR3p1DczjljsnvW3aq1XYuWyz"}
    r = requests.get(API_URL+"?forceExtraction=false&url="+recipe_url, headers=headers)
    return str(r.json())

@app.route("/login", methods=['POST'])
def login():
    pass
