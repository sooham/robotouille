from bingtts import Translator
import json
from pprint import pprint




### reading recepe

with open('response.json') as data_file:    
    data = json.load(data_file)
#pprint(data["analyzedInstructions"][0]["steps"][0]["step"])


numSteps = data["analyzedInstructions"][0]["steps"].__len__()
instructionList = list()

for i in range(0, numSteps-1):
    #pprint(data["analyzedInstructions"][0]["steps"][i]["step"])
    instructionList.append(data["analyzedInstructions"][0]["steps"][i]["step"])
    print(str(instructionList[i]))
    #print("\n")

#print(instructionList)


### Text to Speech

translator = Translator('50dbceaa8a424c1c89ea9c33d3a4eec0')

for i in range(0, numSteps-1):
    output = translator.speak(str(instructionList[i]), "en-US", "Female","riff-16khz-16bit-mono-pcm")
    with open("instruction_"+str(i)+".wav", "w") as f:
        f.write(output)
'''

output = translator.speak("Hello, my name is sooham", "en-IN", "Male","riff-16khz-16bit-mono-pcm")
with open("test.wav", "w") as f:
    f.write(output)
'''

# Speech to text

def recognize_raw(self, wav, locale=None):
    
        if locale is None:
            locale = self.locale
        if locale not in LOCALES:
            raise ValueError('unsupported locale: ' + locale)

        with audio._open_wav(wav) as w:
            if w.getnchannels() != 1:
                raise ValueError('can only recognize single channel audio')

            content_type = '; '.join((
                'audio/wav',
                'codec="audio/pcm"',
                'samplerate=8000',
                'sourcerate={}'.format(w.getframerate()),
                'trustsourcerate=true'
            ))


        params = '&'.join((
            'scenarios=ulm',
            'appid=D4D52672-91D7-4C74-8AD8-42B1D98141A5',
            'locale={}'.format(locale),
            'device.os="Windows OS"',
            'version=3.0',
            'format=json',
            'instanceid=565D69FF-E928-4B7E-87DA-9A750B96D9E3',
            'requestid={}'.format(uuid.uuid4())
        ))

        r = requests.post(
            _API_SCOPE + '/recognize?' + params,
            data=wav,
            headers={
                'Content-Type': content_type,
                #'Accept': 'application/json;text/xml',
                'Authorization': 'Bearer ' + self._get_token(),
            },
        )
        r.raise_for_status()

        return r.json()