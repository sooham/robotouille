from __future__ import print_function
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recipeLink", methods=['POST'])
def process_recipe():
    assert request.method == 'POST'

    return "recieved recipe link: %s" % (request.form['recipeLink'])

@app.route("/login", methods=['POST'])
def login():
    pass
