
import sys, subprocess, os.path
from os import path

if len(sys.argv) > 2:
    prefix = sys.argv[1]
    targetLanguage = sys.argv[2]
else:
    print("please provide the prefix and the target language")
    exit(-1)

print("## audio2video, prefix: " + prefix + ", targetLanguage: " + targetLanguage)
filePath = "build/" + prefix + "-" + targetLanguage + ".vtt" 
file = open(filePath) 
lines = file.read().splitlines()
count = 0
filePrefix = "build/" + prefix + "/" + prefix + "-"

def audioToVideo():
    imageFile = filePrefix + str(count).zfill(3) + "-" + targetLanguage + ".jpg"
    audioFilePrefix = filePrefix + str(count).zfill(3) + "-" + targetLanguage
    audioFile = audioFilePrefix + ".m4a"
    videoFile = audioFilePrefix + "-s~.mp4"
    if path.exists(imageFile):
        if not path.exists(videoFile):
            subprocess.call(["ffmpeg", "-y", "-loop", "1", "-i", imageFile, "-i", audioFile, "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", videoFile])

def adjustVideo():
    filePrefix = "build/" + prefix + "/" + prefix + "-"
    videoFile = filePrefix + str(count).zfill(3) + "-" + targetLanguage + "-s~.mp4"
    videoFileOut = filePrefix + str(count).zfill(3) + "-" + targetLanguage + "-s.mp4"
    if path.exists(videoFile):
        subprocess.call(["ffmpeg", "-y", "-i", videoFile, "-t", durations[count], "-c", "copy", videoFileOut])
        subprocess.call(["rm", "-f", videoFile])

def deleteFiles():
    imageFile = filePrefix + str(count).zfill(3) + "-" + targetLanguage + ".jpg"
    audioFilePrefix = filePrefix + str(count).zfill(3) + "-" + targetLanguage
    audioFile = audioFilePrefix + ".m4a"
    subprocess.call(["rm", "-f", audioFile])
    subprocess.call(["rm", "-f", imageFile])
    
def processFiles():
    audioToVideo()
    #adjustVideo()
    deleteFiles()
            
durationsFilePath = "build/durations.txt"
durationsFile = open(durationsFilePath)
durations = durationsFile.read().splitlines()

for line in lines:
    if "-->" in line:
        if count > 0:
            processFiles()
        count = count + 1

processFiles()
count = count + 1

file.close()
