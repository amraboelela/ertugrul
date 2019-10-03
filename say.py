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
                targetFilePath = prefix + "/" + prefix + "-" + format(count, '03d') + "-" + language
                if language == "en":
                    subprocess.call(["say", "-v", voice, "-o", targetFilePath + ".m4a", paragraph])
                    subprocess.call(["ffmpeg", "-y", "-i", targetFilePath + ".m4a", "-acodec", "libmp3lame", "-ab", "128k", targetFilePath + ".mp3"])
                    exit(0)
                else:
                    subprocess.call(["say", "-v", voice, "-r", "125", "-o", targetFilePath + ".m4a", paragraph])
            paragraph = ""
            count = count + 1
    else:
        paragraph = paragraph + line.replace('-','') + ", "
file.close()

