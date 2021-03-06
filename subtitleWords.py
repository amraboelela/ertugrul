
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

dictionaryFilePath = "build/dictionary-" + targetLanguage + ".txt"
dictionaryFile = open(dictionaryFilePath)
dictionaryLines = dictionaryFile.read().splitlines()
dictionary = {}
for dictionaryLine in dictionaryLines:
    lineSplit = dictionaryLine.split(":")
    word = lineSplit[0].strip()
    if len(lineSplit) > 1:
        meaning = lineSplit[1].strip()
        #print("word: " + word)
        dictionary[word] = meaning
    else:
        print("word without meaning: " + word)

targetFilePath = "build/" + prefix + "-" + targetLanguage + ".vtt"
subtitlesPath = "build/" + prefix + "-w.srt"

targetFile = open(targetFilePath)
targetLines = targetFile.read().splitlines()

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
def writeToSubtitlesFile(cutCode, paragraph):
    global startTimeFloat
    global includeCount
    includeCount = includeCount + 1
    subtitlesFile.write(str(includeCount) + "\n")
    startTimeString = timeString(startTimeFloat)
    print("cutCode: " + cutCode)
    print("episodeDurationsDictionary: " + str(episodeDurationsDictionary))
    duration = float(episodeDurationsDictionary[cutCode])
    startTimeFloat = startTimeFloat + duration
    endTimeString = timeString(startTimeFloat - 0.1)
    subtitlesFile.write(startTimeString + " --> " + endTimeString + "\n")
    lines = paragraph.split("\n")
    for line in lines:
        subtitlesFile.write("<font color=\"white\">")
        words = line.split()
        for word in words:
            if word[-1] == "," or word[-1] == "." or word[-1] == "!" or word[-1] == "?":
                subtitlesFile.write(word[:len(word)-1])
            else:
                subtitlesFile.write(word)
            cleanWord = word.lower().replace(":","").replace(",","").replace(";","").replace("?", "").replace("!", "").replace(".", "").replace("[", "").replace("]", "").replace("-", "").replace("[","").replace("]","").replace("<i>","").replace("</i>","").replace('"', '').replace("'", "")
            try:
                meaning = dictionary[cleanWord]
                #print("word: " + word + ", meaning: " + meaning)
                if len(meaning.strip()) > 0 and meaning != cleanWord:
                    subtitlesFile.write(" <font color=\"yellow\">(" + meaning + ")</font>")
                    if word[-1] == "," or word[-1] == "." or word[-1] == "!" or word[-1] == "?":
                        subtitlesFile.write(word[-1])
            except Exception as error:
                print("error: " + str(error))
            subtitlesFile.write(" ")
        subtitlesFile.write("</font>\n")

    subtitlesFile.write("\n")
 
if not path.exists(subtitlesPath) or os.stat(subtitlesPath).st_size == 0:
    print("not path.exists(subtitlesPath)")
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
    
    filePath = "build/" + prefix + "-" + targetLanguage + ".vtt"
    file = open(filePath)
    lines = file.read().splitlines()
    prevStartTime = "00:00"
    prevTimeStamp = 0
    count = 0

    paragraph = ""
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
            duration = timeStamp - prevTimeStamp
            prevTimeStamp = timeStamp
            if len(paragraph) > 0  and count > 0:
                if duration > durationLowerLimit and duration < durationUpperLimit:
                    paragraph = paragraph[:len(paragraph)-2]
                    writeToSubtitlesFile(str(count).zfill(3), paragraph)
            paragraph = ""
            count = count + 1
        else:
            paragraph = paragraph + line + "\n"
    subtitlesFile.close()
#quit()
targetFile.close()
sbtFile = "build/" + prefix + "-sbw-" + postfix + ".mp4"
if not path.exists(sbtFile):
    os.system("handbrakecli -i build/" + prefix + "-" + postfix +".mp4 -o " + sbtFile + " --srt-file build/" + prefix + "-w.srt --srt-codeset UTF-8 --srt-burn")
