
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
    files = os.listdir("build/" + prefix+ "/frames/")
    files = list(filter(lambda file: prefix + "-" + str(count).zfill(3) + "-" in file, files))
    files = list(filter(lambda file: "-cm." not in file and "-cr." not in file and "-rs." not in file, files))
    files.sort()
    for file in files:
        fileSplit = file.split(".")
        fileTokens = fileSplit[0].split("-")
        frameID = fileTokens[-1]
        #backImagePrefix = "build/" + prefix + "-tr"
        backImage = "build/greenGrass.jpg"
        imagePrefix = framePrefix + "-" + frameID
        if not path.exists(imagePrefix + "-cm.jpg"):
            print("Editing: " + imagePrefix + ".jpg")
            os.system("mv " + imagePrefix + ".jpg " + imagePrefix + "-cm.jpg")
                        
            #subprocess.call(["convert", backImagePrefix + ".jpg", "-crop", "800x482+230+0", backImagePrefix + "-cr.jpg"])
            #subprocess.call(["convert", imagePrefix + ".jpg", "-crop", "1660x1070+250+0", imagePrefix + "-cr.jpg"])
            #subprocess.call(["convert", imagePrefix + "-cr.jpg", "-resize", "40%", imagePrefix + "-rs.jpg"])
            #subprocess.call(["magick", "composite", "-gravity", "north", imagePrefix + "-rs.jpg", backImage, imagePrefix + "-cm.jpg"])
            #os.system("rm -f " + imagePrefix + ".jpg")
            #os.system("rm -f " + imagePrefix + "-rs.jpg")
            #os.system("rm -f " + imagePrefix + "-cr.jpg")
 
for line in lines:
    if "-->" in line:
        if count > 0:
            editFrame()
        count = count + 1
file.close()
