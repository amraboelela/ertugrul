
import sys, subprocess, os.path
from os import path

if len(sys.argv) > 2:
    prefix = sys.argv[1]
    targetLanguage = sys.argv[2]
else:
    print("please provide the prefix, and the target language")
    exit(-1)

print("## frames2video, prefix: " + prefix + ", targetLanguage: " + targetLanguage)

filePath = "build/" + prefix + "-" + targetLanguage + ".vtt"
file = open(filePath)
lines = file.read().splitlines()
count = 0
filePrefix = "build/" + prefix + "/" + prefix

def framesToVideo():
    videoFile = filePrefix + "-" + str(count).zfill(3) + "-" + targetLanguage + "-a.mp4"
    framePrefix = "build/" + prefix + "/frames/" + prefix + "-" + str(count).zfill(3)
    videoPrefix = filePrefix + "-" + str(count).zfill(3)
    if not path.exists(videoPrefix + "-" + targetLanguage + "-c.mp4") and path.exists(videoFile):
        print("Generating: " + videoPrefix + ".mp4")
        subprocess.call(["ffmpeg", "-y", "-r", "1", "-f", "image2", "-pattern_type", "glob", "-i", framePrefix + "-*.jpg", "-vcodec", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", videoPrefix + "-cm.mp4"])
        subprocess.call(["ffmpeg", "-y", "-i", videoPrefix + "-cm.mp4", "-i", videoPrefix + "-tr.m4a", "-c", "copy", "-map", "0:v:0", "-map", "1:a:0", videoPrefix + "-" + targetLanguage + "-c.mp4"])
        os.system("rm -f " + videoPrefix + "-cm.mp4")
 
for line in lines:
    if "-->" in line:
        if count > 0:
            framesToVideo()
        count = count + 1
file.close()
