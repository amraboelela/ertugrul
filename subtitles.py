# importing the requests library
import sys, subprocess, os.path
from os import path

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
        targetFileMp3 = "data/" + prefix + "/" + prefix + "-" + format(count, '03d') + "-" + order + language + ".mp3"
        targetFilePrefix = "data/" + prefix + "/" + prefix + "-" + format(count, '03d') + "-" + order + language
        targetFile = targetFilePrefix + ".m4a"
        fileCount = 0
        if len(paragraph) > 0 and count > 0 and not path.exists(targetFile):
            print str(count) + ".saying: " + paragraph
            if language == "en":
                subprocess.call(["say", "-v", voice, "-o", targetFilePrefix + "~.m4a", paragraph])
            else:
                if language == "ar":
                    command = "gtts-cli '" + paragraph +  "' -l ar --output " + targetFileMp3
                    os.system(command)
                    os.system("ffmpeg -i " + targetFileMp3 + " -c:a aac -b:a 192k " + targetFilePrefix + "~.m4a")
                    os.system("rm " + targetFileMp3)
                else:
                    subprocess.call(["say", "-v", voice, "-r", "125", "-o", targetFilePrefix + "~.m4a", paragraph])
            subprocessArray = ["ffmpeg", "-y"]
            concatString = ""
            subprocessArray.extend(["-i", targetFilePrefix + "~.m4a"])
            subprocessArray.extend(["-i", "silence1.m4a"])
            concatString = concatString + "[" + str(fileCount) + ":a]"
            fileCount = fileCount + 1
            concatString = concatString + "[" + str(fileCount) + ":a]"
            fileCount = fileCount + 1
            subprocessArray.extend(["-filter_complex", concatString + "concat=n=" + str(fileCount) + ":v=0:a=1", targetFilePrefix + ".m4a"])
            subprocess.call(subprocessArray)
            os.system("rm " + targetFilePrefix + "~.m4a")
        paragraph = ""
        count = count + 1
    else:
        paragraph = paragraph + line.replace('-','') + ", "
file.close()

