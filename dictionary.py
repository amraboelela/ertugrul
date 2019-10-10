# importing the requests library
import json, sys, subprocess, requests, re

if len(sys.argv) > 2:
    filename = sys.argv[1]
    language = sys.argv[2]
else:
    print "please provide the file name and the language"
    exit(-1)

dictionaryFile = "data/dictionery-" + language + ".json"

try:
    dictionary = json.load(open(dictionaryFile))
except:
    dictionary = {}

# api-endpoint
URL = "https://translation.googleapis.com/language/translate/v2"
from translation_key import *

print "filename: " + filename
file = open(filename)
print "file: " + str(file)
lines = file.read().splitlines()
for line in lines:
    print "line: " + line
    if not "-->" in line and len(paragraph) > 0:
        print str(count) + ".line: " + line
        words = re.split(" ", paragraph)
        for word in words:
            print("word: " + word)
            PARAMS = {'key':key, 'q':word, 'source':language, 'target':'en'}
            r = requests.get(url = URL, params = PARAMS)
            data = r.json()
            translatedWord = data['data']['translations'][0]['translatedText'].replace('-','').replace("&#39;","'")
            try:
                translatedWord = translatedText.encode('utf8')
                print(translatedWord)
                dictionary[word] = translatedWord
                print
            except Exception as error:
                print "error: " + str(error) + " line: " + line

file.close()

json.dump(dictionary, open(dictionaryFile, 'w'), sort_keys = False, indent = 4, ensure_ascii = True)

