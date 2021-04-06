import sys, subprocess, os.path
from os import path
import durationLimit

if len(sys.argv) > 2:
    prefix = sys.argv[1]
    targetLanguage = sys.argv[2]
else:
    print("please provide the prefix and the target language")
    exit(-1)

print("## cut, prefix: " + prefix + ", targetLanguage: " + targetLanguage)

durationLowerLimit = durationLimit.lowerLimit(prefix, targetLanguage)
durationUpperLimit = durationLimit.upperLimit(targetLanguage)
#print("durationUpperLimit: " + str(durationUpperLimit))

filePath = "build/" + prefix + "-" + targetLanguage + ".vtt"
print("cut filePath: " + filePath)
file = open(filePath)

lines = file.read().splitlines()
count = 0
prevStartTime = "00:00"
prevTimeStamp = 0

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
        milliseconds = int(secondsArray[1])
        timeStamp = durationLimit.timeStamp(prefix, targetLanguage, minutes, seconds, milliseconds)
        #print("timeStamp: " + str(timeStamp))
        duration = timeStamp - prevTimeStamp
        prevTimeStamp = timeStamp
        minutes = int(timeStamp) / 60
        seconds = int(timeStamp) - minutes * 60
        startTime = str(minutes) + ":" + str(seconds) + "." + secondsArray[1]
        print("startTime: " + startTime)
        if count > 0 and duration > durationLowerLimit and duration < durationUpperLimit:
            filePrefix = "build/" + prefix + "/" + prefix + "-" + str(count).zfill(3)
            targetFile = filePrefix + "-" + targetLanguage
            if not path.exists(targetFile + "-a.mp4") and not path.exists(targetFile + ".jpg"):
                subprocess.call(["ffmpeg", "-y", "-i", "build/" + prefix + "-" + targetLanguage + ".m4a", "-acodec", "copy", "-ss", prevStartTime, "-to", startTime, targetFile + "~.m4a"])
                subprocess.call(["ffmpeg", "-y", "-i", targetFile + "~.m4a", "-filter:a", "volume=4.5", targetFile + "~~.m4a"])
                subprocess.call(["mv", targetFile + "~~.m4a", targetFile + ".m4a"])
                subprocess.call(["rm", targetFile + "~.m4a"])
                
                subprocess.call(["ffmpeg", "-y", "-i", "build/" + prefix + "-" + targetLanguage + ".mp4", "-acodec", "copy", "-ss", prevStartTime, "-to", startTime, targetFile + "-a~.mp4"])
                subprocess.call(["ffmpeg", "-y", "-i", targetFile + "-a~.mp4", "-filter:a", "volume=4.5", targetFile + "-a~~.mp4"])
                subprocess.call(["mv", targetFile + "-a~~.mp4", targetFile + "-a.mp4"])
                subprocess.call(["rm", targetFile + "-a~.mp4"])
            else:
                print("targetFile already exists: " + targetFile)
        else:
            print("not accepted count, duration: " + str(count) + ", " + str(duration))
        prevStartTime = startTime
        count = count + 1
#quit()
if targetLanguage == "tr":
    filePrefix = "build/" + prefix + "/" + prefix + "-" + str(count).zfill(3)
    targetFile = filePrefix + "-" + targetLanguage
    if not path.exists(targetFile + "-a.mp4") and not path.exists(filePrefix + "-" + targetLanguage + ".jpg"):
        subprocess.call(["ffmpeg", "-y", "-i", "build/" + prefix + "-" + targetLanguage + ".m4a", "-acodec", "copy", "-ss", prevStartTime, "-t", "10", targetFile + "~.m4a"])
        subprocess.call(["ffmpeg", "-y", "-i", targetFile + "~.m4a", "-filter:a", "volume=4.5", targetFile + "~~.m4a"])
        subprocess.call(["mv", targetFile + "~~.m4a", targetFile + ".m4a"])
        subprocess.call(["rm", targetFile + "~.m4a"])

        subprocess.call(["ffmpeg", "-y", "-i", "build/" + prefix + "-" + targetLanguage + ".mp4", "-acodec", "copy", "-ss", prevStartTime, "-t", "10", targetFile + "-a~.mp4"])
        subprocess.call(["ffmpeg", "-y", "-i", targetFile + "-a~.mp4", "-filter:a", "volume=4.5", targetFile + "-a~~.mp4"])
        subprocess.call(["mv", targetFile + "-a~~.mp4", targetFile + "-a.mp4"])
        subprocess.call(["rm", targetFile + "-a~.mp4"])

file.close()
