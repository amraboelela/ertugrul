# importing the requests library
import sys, subprocess

if len(sys.argv) > 3:
    prefix = sys.argv[1]
    order = sys.argv[2]
    language = sys.argv[3]
else:
    print "please provide the prefix, the language order  and the language"
    exit(-1)

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
            count = count + 1
            print str(count) + ".saying: " + paragraph
            #if count>3:
            targetFile = "data/" + prefix + "/" + prefix + "-" + format(count, '03d') + "-" + order + language + ".m4a"
            if language == "en":
                subprocess.call(["say", "-v", voice, "-o", targetFile, paragraph])
            else:
                subprocess.call(["say", "-v", voice, "-r", "125", "-o", targetFile, paragraph])
            paragraph = ""
    else:
        paragraph = paragraph + line.replace('-','') + ", "
file.close()

