# importing the requests library
import json, sys, subprocess, requests, re, os

if len(sys.argv) > 2:
    prefix = sys.argv[1]
    language = sys.argv[2]
else:
    print "please provide the prefix and the language"
    exit(-1)

dictionaryFile = "data/dictionary-" + language + ".json"

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
#print "filename: " + filename
file = open(filename)
lines = file.read().splitlines()
count  = 0
for line in lines:
    if not "-->" in line and len(line) > 0:
        line = line.lower().replace(":","").replace(",","").replace("?", "").replace("!", "").replace(".", "").replace("[", "").replace("]", "").replace("-", "").replace("[","").replace("]","").replace("<i>","").replace("</i>","").replace('"', '')
        #print "line: " + line
        words = line.split()
        for word in words:
            if dictionary.has_key(word.decode('utf8')):
                dicValue = dictionary[word.decode('utf8')]
                #print "type(dicValue): " + str(type(dicValue))
                if type(dicValue) is dict and dicValue['update'] == True:
                    print(str(count) + ". " + word + ": " + dicValue['en'].encode('utf8'))
                    count = count + 1
                    dicValue['update'] = False
                    #dictionary[word.decode('utf8')] = dicValue
                    targetFile = "data/words/" + language + "/" + word + "-en.m4a"
                    if word == dicValue['en'].encode('utf8'):
                        os.system("rm -f " + targetFile)
                    else:
                        subprocess.call(["say", "-v", "Alex", dicValue['en'], "-o", targetFile])
                        targetFile = "data/words/" + language + "/" + word + ".m4a"
                        targetFileMp3 = "data/words/" + language + "/" + word + ".mp3"
                        if language == "ar":
                            subprocess.call(["gtts-cli", word, "-l", "ar", "--output", targetFileMp3])
                            os.system("ffmpeg -y -i " + targetFileMp3 + " -c:a aac -b:a 192k " + targetFile)
                            os.system("rm " + targetFileMp3)
                        else:
                            subprocess.call(["say", "-v", voice, "-r", "125", word, "-o", targetFile])
                elif type(dicValue) is unicode or type(dicValue) is str:
                    dictionary[word.decode('utf8')] = {'en': dicValue, 'update': False}
            else:
                print "word: " + word
                try:
                    count = count + 1
                    PARAMS = {'key':key, 'q':word, 'source':language, 'target':'en'}
                    r = requests.get(url = URL, params = PARAMS)
                    data = r.json()
                    translatedWord = data['data']['translations'][0]['translatedText'].replace('-','').replace("&#39;","'").replace("?","").lower()
                    dictionary[word.decode('utf8')] = {'en': translatedWord, 'update': False}
                    print(str(count) + ". " + word + ": " + translatedWord.encode('utf8'))
                    if word != translatedWord.encode('utf8'):
                        targetFile = "data/words/" + language + "/" + word + ".m4a"
                        targetFileMp3 = "data/words/" + language + "/" + word + ".mp3"
                        if language == "ar":
                            subprocess.call(["gtts-cli", word, "-l", "ar", "--output", targetFileMp3])
                            os.system("ffmpeg -y -i " + targetFileMp3 + " -c:a aac -b:a 192k " + targetFile)
                            os.system("rm " + targetFileMp3)
                        else:
                            subprocess.call(["say", "-v", voice, "-r", "125", word, "-o", targetFile])
                        targetFile = "data/words/" + language + "/" + word + "-en.m4a"
                        subprocess.call(["say", "-v", "Alex", translatedWord, "-o", targetFile])
                    if count % 100 == 0:
                        json.dump(dictionary, open(dictionaryFile, 'w'), sort_keys = False, indent = 4, ensure_ascii = True)
                except Exception as error:
                    print "error: " + str(error) + " word: " + word
                    json.dump(dictionary, open(dictionaryFile, 'w'), sort_keys = False, indent = 4, ensure_ascii = True)

file.close()

json.dump(dictionary, open(dictionaryFile, 'w'), sort_keys = False, indent = 4, ensure_ascii = True)

os.system("python unicode.py " + dictionaryFile + " > data/dictionary-" + language + ".txt")

