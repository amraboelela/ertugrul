import sys, subprocess, os.path
from os import path

if len(sys.argv) > 3:
    prefix = sys.argv[1]
    order = sys.argv[2]
    targetLanguage = sys.argv[3]
else:
    print "please provide the prefix, language order, and the target language"
    exit(-1)

print "## cut, prefix: " + prefix + ", order: " + order + ", targetLanguage: " + targetLanguage

filePath = "build/" + prefix + "-" + targetLanguage + ".vtt" 
file = open(filePath) 
lines = file.read().splitlines()

paragraphs = []

count = 0
paragraph = ""
for line in lines:
    if "-->" in line:
        if len(paragraph) > 0 and count > 0:
            paragraph = paragraph[:len(paragraph)-2]
            paragraphs.append(paragraph)
        paragraph = ""
        count = count + 1
    else:
        paragraph = paragraph + line + "\n"
paragraphs.append(paragraph)

count = 0
prevStartTime = "00:00"
prevTotalSeconds = 0
threshold = 8
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
        if count > 0:
            paragraph = paragraphs[count - 1]
            threshold = len(paragraph) / 5
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
        startTime = str(minutes) + ":" + str(seconds)
        duration = totalSeconds - prevTotalSeconds
        if duration > threshold * 3:
            duration = threshold * 3
        plusDuration = prevTotalSeconds + duration
        minutes = plusDuration / 60 
        seconds = plusDuration - minutes * 60
        plusDurationStartTime = str(minutes) + ":" + str(seconds)
        #if duration > threshold:
        #    print "paragraph: " + paragraph
        #    print "threshold: " + str(threshold)
        #    print "duration: " + str(duration)
        if count > 0 and duration > threshold:
            filePrefix = "build/" + prefix + "/" + prefix + "-" + format(count, '03d')
            targetFile = filePrefix + "-" + order + "o" + targetLanguage
            if not path.exists(targetFile + ".mp4") and not path.exists(filePrefix + "-" + targetLanguage + ".jpg"):
                #subprocess.call(["ffmpeg", "-y", "-i", "build/" + prefix + "-o" + targetLanguage + ".m4a", "-acodec", "copy", "-ss", prevStartTime, "-to", plusDurationStartTime, targetFile + "~.m4a"])
                #subprocess.call(["ffmpeg", "-y", "-i", targetFile + "~.m4a", "-filter:a", "volume=4.5", targetFile + "~~.m4a"])
                #subprocess.call(["mv", targetFile + "~~.m4a", targetFile + ".m4a"])
                #subprocess.call(["rm", targetFile + "~.m4a"])
                
                subprocess.call(["ffmpeg", "-y", "-i", "build/" + prefix + "-o" + targetLanguage + ".mp4", "-acodec", "copy", "-ss", prevStartTime, "-to", plusDurationStartTime, targetFile + "~.mp4"])
                subprocess.call(["ffmpeg", "-y", "-i", targetFile + "~.mp4", "-filter:a", "volume=4.5", targetFile + "~~.mp4"])
                subprocess.call(["mv", targetFile + "~~.mp4", targetFile + ".mp4"])
                subprocess.call(["rm", targetFile + "~.mp4"])
        prevTotalSeconds = totalSeconds
        prevStartTime = startTime
        count = count + 1
        #if count > 20:
        #    break

if targetLanguage != "tr":
    filePrefix = "build/" + prefix + "/" + prefix + "-" + format(count, '03d')
    targetFile = filePrefix + "-" + order + "o" + targetLanguage
    if not path.exists(targetFile + ".mp4") and not path.exists(filePrefix + "-" + targetLanguage + ".jpg"):
        #subprocess.call(["ffmpeg", "-y", "-i", "build/" + prefix + "-o" + targetLanguage + ".m4a", "-acodec", "copy", "-ss", prevStartTime, "-t", "10", targetFile + "~.m4a"])
        #subprocess.call(["ffmpeg", "-y", "-i", targetFile + "~.m4a", "-filter:a", "volume=4.5", targetFile + "~~.m4a"])
        #subprocess.call(["mv", targetFile + "~~.m4a", targetFile + ".m4a"])
        #subprocess.call(["rm", targetFile + "~.m4a"])

        subprocess.call(["ffmpeg", "-y", "-i", "build/" + prefix + "-o" + targetLanguage + ".mp4", "-acodec", "copy", "-ss", prevStartTime, "-t", "10", targetFile + "~.mp4"])
        subprocess.call(["ffmpeg", "-y", "-i", targetFile + "~.mp4", "-filter:a", "volume=4.5", targetFile + "~~.mp4"])
        subprocess.call(["mv", targetFile + "~~.mp4", targetFile + ".mp4"])
        subprocess.call(["rm", targetFile + "~.mp4"])

file.close()
