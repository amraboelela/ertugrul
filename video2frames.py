
import sys, subprocess, os.path
from os import path

if len(sys.argv) > 2:
    prefix = sys.argv[1]
    targetLanguage = sys.argv[2]
else:
    print("please provide the prefix, and the target language")
    exit(-1)

print("## video2Frames, prefix: " + prefix + ", targetLanguage: " + targetLanguage)

filePath = "build/" + prefix + "-" + targetLanguage + ".vtt" 
file = open(filePath) 
lines = file.read().splitlines()
count = 0
filePrefix = "build/" + prefix + "/" + prefix + "-"

def videoToFrames():
    videoFile = filePrefix + str(count).zfill(3) + "-" + targetLanguage + "-a.mp4"
    imageFilePrefix = "build/" + prefix + "/frames/" + prefix + "-" + str(count).zfill(3)
    imageFile = imageFilePrefix + "-%4d.jpg"
    firstImageFile = imageFilePrefix + "-0001.jpg"
    if not path.exists(firstImageFile) and not path.exists(imageFilePrefix + "-0001-cm.jpg") and path.exists(videoFile):
        subprocess.call(["ffmpeg", "-y", "-i", videoFile, "-r", "20", imageFile])
 
for line in lines:
    if "-->" in line:
        if count > 0:
            videoToFrames()
        count = count + 1
        #quit()

#videoToFrames()
file.close()
