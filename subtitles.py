# importing the requests library
import sys, subprocess, os.path
from os import path

if len(sys.argv) > 3:
    prefix = sys.argv[1]
    sourceLanguage = sys.argv[2]
    targetLanguage = sys.argv[3]
else:
    print "please provide the prefix, source language and the target language"
    exit(-1)

sourceFilePath = "data/" + prefix + "-" + targetLanguage + "-" + sourceLanguage + ".vtt"
targetFilePath = "data/" + prefix + "-" + targetLanguage + ".vtt"
subtitlesPath = "data/" + prefix + ".srt"

sourceFile = open(sourceFilePath)
targetFile = open(targetFilePath)
subtitlesFile = open(subtitlesPath, "w")
sourceLines = sourceFile.read().splitlines()
targetLines = targetFile.read().splitlines()

sourceParagraphs = []
targetParagraphs = []

def getParagraphs(lines, paragraghs):
    count = 0
    paragraph = ""
    for line in lines:
        if "-->" in line:
            if len(paragraph) > 0 and count > 0:
                paragraph = "<font color=\"white\">" + paragraph[:len(paragraph)-2] + "</font>\n\n"
                paragraghs.append(paragraph)
            paragraph = ""
            count = count + 1
        else:
            paragraph = paragraph + line + "\n"
    paragraghs.append(paragraph)

getParagraphs(sourceLines, sourceParagraphs)
getParagraphs(targetLines, targetParagraphs)

files = os.listdir("data/" + prefix)
files.sort()
durationsFilePath = "data/durations.txt"
os.system("rm -f " + durationsFilePath)
for file in files:
    if not "~" in file:
        videoFile = "data/" + prefix + "/" + file
        os.system("ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 " + videoFile + " >> " + durationsFilePath)

durationsFile = open(durationsFilePath)
durations = durationsFile.read().splitlines()
startTimeFloat = float(0.0)
durationIndex = 0

def timeString(timeFloat):
    milliSeconds = int(timeFloat * 1000 % 1000)
    totalSeconds = int(timeFloat)
    seconds = totalSeconds % 60
    totalMinutes = totalSeconds / 60
    minutes = totalMinutes % 60
    hours = totalMinutes / 60
    return format(hours, '02d') + ":" + format(minutes, '02d') + ":" + format(seconds, '02d') + "," + format(milliSeconds, '03d')

def writeToSubtitlesFile(paragraph):
    global startTimeFloat
    global durationIndex
    subtitlesFile.write(str(durationIndex) + "\n")
    startTimeString = timeString(startTimeFloat)
    if durationIndex < len(durations):
        duration = float(durations[durationIndex])
        startTimeFloat = startTimeFloat + duration
        endTimeString = timeString(startTimeFloat)
    else:
        endTimeString = "Not Yet"
    subtitlesFile.write(startTimeString + " --> " + endTimeString + "\n")
    subtitlesFile.write(paragraph)
    durationIndex = durationIndex + 1

for i in range(0, len(sourceParagraphs)):
    writeToSubtitlesFile(sourceParagraphs[i])
    writeToSubtitlesFile(targetParagraphs[i])

sourceFile.close()
targetFile.close()
subtitlesFile.close()

os.system("mv data/" + prefix + ".mp4 data/" + prefix + "~.mp4")
os.system("ffmpeg -i data/" + prefix + "~.mp4 -i " + subtitlesPath + " -c copy -c:s mov_text data/" + prefix + ".mp4")
os.system("rm data/" + prefix + "~.mp4")

