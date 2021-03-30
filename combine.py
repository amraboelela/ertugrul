# importing the requests library
import os, sys, subprocess, os.path
from os import path
import durationLimit

if len(sys.argv) > 3:
    prefix = sys.argv[1]
    targetLanguage = sys.argv[2]
    postfix = sys.argv[3]
else:
    print("please provide prefix, target language, and postfix")
    exit(-1)
    
print("## combin, prefix: " + prefix + ", postfix: " + postfix)

durationLowerLimit = durationLimit.lowerLimit(prefix, targetLanguage)
durationUpperLimit = durationLimit.upperLimit(targetLanguage)

filePath = "build/" + prefix + "-" + targetLanguage + ".vtt"
file = open(filePath)
lines = file.read().splitlines()
prevStartTime = "00:00"
prevTimeStamp = 0
subprocessArray = ["ffmpeg", "-y"]
count = 0
includeCount = 0
fileCount = 0
concatString = ""

for line in lines:
    if "-->" in line:
        times = line.split(" --> ")
        startTime = times[0]
        if targetLanguage == "tr":
            startTime = "00:" + startTime
        subTimes = startTime.split(":")
        hours = int(subTimes[0])
        minutes = int(subTimes[1])
        secondsArray = subTimes[2].split(".")
        seconds = int(secondsArray[0])
        totalSeconds = minutes * 60 + seconds
        timeStamp = totalSeconds + float(secondsArray[1]) / 1000
        #print("timeStamp: " + str(timeStamp))
        duration = timeStamp - prevTimeStamp
        prevTimeStamp = timeStamp
        #print("durationLowerLimit: " + str(durationLowerLimit))
        if count > 0 and duration > durationLowerLimit and duration < durationUpperLimit:
            filePrefix = "build/" + prefix + "/" + prefix + "-" + str(count).zfill(3)
            targetFile = filePrefix + "-" + targetLanguage
#            if not path.exists(targetFile + "-a.mp4") and not path.exists(filePrefix + "-" + targetLanguage + ".jpg"):
            #    subprocess.call(["ffmpeg", "-y", "-i", "build/" + prefix + "-" + targetLanguage + ".mp4"
            subprocessArray.extend(["-i", filePrefix + "-" + targetLanguage + "-" + postfix + ".mp4"])
            concatString = concatString + "[" + str(fileCount) + ":v][" + str(fileCount) + ":a]"
            fileCount = fileCount + 1
            includeCount = includeCount + 1
            if includeCount % 100 == 0:
                targetFile = "build/" + prefix + "-" + str(includeCount / 100).zfill(2) + "-" + postfix + ".mp4"
                if not path.exists(targetFile):
                    subprocessArray.extend(["-filter_complex", concatString + "concat=n=" + str(fileCount) + ":v=1:a=1", targetFile])
                    #print("subprocessArray: " + str(subprocessArray))
                    subprocess.call(subprocessArray)
                fileCount = 0
                concatString = ""
                subprocessArray = ["ffmpeg", "-y"]
        count = count + 1
#quit()
if includeCount % 100 > 1:
    n = includeCount / 100 + 1
    targetFile = "build/" + prefix + "-" + str(n).zfill(2) + "-" + postfix + ".mp4"
    print "targetFile: " + targetFile
    if not path.exists(targetFile):
        subprocessArray.extend(["-filter_complex", concatString + "concat=n=" + str(fileCount) + ":v=1:a=1", targetFile])
        print("subprocessArray: " + str(subprocessArray))
        subprocess.call(subprocessArray)
else:
    n = 1
concatString = ""
subprocessArray = ["ffmpeg", "-y"]
targetFile = "build/" + prefix + "-" + postfix + ".mp4"
if not path.exists(targetFile):
    for i in range(0, n):
        subprocessArray.extend(["-i", "build/" + prefix + "-" + str(i+1).zfill(2) + "-" + postfix + ".mp4"])
        concatString = concatString + "[" + str(i) + ":v][" + str(i) + ":a]"
    subprocessArray.extend(["-filter_complex", concatString + "concat=n=" + str(n) + ":v=1:a=1", targetFile])
    subprocess.call(subprocessArray)
