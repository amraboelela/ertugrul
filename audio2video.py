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
for line in lines:
    if "-->" in line:
        if count > 0:
            audioFilePrefix = filePrefix + format(count, '03d') + "-1" + sourceLanguage
            audioFile = audioFilePrefix + ".m4a"
            imageFile = filePrefix + format(count, '03d') + "-" + targetLanguage + ".jpg"
            videoFile = audioFilePrefix + ".mp4"
            if not path.exists(videoFile):
                subprocess.call(["ffmpeg", "-y", "-loop", "1", "-i", imageFile, "-i", audioFile, "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", videoFile])
                subprocess.call(["rm", audioFile])
                subprocess.call(["rm", imageFile])
            audioFilePrefix = filePrefix + format(count, '03d') + "-3" + sourceLanguage + "-" + targetLanguage
            audioFile = audioFilePrefix + ".m4a"
            imageFile = filePrefix + format(count+1, '03d') + "-" + targetLanguage + ".jpg"
            videoFile = audioFilePrefix + ".mp4"
            if not path.exists(videoFile):
                subprocess.call(["ffmpeg", "-y", "-loop", "1", "-i", imageFile, "-i", audioFile, "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", videoFile])
                subprocess.call(["rm", audioFile])
                subprocess.call(["rm", imageFile])
        count = count + 1

file.close()

