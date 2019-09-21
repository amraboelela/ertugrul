# importing the requests library
import sys, subprocess

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print "please provide the file name and its language"
    exit(-1)

language = filename[len(filename)-6:len(filename)-4]
switcher = {
        "en": "Alex",
        "tr": "Yelda",
        "ar": "Maged"
    }

voice = switcher.get(language)

file = open(filename)
lines = file.read().splitlines()
count = 0
for line in lines:
    if not line.strip():
        x = 0
    else:
        count = count + 1
        print(str(count) + ".saying: " + line)
        if language == "en":
            subprocess.call(["say", "-v", voice, "-o", "audio/" + filename.replace('.srt', '') + "-" + format(count, '04d') + ".m4a", line])
        else:
            subprocess.call(["say", "-v", voice, "-r", "130", "-o", "audio/" + filename.replace('.srt', '') + "-" + format(count, '04d') + ".m4a", line])
file.close()

