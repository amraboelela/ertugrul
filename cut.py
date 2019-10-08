# importing the requests library
import sys, subprocess, os.path
from os import path

if len(sys.argv) > 2:
    prefix = sys.argv[1]
    targetLanguage = sys.argv[2]
else:
    print "please provide the prefix and the target language"
    exit(-1)

filePath = "data/" + prefix + "-en.vtt" 
file = open(filePath) 
lines = file.read().splitlines()
count = 0
prevStartTime = "00:00:00"
for line in lines:
    if "-->" in line:
        times = line.split(" --> ")
        startTime = times[0][:len(times[0])-4]
        print "startTime: " + startTime
        subTimes = startTime.split(":")
        hours = int(subTimes[0])
        minutes = int(subTimes[1])
        seconds = int(subTimes[2])
        print "hours: " + str(hours)
        print "minutes: " + str(minutes)
        print "seconds: " + str(seconds)
        totalSeconds = hours * 60 * 60 + minutes * 60 + seconds
        shiftedSeconds = 60 + 43
        #print "totalSeconds: " + str(totalSeconds)
        totalSeconds = totalSeconds - shiftedSeconds
        if totalSeconds < 0:
            totalSeconds = 0
        print "totalSeconds 2: " + str(totalSeconds)
        hours = totalSeconds / 60 / 60
        minutes = (totalSeconds - (hours * 60 * 60)) / 60 
        seconds = (totalSeconds - (hours * 60 * 60) - minutes * 60)
        #print "hours 2: " + str(hours)
        #print "minutes 2: " + str(minutes)
        #print "seconds 2: " + str(seconds)
        startTime = str(hours) + ":" + str(minutes) + ":" + str(seconds)
        #print "startTime 2: " + startTime
        #print "prevStartTime: " + prevStartTime
        if count > 4:
            #exit(0)
            targetFile = "data/" + prefix + "/" + prefix + "-" + format(count, '03d') + "-o" + targetLanguage
            if not path.exists(targetFile + ".m4a"):
                subprocess.call(["ffmpeg", "-y", "-i", "data/" + prefix + "-o" + targetLanguage + ".m4a", "-acodec", "copy", "-ss", prevStartTime, "-to", startTime, targetFile + "~.m4a"])
                subprocess.call(["ffmpeg", "-y", "-i", targetFile + "~.m4a", "-filter:a", "volume=4.5", targetFile + "~~.m4a"])
                subprocess.call(["ffmpeg", "-y", "-i", targetFile + "~.m4a", "-filter:a", "volume=4.5", targetFile + ".m4a"])
                subprocess.call(["mv", targetFile + "~~.m4a", targetFile + ".m4a"])
                subprocess.call(["rm", targetFile + "~.m4a"])
            #exit(0)
        prevStartTime = startTime
        count = count + 1
file.close()

