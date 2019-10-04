# importing the requests library
import sys, subprocess

if len(sys.argv) > 2:
    prefix = sys.argv[1]
    language = sys.argv[2]
else:
    print "please provide the prefix and the language"
    exit(-1)

filePath = "output/" + prefix + "/" + prefix + "-en.vtt"
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
            print str(count) + ".saying: " + paragraph
            if count>4:
                targetFilePath = "output/" + prefix + "/" + prefix + "-" + format(count, '03d') + "-" + language
                if language == "en":
                    subprocess.call(["say", "-v", voice, "-o", targetFilePath + ".m4a", "\n\n" + paragraph + "\n\n"])
                    #subprocess.call(["ffmpeg", "-y", "-i", targetFilePath + ".m4a", "-acodec", "libmp3lame", "-ab", "128k", targetFilePath + ".mp3"])
                    #exit(0)
                else:
                    subprocess.call(["say", "-v", voice, "-r", "125", "-o", targetFilePath + ".m4a", paragraph])
            paragraph = ""
            count = count + 1
    else:
        paragraph = paragraph + line.replace('-','') + ", "
file.close()

