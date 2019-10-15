# importing the requests library
import json, sys, subprocess, requests, re

if len(sys.argv) > 2:
    prefix = sys.argv[1]
    language = sys.argv[2]
else:
    print "please provide the file name and the language"
    exit(-1)

dictionaryFile = "data/dictionery-" + language + ".json"

try:
    dictionary = json.load(open(dictionaryFile))
except:
    dictionary = {}

switcher = {
        "en": "Alex",
        "tr": "Yelda",
        "ar": "Maged"
    }

voice = switcher.get(language)

# api-endpoint
URL = "https://translation.googleapis.com/language/translate/v2"
from translation_key import *

filename = "data/" + prefix + "-" + language + ".vtt"
file = open(filename)
lines = file.read().splitlines()
count  = 0
for line in lines:
    if not "-->" in line and len(line) > 0:
        line = line.lower().replace(":","").replace(",","").replace("?", "").replace("!", "").replace(".", "").replace("[", "").replace("]", "").replace("-", "")
        words = line.split()
        for word in words:
            if not dictionary.has_key(word.decode('utf8')):
                try:
                    count = count + 1
                    PARAMS = {'key':key, 'q':word, 'source':language, 'target':'en'}
                    r = requests.get(url = URL, params = PARAMS)
                    data = r.json()
                    translatedWord = data['data']['translations'][0]['translatedText'].replace('-','').replace("&#39;","'").lower()
                    dictionary[word.decode('utf8')] = translatedWord
                    print(str(count) + ". " + word + ": " + translatedWord.encode('utf8'))
                    if word != translatedWord.encode('utf8'):
                        targetFile = "data/words/" + word + ".m4a"
                        subprocess.call(["say", "-v", voice, "-r", "125", "-o", targetFile, word])
                        targetFile = "data/words/" + word + "-en.m4a"
                        subprocess.call(["say", "-v", "Alex", "-o", targetFile, translatedWord])
                    if count % 100 == 0:
                        json.dump(dictionary, open(dictionaryFile, 'w'), sort_keys = False, indent = 4, ensure_ascii = True)
                except Exception as error:
                    print "error: " + str(error) + " word: " + word
                    json.dump(dictionary, open(dictionaryFile, 'w'), sort_keys = False, indent = 4, ensure_ascii = True)

file.close()

json.dump(dictionary, open(dictionaryFile, 'w'), sort_keys = False, indent = 4, ensure_ascii = True)

