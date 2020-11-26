
import json, sys, subprocess, requests, re

if len(sys.argv) > 1:
    jsonFile = sys.argv[1]
else:
    print("please provide the json file")
    exit(-1)

try:
    dictionary = json.load(open(jsonFile))
except:
    dictionary = {}

for key in dictionary.keys():
    print key.encode('utf8') + ": " + dictionary[key]['en'].encode('utf8')
    #print key.encode('utf8') + " (" + key  + ")" + ": " + dictionary[key]['en'].encode('utf8')

