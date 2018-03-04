from __future__ import print_function

import pdb
import json
import requests
import urllib
import lxml
import utils

from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

API_URL = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/extract"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recipe")
def process_recipe():
    recipe_url = request.args.get('recipeLink')
    recipe_url_esc = urllib.quote(recipe_url, safe='')
    headers = {"X-Mashape-Key" : "e3LHtLGp7Smshyw7E0qaeCjHiuR3p1DczjljsnvW3aq1XYuWyz"}
    recipe_json = requests.get(API_URL+"?forceExtraction=false&url="+recipe_url_esc, headers=headers).json()

    # create the team input kwargs
    kwargs = utils.create_template_kwargs(recipe_url, recipe_json)

    # synthesize recipe steps using bing text to speech API
    kwargs['wav_files'] = utils.synthesize_steps_speech(str(recipe_json['id']), kwargs['recipe_steps'])

    return render_template("recipeFollowView.html", **kwargs)


@app.route("/login", methods=['POST'])
def login():
    pass

