import os
import errno
import lxml
import pdb

from bingtts import Translator
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
        return None

def get_steps(recipe_json):
    instructionList = recipe_json['analyzedInstructions'][0]["steps"]
    return instructionList

def get_ingredients(recipe_json):
    ing_raw = recipe_json['extendedIngredients']
    ing_pos = [ing['originalString'] for ing in ing_raw]
    return ing_pos

def get_total_time(recipe_json):
    return recipe_json['readyInMinutes'] if 'readyInMinutes' in recipe_json else None

def create_template_kwargs(recipe_url, recipe_json):
    kwargs = dict()
    kwargs['recipe_url'] = recipe_url
    kwargs['recipe_name'] = get_recipe_name(recipe_json)
    kwargs['domain'] = get_url_domain(recipe_url)
    kwargs['recipe_steps'] = get_steps(recipe_json)
    kwargs['image'] = get_image(recipe_json)
    kwargs['total_time'] = get_total_time(recipe_json)
    kwargs['ing_pos'] = get_ingredients(recipe_json)
    return kwargs

def synthesize_speech(recipe_id, steps_json, ing_pos):
    # TODO: Do unhardcode path, it is relative to calling PWD
    wav_root = "./website/static/wav/"

    if not os.path.exists(wav_root + recipe_id):
        tts = Translator('50dbceaa8a424c1c89ea9c33d3a4eec0')
        speech_text = [step_raw['step'] for step_raw in steps_json]
        # TODO: optimize speech
        speech_bin = [tts.speak(step_raw, "en-US", "Female", "riff-16khz-16bit-mono-pcm") for step_raw in speech_text]
        ing_bin = [tts.speak(ing_raw, "en-US", "Female", "riff-16khz-16bit-mono-pcm") for ing_raw in ing_pos]

        # create the recipe ID holding the recipe wave files

        try:
            print('creating folder ' + wav_root + recipe_id)
            os.makedirs(wav_root + recipe_id)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        wav_list = []

        for ing_num in xrange(len(ing_pos)):
            fname = 'ing_%d' % ing_num
            wav_list.append('%s' % fname)
            with open("%s%s/%s.wav" % (wav_root, recipe_id, fname), 'w') as f:
                f.write(ing_bin[ing_num])

        for step in xrange(len(speech_text)):
            fname = 'step_%d' % step
            wav_list.append('%s' % fname)
            with open("%s%s/%s.wav" % (wav_root, recipe_id, fname), 'w') as f:
                f.write(speech_bin[step])

        return wav_list
    else:
        return [file[:-4] for file in os.listdir('%s%s' % (wav_root, recipe_id)) if file.endswith(".wav")]







