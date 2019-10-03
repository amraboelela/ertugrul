# importing the requests library
import sys, subprocess

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print "please provide the vtt file name"
    exit(-1)

prefix = filename[:len(filename)-7]
language = filename[len(filename)-6:len(filename)-4]
switcher = {
        "en": "Alex",
        "tr": "Yelda",
        "ar": "Maged"
    }

voice = switcher.get(language)

subprocess.call(["mkdir", prefix])
file = open(filename)
lines = file.read().splitlines()
count = 0
paragraph = ""
for line in lines:
    if "-->" in line:
        if len(paragraph) > 0:
            print str(count) + ".saying: " + paragraph
            if count>4:
                if language == "en":
                    subprocess.call(["say", "-v", voice, "-o", prefix + "/" + prefix + "-" + format(count, '03d') + "-" + language + ".m4a", paragraph])
                else:
                    subprocess.call(["say", "-v", voice, "-r", "125", "-o", prefix + "/" + prefix + "-" + format(count, '03d') + "-" + language + ".m4a", paragraph])
            paragraph = ""
            count = count + 1
    else:
        paragraph = paragraph + line.replace('-','') + ", "
file.close()

