# importing the requests library
import sys, subprocess

if len(sys.argv) > 2:
    filename = sys.argv[1]
    language = sys.argv[2]
else:
    print "please provide the file name and its language"
    exit(-1)

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
        print
    else:
        count = count + 1
        print("saying: " + line)
        subprocess.call(["say", "-v", voice, "-o", "audio/" + "filename + "-" + format(count, '04d') + ".m4a", line])
file.close()

