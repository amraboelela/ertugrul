
import sys, subprocess, os.path
from os import path

if len(sys.argv) > 3:
    prefix = sys.argv[1]
    targetLanguage = sys.argv[2]
    postfix = sys.argv[3]
else:
    print("please provide the prefix, target language, and prefix")
    exit(-1)

print("## subtitles, prefix: " + prefix + ", targetLanguage: " + targetLanguage + ", postfix: " + postfix)

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
    seconds = int(totalSeconds % 60)
    totalMinutes = int(totalSeconds / 60)
    minutes = int(totalMinutes % 60)
    hours = int(totalMinutes / 60)
    return str(hours).zfill(2) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2) + "," + str(milliSeconds).zfill(3)
   
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
    lines = paragraph.split("\n")
    for line in lines:
        subtitlesFile.write("<font color=\"white\">")
        words = line.split()
        for word in words:
            cleanWord = word.replace(":","").replace(",","").replace("?", "").replace("!", "").replace(".", "").replace("[", "").replace("]", "").replace("-", "").replace("[","").replace("]","").replace("<i>","").replace("</i>","").replace('"', '').replace("'", "")
            subtitlesFile.write(cleanWord)
            cleanWord = cleanWord.lower()
            try:
                meaning = dictionary[cleanWord]
                #print("word: " + word + ", meaning: " + meaning)
                if len(meaning.strip()) > 0 and meaning != word:
                    subtitlesFile.write(": <font color=\"yellow\">" + meaning + "</font>")
                    if word[-1] == "," or word[-1] == "." or word[-1] == "!" or word[-1] == "?":
                        subtitlesFile.write(word[-1])
                    subtitlesFile.write(" ")
            except Exception as error:
                print("error: " + str(error))
        subtitlesFile.write("</font>\n")

    subtitlesFile.write("\n")
    durationIndex = durationIndex + 1
 
if not path.exists(subtitlesPath) or os.stat(subtitlesPath).st_size == 0:
    getParagraphs(targetLines, targetParagraphs)

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
    startTimeFloat = float(0.0)
    durationIndex = 0
    
    for i in range(0, len(targetParagraphs)):
        videoFile = "build/" + prefix + "/" + prefix + "-" + str(i+1).zfill(3) + "-" + targetLanguage + "-" + postfix + ".mp4"
        #print "videoFile: " + videoFile
        if path.exists(videoFile):
            writeToSubtitlesFile(targetParagraphs[i])

targetFile.close()
subtitlesFile.close()

sbtFile = "build/" + prefix + "-sbt-" + postfix + ".mp4"
if not path.exists(sbtFile):
    os.system("handbrakecli -i build/" + prefix + "-" + postfix +".mp4 -o " + sbtFile + " --srt-file build/" + prefix + ".srt --srt-codeset UTF-8 --srt-burn")
