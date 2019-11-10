# importing the requests library
import sys, subprocess, os.path
from os import path

if len(sys.argv) > 3:
    prefix = sys.argv[1]
    order = sys.argv[2]
    targetLanguage = sys.argv[3]
else:
    print "please provide the prefix, language order, and the target language"
    exit(-1)

print "## sayWords, prefix: " + prefix + ", order: " + order + ", targetLanguage: " + targetLanguage

filePath = "data/" + prefix + "-" + targetLanguage + ".vtt" 
file = open(filePath) 
lines = file.read().splitlines()
count = 0
prevStartTime = "00:00"
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
        shiftedSeconds = 0
        if targetLanguage == "ar":
            subPrefix = prefix[:11]
            if subPrefix == "ertugrul-1-":
                episode = prefix[11:13]
                #print "episode: " + episode
                if episode == "01" or episode == "02" or episode == "04" or episode == "06":
                    shiftedSeconds = 60 + 43
                elif episode == "03" or episode == "05":
                    shiftedSeconds = 60 + 41
                elif episode == "12":
                    shiftedSeconds = 2 * 60 + 7
                elif episode == "13" or episode == "20":
                    shiftedSeconds = 2 * 60
                else:
                    shiftedSeconds = 2 * 60 + 2

        totalSeconds = totalSeconds - shiftedSeconds
        if totalSeconds < 0:
            totalSeconds = 0
        #hours = totalSeconds / 60 / 60
        minutes = totalSeconds / 60 
        seconds = totalSeconds - minutes * 60
        startTime = str(minutes) + ":" + str(seconds) + "." + secondsArray[1]
        #print "startTime: " + startTime
        if count > 0:
            targetFile = "data/" + prefix + "/" + prefix + "-" + format(count, '03d') + "-" + order + "o" + targetLanguage
            if not path.exists(targetFile + ".mp4"):
                subprocess.call(["ffmpeg", "-y", "-i", "data/" + prefix + "-o" + targetLanguage + ".mp4", "-acodec", "copy", "-ss", prevStartTime, "-to", startTime, targetFile + "~.mp4"])
                subprocess.call(["ffmpeg", "-y", "-i", targetFile + "~.mp4", "-filter:a", "volume=4.5", targetFile + "~~.mp4"])
                subprocess.call(["mv", targetFile + "~~.mp4", targetFile + ".mp4"])
                subprocess.call(["rm", targetFile + "~.mp4"])
        prevStartTime = startTime
        count = count + 1

targetFile = "data/" + prefix + "/" + prefix + "-" + format(count, '03d') + "-" + order + "o" + targetLanguage
if not path.exists(targetFile + ".mp4"): 
    subprocess.call(["ffmpeg", "-y", "-i", "data/" + prefix + "-o" + targetLanguage + ".mp4", "-acodec", "copy", "-ss", prevStartTime, "-t", "10", targetFile + "~.mp4"])
    subprocess.call(["ffmpeg", "-y", "-i", targetFile + "~.mp4", "-filter:a", "volume=4.5", targetFile + "~~.mp4"])
    subprocess.call(["mv", targetFile + "~~.mp4", targetFile + ".mp4"])
    subprocess.call(["rm", targetFile + "~.mp4"])

file.close()

