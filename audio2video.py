
import sys, subprocess, os.path
from os import path

if len(sys.argv) > 3:
    prefix = sys.argv[1]
    sourceLanguage = sys.argv[2]
    targetLanguage = sys.argv[3]
else:
    print "please provide the prefix, source language, and the target language"
    exit(-1)

print "## audio2video, prefix: " + prefix + ", sourceLanguage: " + sourceLanguage + ", targetLanguage: " + targetLanguage
filePath = "build/" + prefix + "-" + targetLanguage + ".vtt" 
file = open(filePath) 
lines = file.read().splitlines()
count = 0
filePrefix = "build/" + prefix + "/" + prefix + "-"

def audioToVideo():
    imageFile = filePrefix + format(count, '03d') + "-" + targetLanguage + ".jpg"
    audioFilePrefix1 = filePrefix + format(count, '03d') + "-1o" + targetLanguage
    audioFilePrefix2 = filePrefix + format(count, '03d') + "-2" + targetLanguage + "-" + sourceLanguage
    audioFile1 = audioFilePrefix1 + ".m4a"
    videoFile1 = audioFilePrefix1 + ".mp4"
    audioFile2 = audioFilePrefix2 + ".m4a"
    videoFile2 = audioFilePrefix2 + ".mp4"
    if path.exists(imageFile):
        if not path.exists(videoFile1):
            subprocess.call(["ffmpeg", "-y", "-loop", "1", "-i", imageFile, "-i", audioFile1, "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", videoFile1])
        if not path.exists(videoFile2):
            subprocess.call(["ffmpeg", "-y", "-loop", "1", "-i", imageFile, "-i", audioFile2, "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", videoFile2])

for line in lines:
    if "-->" in line:
        if count > 0:
            audioToVideo()
        count = count + 1

audioToVideo()
count = count + 1

for i in range(1, count):
    imageFile = filePrefix + format(i, '03d') + "-" + targetLanguage + ".jpg"
    audioFilePrefix1 = filePrefix + format(i, '03d') + "-1o" + targetLanguage
    audioFilePrefix2 = filePrefix + format(i, '03d') + "-2" + targetLanguage + "-" + sourceLanguage
    audioFile1 = audioFilePrefix1 + ".m4a"
    audioFile2 = audioFilePrefix2 + ".m4a"
    subprocess.call(["rm", "-f", audioFile1])
    subprocess.call(["rm", "-f", audioFile2])
    subprocess.call(["rm", "-f", imageFile])

file.close()
