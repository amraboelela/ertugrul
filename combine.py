# importing the requests library
import os, sys, subprocess

if len(sys.argv) > 1:
    directory = sys.argv[1]
else:
    print "please provide the directory"
    exit(-1)

outputFile = open("audioFiles.txt", "w")
files = os.listdir(directory)
files.sort()
for file in files:
    if ".DS_Store" in file:
        x = 1
    else:
        outputFile.write("file '" + directory + "/" + file + "'\n")
        outputFile.write("file 'silence1.m4a'\n")
        if "-en" not in file:
            outputFile.write("file 'silence1.m4a'\n")

outputFile.close()
subprocess.call(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "audioFiles.txt", "-c", "copy", directory + ".m4a"])

