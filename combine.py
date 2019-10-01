# importing the requests library
import os, sys, subprocess

if len(sys.argv) > 3:
    directory = sys.argv[1]
    sourceLanguage = sys.argv[2]
    targetLanguage = sys.argv[3]
else:
    print "please provide the directory, source language, and target language"
    exit(-1)

outputFile = open("audioFiles.txt", "w")
files = os.listdir(directory)

if sourceLanguage < targetLanguage:
    files.sort()
else:
    file.sort(reverse = True)
for file in files:
    if "-" + sourceLanguage in file or "-" + targetLanguage in file:
        outputFile.write("file '" + directory + "/" + file + "'\n")
        outputFile.write("file 'silence1.m4a'\n")
    if targetLanguage in file:
        outputFile.write("file 'silence1.m4a'\n")

outputFile.close()
subprocess.call(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "audioFiles.txt", "-c", "copy", directory + ".m4a"])

