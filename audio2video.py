# importing the requests library
import sys, subprocess, os.path
from os import path

if len(sys.argv) > 3:
    prefix = sys.argv[1]
    sourceLanguage = sys.argv[2]
    targetLanguage = sys.argv[3]
else:
    print "please provide the prefix, source language, and the target language"
    exit(-1)

filePath = "data/" + prefix + "-" + targetLanguage + ".vtt" 
file = open(filePath) 
lines = file.read().splitlines()
count = 0
filePrefix = "data/" + prefix + "/" + prefix + "-"

def audioToVideo():
    imageFile = filePrefix + format(count, '03d') + "-" + targetLanguage + ".jpg"
    audioFilePrefix = filePrefix + format(count, '03d') + "-2" + targetLanguage + "-" + sourceLanguage
    audioFile = audioFilePrefix + ".m4a"
    videoFile = audioFilePrefix + ".mp4"
    if not path.exists(videoFile):
        subprocess.call(["ffmpeg", "-y", "-loop", "1", "-i", imageFile, "-i", audioFile, "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", videoFile])

for line in lines:
    if "-->" in line:
        if count > 0:
            audioToVideo()
        count = count + 1

audioToVideo()
count = count + 1

for i in range(1, count):
    imageFile = filePrefix + format(i, '03d') + "-" + targetLanguage + ".jpg"
    audioFilePrefix = filePrefix + format(i, '03d') + "-2" + targetLanguage + "-" + sourceLanguage
    audioFile = audioFilePrefix + ".m4a"
    subprocess.call(["rm", "-f", audioFile])
    subprocess.call(["rm", "-f", imageFile])

file.close()

