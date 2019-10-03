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
reverse = False
if sourceLanguage < targetLanguage:
    reverse = False
else:
    reverse = True
files.sort()
target = ""
for file in files:
    if reverse:
        if "-" + targetLanguage in file:
            target = "file '" + directory + "/" + file + "'\n"
        if "-" + sourceLanguage in file:
            outputFile.write("file '" + directory + "/" + file + "'\n")
            outputFile.write("file 'silence1.m4a'\n")
            outputFile.write(target)
            outputFile.write("file 'silence1.m4a'\n")
            outputFile.write("file 'silence1.m4a'\n")
    else:
        if "-" + sourceLanguage in file or "-" + targetLanguage in file:
            outputFile.write("file '" + directory + "/" + file + "'\n")
            #outputFile.write("file 'silence1.m4a'\n")
        #if targetLanguage in file:
        #    outputFile.write("file 'silence1.m4a'\n")

outputFile.close()
subprocess.call(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "audioFiles.txt", "-c", "copy", directory + "/" + directory + ".m4a"])

