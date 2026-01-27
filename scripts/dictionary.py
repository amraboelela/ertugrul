# -*- coding: utf-8 -*-

import json, sys, subprocess, requests, re, os

if len(sys.argv) > 2:
    prefix = sys.argv[1]
    language = sys.argv[2]
else:
    print("please provide the prefix and the language")
    exit(-1)

print("## dictionary, prefix: " + prefix + ", language: " + language)

dictionaryFilePath = "build/dictionary-" + language + ".txt"
dictionaryFile = open(dictionaryFilePath)
dictionaryLines = dictionaryFile.read().splitlines()
dictionary = {}
for dictionaryLine in dictionaryLines:
    lineSplit = dictionaryLine.split(":")
    word = lineSplit[0].strip()
    if len(lineSplit) > 1:
        meaning = lineSplit[1].strip()
        #print("word: " + word)
        dictionary[word] = meaning
    else:
        print("word without meaning: " + word)

# api-endpoint
URL = "https://translation.googleapis.com/language/translate/v2"
from translation_key import *

filename = "build/" + prefix + "-" + language + ".vtt"
#print("filename: " + filename)
file = open(filename)
lines = file.read().splitlines()
count  = 0
for line in lines:
    if not "-->" in line and len(line) > 0:
        line = line.lower().replace(":","").replace(",","").replace(";","").replace("?", "").replace("!", "").replace(".", "").replace("[", "").replace("]", "").replace("-", "").replace("[","").replace("]","").replace("<i>","").replace("</i>","").replace('"', '').replace("'", "")
        #print("line: " + line)
        words = line.split()
        for word in words:
            #print("word: " + word)
            if word not in dictionary:
                try:
                    count = count + 1
                    PARAMS = {'key':key, 'q':word, 'source':language, 'target':'en'}
                    r = requests.get(url = URL, params = PARAMS)
                    data = r.json()
                    translatedWord = data['data']['translations'][0]['translatedText'].replace('-','').replace("&#39;","'").replace("?","").lower()
                    dictionary[word] = translatedWord
                    print(str(count) + ". new word - " + word + ": " + translatedWord)
                except Exception as error:
                    print("error: " + str(error) + " word: " + word)

file.close()
lines = []
with open(dictionaryFilePath, 'w') as outfile:
    for key in dictionary.keys():
        try:
            lines.append(key + ": " + dictionary[key])
        except:
            try:
                lines.append(str(key) + ": " + str(dictionary[key]))
            except Exception as error:
                print("error: " + str(error))
lines.sort()
with open(dictionaryFilePath, 'w') as outfile:
    for line in lines:
        outfile.write(line + "\n")
