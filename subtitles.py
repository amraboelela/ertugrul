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
#sourceFilePath = "data/" + prefix + "-" + sourceLanguage + ".vtt"
targetFilePath = "data/" + prefix + "-" + targetLanguage + ".vtt"
subtitlesPath = "data/" + prefix + ".srt"

sourceFile = open(sourceFilePath)
targetFile = open(targetFilePath)
subtitlesFile = open(subtitlesPath, "w")
sourceLines = sourceFile.read().splitlines()
targetLines = targetFile.read().splitlines()

def writeToSubtitlesFile(count, paragraph):
    subtitlesFile.write(str(count) + "\n")
    subtitlesFile.write("<start time> --> <end time>\n")
    subtitlesFile.write(paragraph)
    #subtitlesFile.write("\n")
 
sourceParagraphs = []
targetParagraphs = []

def getParagraphs(lines, paragraghs):
    count = 0
    paragraph = ""
    for line in lines:
        if "-->" in line:
            if len(paragraph) > 0 and count > 0:
                paragraghs.append(paragraph)
            paragraph = ""
            count = count + 1
        else:
            paragraph = paragraph + line + "\n"
    paragraghs.append(paragraph)

getParagraphs(sourceLines, sourceParagraphs)
getParagraphs(targetLines, targetParagraphs)

#print len(sourceParagraphs)
#print len(targetParagraphs)

count = 0
for i in range(0, len(sourceParagraphs)):
    count = count + 1
    writeToSubtitlesFile(count, sourceParagraphs[i])
    count = count + 1
    writeToSubtitlesFile(count, targetParagraphs[i])

sourceFile.close()
targetFile.close()
subtitlesFile.close()

