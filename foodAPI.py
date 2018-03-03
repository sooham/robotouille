import json
from urllib import request
from urllib import parse

api_url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/extract"
recipe_url = "https://www.foodnetwork.com/recipes/ina-garten/lemon-chicken-breasts-recipe-1923711"
safe_recipe_url = parse.quote(recipe_url, safe='')
force_extraction = "false"
header = {"X-Mashape-Key" : "e3LHtLGp7Smshyw7E0qaeCjHiuR3p1DczjljsnvW3aq1XYuWyz"}

r_equest = request.Request(api_url+"?forceExtraction="+force_extraction+"&url="+safe_recipe_url, headers = header)
r_esponse = request.urlopen(r_equest)

data = json.load(r_esponse)
print(data)
