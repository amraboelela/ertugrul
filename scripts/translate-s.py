# importing the requests library
import sys, subprocess

if len(sys.argv) > 3:
    prefix = sys.argv[1]
    sourceLanguage = sys.argv[2]
    targetLanguage = sys.argv[3]
else:
    print "please provide the prefix, source language, and the target language"
    exit(-1)

sourceFileName = "build/" + prefix + "-" + sourceLanguage + ".vtt"
sourceFile = open(sourceFileName)
sourceLines = sourceFile.read().splitlines()
paragraph = ""
sourceParagraphs = []
for line in sourceLines:
    if "-->" in line:
        if len(paragraph) > 0:
            paragraph = paragraph[:len(paragraph)-2]
            sourceParagraphs.append(paragraph)
        paragraph = ""
    else:
        paragraph = paragraph + line.replace('-','').replace("!","").replace(".","") + ". "

targetFileName = "build/" + prefix + "-" + targetLanguage + "-p.vtt"
targetFile = open(targetFileName)
targetLines = targetFile.read().splitlines()
paragraph = ""
targetParagraphs = []
for line in targetLines:
    if "-->" in line:
        if len(paragraph) > 0:
            paragraph = paragraph[:len(paragraph)-2]
            targetParagraphs.append(paragraph)
        paragraph = ""
    else:
        paragraph = paragraph + line.replace('-','').replace("!","").replace(".","") + ". "

count = 0
for paragraph in sourceParagraphs:
    print paragraph
    print 
    print targetParagraphs[count]
    print
    print
    count = count + 1
    if count > 10:
        break
 
sourceFile.close()
targetFile.close()

