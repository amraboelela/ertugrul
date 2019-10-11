# importing the requests library
import sys, subprocess, os.path
from os import path

if len(sys.argv) > 3:
    prefix = sys.argv[1]
    order = sys.argv[2]
    language = sys.argv[3]
else:
    print "please provide the prefix, the language order  and the language"

filePath = "data/" + prefix + "-" + language + ".vtt"
switcher = {
        "en": "Alex",
        "tr": "Yelda",
        "ar": "Maged"
    }

voice = switcher.get(language)

file = open(filePath)
lines = file.read().splitlines()
count = 0
paragraph = ""
for line in lines:
    if "-->" in line:
        if len(paragraph) > 0:
            if count>3:
                targetFile = "data/" + prefix + "/" + prefix + "-" + format(count, '03d') + "-" + order + language + "-en.m4a"
                print str(count) + ".saying: " + paragraph
                paragraph = paragraph.lower().replace(":","").replace(",","").replace("?", "").replace("!", "").replace(".", "")
                words = paragraph.split()
                subprocessArray = ["ffmpeg", "-y"]
                concatString = ""
                fileCount = 0
                for word in words:
                    wordFile = "data/words/" + word + ".m4a"
                    if path.exists(wordFile):
                        print "saying: " + word
                        subprocessArray.extend(["-i", wordFile])
                        subprocessArray.extend(["-i", "silence1.m4a"])
                        concatString = concatString + "[" + str(fileCount) + ":a]"
                        fileCount = fileCount + 1
                        concatString = concatString + "[" + str(fileCount) + ":a]"
                        fileCount = fileCount + 1
                    enWordFile = "data/words/" + word + "-en.m4a"
                    if path.exists(enWordFile):
                        subprocessArray.extend(["-i", enWordFile])
                        subprocessArray.extend(["-i", "silence1.m4a"])
                        concatString = concatString + "[" + str(fileCount) + ":a]"
                        fileCount = fileCount + 1
                        concatString = concatString + "[" + str(fileCount) + ":a]"
                        fileCount = fileCount + 1
                    #subprocessArray.extend(["-i", "silence1.m4a"])
                    #concatString = concatString + "[" + str(fileCount) + ":a]"
                    #fileCount = fileCount + 1
                subprocessArray.extend(["-filter_complex", concatString + "concat=n=" + str(fileCount) + ":v=0:a=1", targetFile])
                subprocess.call(subprocessArray)
            paragraph = ""
            count = count + 1
    else:
        paragraph = paragraph + line.replace('-','') + ", "

file.close()

