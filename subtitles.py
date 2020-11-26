# -*- coding: utf-8 -*-

import sys, subprocess, os.path
from os import path

if len(sys.argv) > 3:
    prefix = sys.argv[1]
    targetLanguage = sys.argv[2]
    postfix = sys.argv[3]
else:
    print("please provide the prefix, target language, and prefix")
    exit(-1)

#print "## subtitles, prefix: " + prefix + sourceLanguage + ", targetLanguage: " + targetLanguage

dictionaryFilePath = "build/dictionary-" + targetLanguage + ".txt"
dictionaryFile = open(dictionaryFilePath)
dictionaryLines = dictionaryFile.read().splitlines()
dictionary = {}
for dictionaryLine in dictionaryLines:
    lineSplit = dictionaryLine.split(":")
    word = lineSplit[0].strip()
    meaning = lineSplit[1].strip()
    #print("word: " + word)
    dictionary[str(word)] = meaning

#if targetLanguage == "tr":
#    sourceFilePath = "build/" + prefix + "-" + targetLanguage + "-" + sourceLanguage + ".vtt"
#else:
#    sourceFilePath = "build/" + prefix + "-" + sourceLanguage + ".vtt"

targetFilePath = "build/" + prefix + "-" + targetLanguage + ".vtt"
subtitlesPath = "build/" + prefix + ".srt"

targetFile = open(targetFilePath)
subtitlesFile = open(subtitlesPath, "w")
targetLines = targetFile.read().splitlines()

targetParagraphs = []

def getParagraphs(lines, paragraghs):
    count = 0
    paragraph = ""
    for line in lines:
        if "-->" in line:
            if len(paragraph) > 0 and count > 0:
                paragraph = paragraph[:len(paragraph)-2]
                paragraghs.append(paragraph)
            paragraph = ""
            count = count + 1
        else:
            paragraph = paragraph + line + "\n"
    paragraghs.append(paragraph)

def timeString(timeFloat):
    milliSeconds = int(timeFloat * 1000 % 1000)
    totalSeconds = int(timeFloat)
    seconds = totalSeconds % 60
    totalMinutes = totalSeconds / 60
    minutes = totalMinutes % 60
    hours = totalMinutes / 60
    return format(hours, '02f') + ":" + format(minutes, '02f') + ":" + format(seconds, '02f') + "," + format(milliSeconds, '03f')

def writeToSubtitlesFile(paragraph1, color1, paragraph2, color2):
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
    subtitlesFile.write("<font color=\"" + color1 + "\">" + paragraph1 + "</font>\n")
    if len(paragraph2) > 0:
        subtitlesFile.write("<font color=\"" + color2 + "\">" + paragraph2 + "</font>\n\n")
    else:
        subtitlesFile.write("\n")
    durationIndex = durationIndex + 1
   
def writeToSubtitlesFile2(paragraph):
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
    subtitlesFile.write("<font color=\"white\">")
    words = paragraph.split()
    for word in words:
        subtitlesFile.write(word + " ")
        meaning = dictionary[str(word.replace("-", ""))]
        subtitlesFile.write("<font color=\"yellow\">" + meaning + "</font> ")
    subtitlesFile.write("</font>\n")

    subtitlesFile.write("\n")
    durationIndex = durationIndex + 1
 
if not path.exists(subtitlesPath) or os.stat(subtitlesPath).st_size == 0:
    getParagraphs(targetLines, targetParagraphs)

    #files = os.listdir("build/" + prefix)
    #files.sort()
    durationsFilePath = "build/durations.txt"
    #os.system("rm -f " + durationsFilePath)
    #for file in files:
    #    if not "~" in file:
    #        videoFile = "build/" + prefix + "/" + file
    #        os.system("ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 " + videoFile + " >> " + durationsFilePath)

    durationsFile = open(durationsFilePath)
    durations = durationsFile.read().splitlines()
    startTimeFloat = float(0.0)
    durationIndex = 0
    
    for i in range(0, len(targetParagraphs)):
        videoFile = "build/" + prefix + "/" + prefix + "-" + format(i+1, '03f') + "-" + targetLanguage + "-" + postfix + ".mp4"
        #print "videoFile: " + videoFile
        if path.exists(videoFile):
            writeToSubtitlesFile2(targetParagraphs[i])

targetFile.close()
subtitlesFile.close()

sbtFile = "build/" + prefix + "-sbt-" + postfix + ".mp4"
if not path.exists(sbtFile):
    os.system("handbrakecli -i build/" + prefix + ".mp4 -o " + sbtFile + " --srt-file build/" + prefix + ".srt --srt-codeset UTF-8 --srt-burn")
