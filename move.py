
import sys, subprocess, os.path
from os import path

if len(sys.argv) > 2:
    prefix = sys.argv[1]
    targetLanguage = sys.argv[2]
else:
    print("please provide the prefix and the target language")
    exit(-1)

print("## move, prefix: " + prefix + ", targetLanguage: " + targetLanguage)
filePath = "build/" + prefix + "-" + targetLanguage + ".vtt"
file = open(filePath)
lines = file.read().splitlines()
count = 0
filePrefix = "build/" + prefix + "/" + prefix + "-"

def moveVideo():
    filePrefix = "build/" + prefix + "/" + prefix + "-"
    videoFile = filePrefix + str(count).zfill(3) + "-" + targetLanguage + "-s~.mp4"
    videoFileOut = filePrefix + str(count).zfill(3) + "-" + targetLanguage + "-s.mp4"
    if path.exists(videoFile):
        subprocess.call(["mv", videoFile, videoFileOut])

for line in lines:
    if "-->" in line:
        if count > 0:
            moveVideo()
        count = count + 1
moveVideo()
file.close()
