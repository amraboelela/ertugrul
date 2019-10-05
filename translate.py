# importing the requests library
import sys, subprocess, requests

if len(sys.argv) > 2:
    filename = sys.argv[1]
    targetLanguage = sys.argv[2]
else:
    print "please provide the file name and the target language"
    exit(-1)

# api-endpoint
URL = "https://translation.googleapis.com/language/translate/v2"
from translation_key import *

#print "filename: " + filename
file = open(filename)
#print "file: " + str(file)
lines = file.read().splitlines()
#print "lines: " + str(lines)
#count = 0
paragraph = ""
#exit(0)
for line in lines:
    #print "line: " + line
    if "-->" in line:
        if len(paragraph) > 0:
            #if count>4:
            #print str(count) + ".translating: " + paragraph
            #targetFilePath = "data/" + prefix + "-" + format(count, '03d') + "-" + language
            #print("targetLanguage: " + targetLanguage)
            PARAMS = {'key':key, 'q':paragraph, 'source':'en', 'target':targetLanguage}
            r = requests.get(url = URL, params = PARAMS)
            data = r.json()
            #print "data: " + str(data)
            #exit(0)
            translatedText = data['data']['translations'][0]['translatedText'].replace('-','').replace("&#39;","'")
            try:
                print(translatedText.encode('utf8'))
                print
            except Exception as error:
                print "error: " + str(error) + " line: " + line

#                if language == "en":
#                    subprocess.call(["say", "-v", voice, "-o", targetFilePath + ".m4a", paragraph])
#                else:
#                    subprocess.call(["say", "-v", voice, "-r", "125", "-o", targetFilePath + ".m4a", paragraph])

        print line
        paragraph = ""
    else:
        paragraph = paragraph + line.replace('-','') + ", "


PARAMS = {'key':key, 'q':paragraph, 'source':'en', 'target':targetLanguage}
r = requests.get(url = URL, params = PARAMS)
data = r.json()
translatedText = data['data']['translations'][0]['translatedText'].replace('-','').replace("&#39;","'")
try:
    print(translatedText.encode('utf8'))
    print
except Exception as error:
    print "error: " + str(error) + " line: " + line


#    if not line.strip():
#        print
#    elif "-->" in line:
#        x = 0
#    else:
#        PARAMS = {'key':key, 'q':line, 'source':'en', 'target':targetLanguage}
#        r = requests.get(url = URL, params = PARAMS)
#        data = r.json()
#        translatedText = data['data']['translations'][0]['translatedText'].replace('-','').replace("&#39;","'")
#        try:
#            print(translatedText.encode('utf8'))
#        except Exception as error:
#            print "error: " + str(error) + " line: " + line

file.close()

