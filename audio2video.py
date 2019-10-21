# importing the requests library
import sys, subprocess, os.path
from os import path

if len(sys.argv) > 3:
    prefix = sys.argv[1]
    order = sys.argv[2]
    targetLanguage = sys.argv[3]
else:
    print "please provide the prefix, order, and the target language"
    exit(-1)

filePath = "data/" + prefix + "-" + targetLanguage + ".vtt" 
file = open(filePath) 
lines = file.read().splitlines()
count = 0
filePrefix = "data/" + prefix + "/" + prefix + "-"
for line in lines:
    if "-->" in line:
        if count > 0:
            videoFile = filePrefix + format(count, '03d') + "-" + order + targetLanguage + ".mp4"
            frameFile = filePrefix + format(count, '03d') + "-" + targetLanguage + ".jpg"
            if not path.exists(frameFile):
                subprocess.call(["ffmpeg", "-y", "-i", videoFile + ".mp4", "-vf", '"select=eq(n\,0)"', "-q:v", "3", frameFile + ".jpg"])
        count = count + 1

videoFile = filePrefix + format(count-1, '03d') + "-" + order + targetLanguage + ".mp4" 
frameFile = filePrefix + format(count, '03d') + "-" + targetLanguage + ".jpg"

subprocess.call(["ffmpeg", "-y", "-sseof", "-3", "-i", videoFile + ".mp4", "-update", "1", "-q:v", "1", frameFile])

file.close()

