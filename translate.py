# importing the requests library
import sys, requests

if len(sys.argv) > 2:
    filename = sys.argv[1]
    targetLanguage = sys.argv[2]
else:
    print "please provide the file name and the target language"
    exit(-1)

txtFileName = filename.replace('.vtt', '') + ".txt"
subprocess.call(["python", "clean.py", filename, ">", txtFilename])

# api-endpoint
URL = "https://translation.googleapis.com/language/translate/v2"
from translation_key import *

file = open(txtFilename)
lines = file.read().splitlines()
for line in lines:
    if not line.strip():
        print
    elif "-->" in line or len(line) < 4:
        x = 0
    else:
        PARAMS = {'key':key, 'q':line, 'source':'en', 'target':targetLanguage}
        r = requests.get(url = URL, params = PARAMS)
        data = r.json()
        translatedText = data['data']['translations'][0]['translatedText']
        try:
            print(translatedText.encode('utf8'))
        except Exception as error:
            print "error: " + str(error) + " line: " + line
file.close()

