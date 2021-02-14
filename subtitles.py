
import sys, subprocess, os.path
from os import path
import durationLimit

if len(sys.argv) > 3:
    prefix = sys.argv[1]
    targetLanguage = sys.argv[2]
    postfix = sys.argv[3]
else:
    print("please provide the prefix, target language, and prefix")
    exit(-1)

print("## subtitles, prefix: " + prefix + ", targetLanguage: " + targetLanguage + ", postfix: " + postfix)

durationLowerLimit = durationLimit.lowerLimit(prefix, targetLanguage)
durationUpperLimit = durationLimit.upperLimit(targetLanguage)

englishFilePath = "build/" + prefix + "-en.vtt"
targetFilePath = "build/" + prefix + "-" + targetLanguage + ".vtt"
subtitlesPath = "build/" + prefix + ".srt"

englishFile = open(englishFilePath)
englishLines = englishFile.read().splitlines()
targetFile = open(targetFilePath)
targetLines = targetFile.read().splitlines()
targetFile.close()
englishFile.close()

def timeString(timeFloat):
    milliSeconds = int(timeFloat * 1000 % 1000)
    totalSeconds = int(timeFloat)
    seconds = int(totalSeconds % 60)
    totalMinutes = int(totalSeconds / 60)
    minutes = int(totalMinutes % 60)
    hours = int(totalMinutes / 60)
    return str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2) + "," + str(milliSeconds).zfill(3)

includeCount = 0
episodeDurationsDictionary = {}
def writeToSubtitlesFile(cutCode, paragraph, englishParagraph):
    global startTimeFloat
    global includeCount
    includeCount = includeCount + 1
    subtitlesFile.write(str(includeCount) + "\n")
    startTimeString = timeString(startTimeFloat)
    #print("cutCode: " + cutCode)
    duration = float(episodeDurationsDictionary[cutCode])
    startTimeFloat = startTimeFloat + duration
    endTimeString = timeString(startTimeFloat - 0.1)
    subtitlesFile.write(startTimeString + " --> " + endTimeString + "\n")
    lines = paragraph.split("\n")
    for line in lines:
        subtitlesFile.write("<font color=\"white\">" + line +"</font>\n")
    englishLines = englishParagraph.split("\n")
    for englishLine in englishLines:
        subtitlesFile.write("<font color=\"yellow\">" + englishLine +"</font>\n")
    subtitlesFile.write("\n")
 
if not path.exists(subtitlesPath) or os.stat(subtitlesPath).st_size == 0:
    #print("not path.exists(subtitlesPath)")
    subtitlesFile = open(subtitlesPath, "w")
    files = os.listdir("build/" + prefix)
    files = list(filter(lambda file: file[0] != ".", files))
    files = list(filter(lambda file: "-" + postfix + "." in file, files))
    files.sort()
    durationsFilePath = "build/durations.txt"
    os.system("rm -f " + durationsFilePath)
    for file in files:
        if not "~" in file:
            videoFile = "build/" + prefix + "/" + file
            os.system("ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 " + videoFile + " >> " + durationsFilePath)

    durationsFile = open(durationsFilePath)
    durations = durationsFile.read().splitlines()
    fileCount = 0
    for file in files:
        if not "~" in file:
            fileParts = file.split("-")
            cutCode = fileParts[3]
            episodeDurationsDictionary[cutCode] = durations[fileCount]
            fileCount = fileCount + 1
    
    startTimeFloat = float(0.0)
    prevStartTime = "00:00"
    prevTimeStamp = 0
    count = 0
    paragraph = ""
    targetParagraphs = []
    targetTimeStamps = []
    targetDurations = []
    cutCodes = []
    for line in targetLines:
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
            if len(paragraph) > 0  and count > 0:
                if duration > durationLowerLimit and duration < durationUpperLimit:
                    paragraph = paragraph[:len(paragraph)-2]
                    cutCodes.append(str(count).zfill(3))
                    #writeToSubtitlesFile(str(count).zfill(3), paragraph)
                    targetTimeStamps.append(timeStamp)
                    targetDurations.append(duration)
                    targetParagraphs.append(paragraph)
            paragraph = ""
            count = count + 1
        else:
            paragraph = paragraph + line + "\n"
            
    #print(targetParagraphs)
    
    startTimeFloat = float(0.0)
    prevStartTime = "00:00"
    prevTimeStamp = 0
    count = 0
    paragraph = ""
    englishParagraphs = []
    englishTimeStamps = []
    for line in englishLines:
        #print("line " + line)
        if "-->" in line:
            times = line.split(" --> ")
            startTime = times[0]
            #if targetLanguage == "tr":
            #    startTime = "00:" + startTime
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
            if len(paragraph) > 0  and count > 0:
                paragraph = paragraph[:len(paragraph)-2]
                #writeToSubtitlesFile(str(count).zfill(3), paragraph)
                englishTimeStamps.append(timeStamp)
                englishParagraphs.append(paragraph)
            paragraph = ""
            count = count + 1
        else:
            paragraph = paragraph + line + "\n"
            
    #print(englishParagraphs)
    count = 0
    englishCount = 0
    timeDiff = 0.7
    for paragraph in targetParagraphs:
        targetTimeStamp = targetTimeStamps[count] + timeDiff
        targetDuration = targetDurations[count]
        #print(str(int(targetTimeStamp)) + ": " + paragraph) #" (" + str(int(targetDuration)) + "): "
        if count < len(targetTimeStamps):
            englishTimeStamp = englishTimeStamps[englishCount]
            bestEnglishTimeStamp = englishTimeStamp
            englishTimeDiff = abs(englishTimeStamp - targetTimeStamp)
            englishParagraph = englishParagraphs[englishCount]
            while englishTimeStamp < targetTimeStamp + targetDuration / 2:
                if abs(englishTimeStamp - targetTimeStamp) < englishTimeDiff:
                    englishTimeDiff = abs(englishTimeStamp - targetTimeStamp)
                    englishParagraph = englishParagraphs[englishCount]
                    bestEnglishTimeStamp = englishTimeStamp
                englishCount = englishCount + 1
                if englishCount < len(englishTimeStamps):
                    englishTimeStamp = englishTimeStamps[englishCount]
                else:
                    break
            writeToSubtitlesFile(cutCodes[count], paragraph, englishParagraph)
        count = count + 1
    subtitlesFile.close()

#quit()
sbtFile = "build/" + prefix + "-sbt-" + postfix + ".mp4"
if not path.exists(sbtFile):
    os.system("handbrakecli -i build/" + prefix + "-" + postfix +".mp4 -o " + sbtFile + " --srt-file build/" + prefix + ".srt --srt-codeset UTF-8 --srt-burn")
