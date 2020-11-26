# -*- coding: utf-8 -*-

import json, sys, subprocess, requests, re, os

if len(sys.argv) > 2:
    prefix = sys.argv[1]
    language = sys.argv[2]
else:
    print "please provide the prefix and the language"
    exit(-1)

print "## dictionary, prefix: " + prefix + ", language: " + language

dictionaryFilePath = "build/dictionary-" + language + ".txt"
dictionaryFile = open(dictionaryFilePath)
dictionaryLines = dictionaryFile.read().splitlines()
dictionary = {}
for dictionaryLine in dictionaryLines:
    lineSplit = dictionaryLine.split(":")
    word = lineSplit[0].strip()
    meaning = lineSplit[1].strip()
    dictionary[word] = meaning

#print "dictionary: " + str(dictionary)
#word = 'haydır'
#print word
#print "dictionary['haydır']: " + dictionary['haydır']
#quit()

# api-endpoint
URL = "https://translation.googleapis.com/language/translate/v2"
from translation_key import *

filename = "build/" + prefix + "-" + language + ".vtt"
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
            #print "word: " + word
            if not dictionary.has_key(word):
                #dicValue = dictionary[word.decode('utf8')]
                #print "type(dicValue): " + str(type(dicValue))
                #if type(dicValue) is dict and dicValue['update'] == True:
                #    print(str(count) + ". needs update " + word + ": " + dicValue['en'].encode('utf8'))
                #    count = count + 1
                #    dicValue['update'] = False
                #    wordFile = "build/words/" + language + "/" + word + ".m4a"
                #    targetFile = "build/words/" + language + "/" + word + "-en.m4a"
                #    if word == dicValue['en'].encode('utf8'):
                #        os.system("rm -f " + wordFile)
                #        os.system("rm -f " + targetFile)
                #    else:
                #        subprocess.call(["say", "-v", "Alex", dicValue['en'], "-o", targetFile])
                #        targetFile = "build/words/" + language + "/" + word + ".m4a"
                #        targetFileMp3 = "build/words/" + language + "/" + word + ".mp3"
                #        if language == "ar":
                #            subprocess.call(["gtts-cli", word, "-l", "ar", "--output", targetFileMp3])
                #            os.system("ffmpeg -y -i " + targetFileMp3 + " -c:a aac -b:a 192k " + targetFile)
                #            os.system("rm " + targetFileMp3)
                #        else:
                #            subprocess.call(["say", "-v", voice, "-r", "125", word, "-o", targetFile])
                #elif type(dicValue) is unicode or type(dicValue) is str:
                #    dictionary[word.decode('utf8')] = {'en': dicValue, 'update': False}
            #else:
                #print "new word: " + word
                try:
                    count = count + 1
                    PARAMS = {'key':key, 'q':word, 'source':language, 'target':'en'}
                    r = requests.get(url = URL, params = PARAMS)
                    data = r.json()
                    translatedWord = data['data']['translations'][0]['translatedText'].replace('-','').replace("&#39;","'").replace("?","").lower()
                    dictionary[word] = translatedWord
                    #{'en': translatedWord, 'update': False}
                    print(str(count) + ". new word - " + word + ": " + translatedWord.encode('utf8'))
                    #if word != translatedWord.encode('utf8'):
                    #    targetFile = "build/words/" + language + "/" + word + ".m4a"
                    #    targetFileMp3 = "build/words/" + language + "/" + word + ".mp3"
                    #    if language == "ar":
                    #        subprocess.call(["gtts-cli", word, "-l", "ar", "--output", targetFileMp3])
                    #        os.system("ffmpeg -y -i " + targetFileMp3 + " -c:a aac -b:a 192k " + targetFile)
                    #        os.system("rm " + targetFileMp3)
                    #    else:
                    #        subprocess.call(["say", "-v", voice, "-r", "125", word, "-o", targetFile])
                    #    targetFile = "build/words/" + language + "/" + word + "-en.m4a"
                    #    subprocess.call(["say", "-v", "Alex", translatedWord, "-o", targetFile])
                    #if count % 100 == 0:
                    #    with io.open(dictionaryFile, 'w', encoding='utf8') as outfile:
                    #        yaml.dump(data, outfile, sort_keys=True, default_flow_style=False, allow_unicode=True)
                except Exception as error:
                    print "error: " + str(error) + " word: " + word
                    #json.dump(dictionary, open(dictionaryFile, 'w'), sort_keys = False, indent = 4, ensure_ascii = True)

file.close()
lines = []
with open(dictionaryFilePath, 'w') as outfile:
    for key in dictionary.keys():
        try:
            lines.append(key.encode('utf8') + ": " + dictionary[key].encode('utf8'))
        except:
            try:
                lines.append(str(key) + ": " + str(dictionary[key]))
            except Exception as error:
                print "error: " + str(error)
lines.sort()
with open(dictionaryFilePath, 'w') as outfile:
    for line in lines:
        outfile.write(line + "\n")
#with io.open(dictionaryFile, 'w', encoding='utf8') as outfile:
#with open(dictionaryFile, 'w') as outfile:
#    yaml.dump(dictionary, outfile, sort_keys=True)

#json.dump(dictionary, open(dictionaryFile, 'w'), sort_keys = False, indent = 4, ensure_ascii = True)
#os.system("python unicode.py " + dictionaryFile + " > build/dictionary-" + language + ".txt")

