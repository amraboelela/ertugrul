
import sys, subprocess, os.path
from os import path

if len(sys.argv) > 2:
    prefix = sys.argv[1]
    targetLanguage = sys.argv[2]
else:
    print("please provide the prefix, and the target language")
    exit(-1)

print("## editFrames, prefix: " + prefix + ", targetLanguage: " + targetLanguage)

filePath = "build/" + prefix + "-" + targetLanguage + ".vtt"
file = open(filePath)
lines = file.read().splitlines()
count = 0

def editFrame():
    framePrefix = "build/" + prefix+ "/frames/" + prefix + "-" + str(count).zfill(3)
    videoPrefix = "build/" + prefix + "-" + str(count).zfill(3)

    subprocess.call(["ffmpeg", "-y", "-r", "20", "-f", "image2", "-pattern_type", "glob", "-i", framePrefix + "-*.jpg", "-vcodec", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", videoPrefix + "-cm.mp4"])
    subprocess.call(["ffmpeg", "-y", "-i", videoPrefix + "-cm.mp4", "-i", videoPrefix + "-tr.m4a", "-c", "copy", "-map", "0:v:0", "-map", "1:a:0", videoPrefix + ".mp4"])
    os.system("rm -f " + videoPrefix + "-cm.mp4")
 
for line in lines:
    if "-->" in line:
        if count > 0:
            frameToVideo()
        count = count + 1
file.close()
