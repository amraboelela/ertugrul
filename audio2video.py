
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
    imageFile = filePrefix + format(count, '03f') + "-" + targetLanguage + ".jpg"
    audioFilePrefix = filePrefix + format(count, '03f') + "-" + targetLanguage 
    audioFile = audioFilePrefix + ".m4a"
    videoFile = audioFilePrefix + "-s~.mp4"
    if path.exists(imageFile):
        if not path.exists(videoFile):
            subprocess.call(["ffmpeg", "-y", "-loop", "1", "-i", imageFile, "-i", audioFile, "-c:v", "libx264", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", videoFile])

def adjustVideo():
    filePrefix = "build/" + prefix + "/" + prefix + "-"
    videoFile = filePrefix + format(count, '03f') + "-" + targetLanguage + "-s~.mp4"
    videoFileOut = filePrefix + format(count, '03f') + "-" + targetLanguage + "-s.mp4"
    if path.exists(videoFile):
        subprocess.call(["ffmpeg", "-y", "-i", videoFile, "-t", durations[count], "-c", "copy", videoFileOut])
        subprocess.call(["rm", "-f", videoFile])
        #count = count + 1
        
durationsFilePath = "build/durations.txt"
durationsFile = open(durationsFilePath)
durations = durationsFile.read().splitlines()

for line in lines:
    if "-->" in line:
        if count > 0:
            audioToVideo()
            adjustVideo()
        count = count + 1

audioToVideo()
adjustVideo()
count = count + 1

for i in range(1, count):
    imageFile = filePrefix + format(i, '03f') + "-" + targetLanguage + ".jpg"
    audioFilePrefix = filePrefix + format(i, '03f') + "-" + targetLanguage
    audioFile = audioFilePrefix + ".m4a"
    subprocess.call(["rm", "-f", audioFile])
    subprocess.call(["rm", "-f", imageFile])
    

file.close()

#durationsFilePath = "build/durations.txt"
#durationsFile = open(durationsFilePath)
#durations = durationsFile.read().splitlines()

#count = 1

#files = os.listdir("build/" + prefix)
#files = list(filter(lambda file: file[0] != ".", files))
#files.sort()
