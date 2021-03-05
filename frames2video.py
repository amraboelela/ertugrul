
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

frameRate = 1
if targetLanguage == "ar":
    frameRate = 24
def framesToVideo():
    #print("framesToVideo")
    videoPrefix = filePrefix + "-" + str(count).zfill(3)
    videoFile = videoPrefix + "-" + targetLanguage + "-a.mp4"
    #print(videoFile)
    framePrefix = "build/" + prefix + "/frames/" + prefix + "-" + str(count).zfill(3)
    #if path.exists(videoFile):
    #    print("videoFile exists: " + videoFile)
    #else:
    #    print("videoFile not exists: " + videoFile)
    cVideoFile = videoPrefix + "-" + targetLanguage + "-c.mp4"
    #if not path.exists(cVideoFile):
    #    print("cVideoFile not exists: " + cVideoFile)
    #else:
    #    print("cVideoFile exists: " + cVideoFile)
    if not path.exists(cVideoFile) and path.exists(videoFile):
        print("Generating: " + videoPrefix + ".mp4")
        subprocess.call(["ffmpeg", "-y", "-r", str(frameRate), "-f", "image2", "-pattern_type", "glob", "-i", framePrefix + "-*.jpg", "-vcodec", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", videoPrefix + "-cm.mp4"])
        subprocess.call(["ffmpeg", "-y", "-i", videoPrefix + "-cm.mp4", "-i", videoPrefix + "-" + targetLanguage + ".m4a", "-c", "copy", "-map", "0:v:0", "-map", "1:a:0", cVideoFile])
        os.system("rm -f " + videoPrefix + "-cm.mp4")
 
for line in lines:
    if "-->" in line:
        if count > 0:
            framesToVideo()
        count = count + 1
file.close()
