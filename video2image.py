
import sys, subprocess, os.path
from os import path

if len(sys.argv) > 2:
    prefix = sys.argv[1]
    targetLanguage = sys.argv[2]
else:
    print("please provide the prefix, and the target language")
    exit(-1)

print("## video2image, prefix: " + prefix + ", targetLanguage: " + targetLanguage)

filePath = "build/" + prefix + "-" + targetLanguage + ".vtt" 
file = open(filePath) 
lines = file.read().splitlines()
count = 0
filePrefix = "build/" + prefix + "/" + prefix + "-"

def videoToImage():
    audioFile = filePrefix + str(count).zfill(3) + "-" + targetLanguage + ".m4a"
    videoFile = filePrefix + str(count).zfill(3) + "-" + targetLanguage + "-a.mp4"
    imageFile = filePrefix + str(count).zfill(3) + "-" + targetLanguage + ".jpg"
    if not path.exists(imageFile) and path.exists(audioFile):
        subprocess.call(["ffmpeg", "-y", "-sseof", "-3", "-i", videoFile, "-update", "1", "-q:v", "1", imageFile])
 
for line in lines:
    if "-->" in line:
        if count > 0:
            videoToImage()
        count = count + 1

videoToImage()
file.close()
