
import sys, subprocess, os.path
from os import path

if len(sys.argv) > 3:
    prefix = sys.argv[1]
    order = sys.argv[2]
    language = sys.argv[3]
else:
    print "please provide the prefix, the language order and the language"

print "## sayWords, prefix: " + prefix + ", order: " + order + ", language: " + language

filePath = "build/" + prefix + "-" + language + ".vtt"
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

def sayWords():
    global count, paragraph
    targetFilePrefix = "build/" + prefix + "/" + prefix + "-" + format(count, '03d') + "-" + order + language + "-en"
    targetFile = targetFilePrefix + ".m4a"
    if len(paragraph) > 0 and count > 0 and not path.exists(targetFile) and not path.exists(targetFilePrefix + ".mp4"):
        print str(count) + ".saying: " + paragraph
        paragraph = paragraph.lower().replace(":","").replace(",","").replace("?", "").replace("!", "").replace(".", "")
        words = paragraph.split()
        subprocessArray = ["ffmpeg", "-y"]
        concatString = ""
        fileCount = 0
        for word in words:
            wordFile = "build/words/" + language + "/" + word + ".m4a"
            enWordFile = "build/words/" + language + "/" + word + "-en.m4a"
            if path.exists(wordFile) and path.exists(enWordFile):
                print "saying: " + word
                subprocessArray.extend(["-i", wordFile])
                subprocessArray.extend(["-i", "silence_2.m4a"])
                concatString = concatString + "[" + str(fileCount) + ":a]"
                fileCount = fileCount + 1
                concatString = concatString + "[" + str(fileCount) + ":a]"
                fileCount = fileCount + 1
                subprocessArray.extend(["-i", enWordFile])
                concatString = concatString + "[" + str(fileCount) + ":a]"
                fileCount = fileCount + 1
                if fileCount/4 < len(words) + 1:
                    subprocessArray.extend(["-i", "silence1.m4a"])
                else:
                    subprocessArray.extend(["-i", "silence_2.m4a"])
                concatString = concatString + "[" + str(fileCount) + ":a]"
                fileCount = fileCount + 1
        if fileCount > 0:
            subprocessArray.extend(["-filter_complex", concatString + "concat=n=" + str(fileCount) + ":v=0:a=1", targetFile])
            #print "subprocessArray: " + str(subprocessArray)
            subprocess.call(subprocessArray)
    paragraph = ""
    count = count + 1

for line in lines:
    if "-->" in line:
        sayWords()
    else:
        paragraph = paragraph + line.replace('-','') + ", "
sayWords()
file.close()

