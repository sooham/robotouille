import lxml
from urlparse import urlparse

def get_recipe_name(recipe_json):
    return recipe_json['title'] if 'title' in recipe_json else None

def get_url_domain(url):
    parsed_uri = urlparse(url)
    domain = '{uri.netloc}'.format(uri=parsed_uri)
    return domain

def get_image(recipe_json):
    if 'image' in recipe_json:
        return recipe_json['image']
    else:
        return Exception

def get_steps(recipe_json):
    instructionList = recipe_json['analyzedInstructions'][0]["steps"]
    return instructionList
