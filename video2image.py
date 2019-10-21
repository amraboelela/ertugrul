# importing the requests library
import sys, subprocess, os.path
from os import path

if len(sys.argv) > 2:
    prefix = sys.argv[1]
    targetLanguage = sys.argv[2]
else:
    print "please provide the prefix, and the target language"
    exit(-1)

filePath = "data/" + prefix + "-" + targetLanguage + ".vtt" 
file = open(filePath) 
lines = file.read().splitlines()
count = 0
filePrefix = "data/" + prefix + "/" + prefix + "-"
for line in lines:
    if "-->" in line:
        if count > 0:
            videoFile = filePrefix + format(count, '03d') + "-2" + targetLanguage + ".mp4"
            imageFile = filePrefix + format(count, '03d') + "-" + targetLanguage + ".jpg"
            if not path.exists(imageFile):
                subprocess.call(["ffmpeg", "-y", "-i", videoFile, "-vf", '"select=eq(n\,0)"', "-q:v", "3", imageFile])
        count = count + 1

videoFile = filePrefix + format(count-1, '03d') + "-2" + targetLanguage + ".mp4" 
imageFile = filePrefix + format(count, '03d') + "-" + targetLanguage + ".jpg"
if not path.exists(imageFile):
    subprocess.call(["ffmpeg", "-y", "-sseof", "-3", "-i", videoFile, "-update", "1", "-q:v", "1", imageFile])

file.close()

