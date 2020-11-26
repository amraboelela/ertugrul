import sys, subprocess, os.path
from os import path

if len(sys.argv) > 2:
    prefix = sys.argv[1]
    #order = sys.argv[2]
    targetLanguage = sys.argv[2]
else:
    print "please provide the prefix and the target language"
    exit(-1)

print "## cut, prefix: " + prefix + ", targetLanguage: " + targetLanguage

filePath = "build/" + prefix + "-" + targetLanguage + ".vtt" 
file = open(filePath) 
durationsFilePath = "build/durations.txt"
durationsFile = open(durationsFilePath, "w")

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
        totalSeconds = minutes * 60 + seconds
        timeStamp = totalSeconds + float(secondsArray[1]) / 1000
        duration = timeStamp - prevTimeStamp
        prevTimeStamp = timeStamp
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
        minutes = totalSeconds / 60 
        seconds = totalSeconds - minutes * 60
        startTime = str(minutes) + ":" + str(seconds) + "." + secondsArray[1]
        if count > 0:
            durationsFile.write(str(duration) + "\n")
            filePrefix = "build/" + prefix + "/" + prefix + "-" + format(count, '03d')
            targetFile = filePrefix + "-" + targetLanguage 
            if not path.exists(targetFile + "-a.mp4") and not path.exists(filePrefix + "-" + targetLanguage + ".jpg"):
                subprocess.call(["ffmpeg", "-y", "-i", "build/" + prefix + "-" + targetLanguage + ".m4a", "-acodec", "copy", "-ss", prevStartTime, "-to", startTime, targetFile + "~.m4a"])
                subprocess.call(["ffmpeg", "-y", "-i", targetFile + "~.m4a", "-filter:a", "volume=4.5", targetFile + "~~.m4a"])
                subprocess.call(["mv", targetFile + "~~.m4a", targetFile + ".m4a"])
                subprocess.call(["rm", targetFile + "~.m4a"])
                
                subprocess.call(["ffmpeg", "-y", "-i", "build/" + prefix + "-" + targetLanguage + ".mp4", "-acodec", "copy", "-ss", prevStartTime, "-to", startTime, targetFile + "-a~.mp4"])
                subprocess.call(["ffmpeg", "-y", "-i", targetFile + "-a~.mp4", "-filter:a", "volume=4.5", targetFile + "-a~~.mp4"])
                subprocess.call(["mv", targetFile + "-a~~.mp4", targetFile + "-a.mp4"])
                subprocess.call(["rm", targetFile + "-a~.mp4"])
        prevStartTime = startTime
        count = count + 1

if targetLanguage == "tr":
    filePrefix = "build/" + prefix + "/" + prefix + "-" + format(count, '03d')
    targetFile = filePrefix + "-" + targetLanguage
    if not path.exists(targetFile + "-a.mp4") and not path.exists(filePrefix + "-" + targetLanguage + ".jpg"):
        subprocess.call(["ffmpeg", "-y", "-i", "build/" + prefix + "-" + targetLanguage + ".m4a", "-acodec", "copy", "-ss", prevStartTime, "-t", "10", targetFile + "~.m4a"])
        subprocess.call(["ffmpeg", "-y", "-i", targetFile + "~.m4a", "-filter:a", "volume=4.5", targetFile + "~~.m4a"])
        subprocess.call(["mv", targetFile + "~~.m4a", targetFile + ".m4a"])
        subprocess.call(["rm", targetFile + "~.m4a"])

        subprocess.call(["ffmpeg", "-y", "-i", "build/" + prefix + "-" + targetLanguage + "-a.mp4", "-acodec", "copy", "-ss", prevStartTime, "-t", "10", targetFile + "-a~.mp4"])
        subprocess.call(["ffmpeg", "-y", "-i", targetFile + "-a~.mp4", "-filter:a", "volume=4.5", targetFile + "-a~~.mp4"])
        subprocess.call(["mv", targetFile + "-a~~.mp4", targetFile + "-a.mp4"])
        subprocess.call(["rm", targetFile + "-a~.mp4"])

file.close()
