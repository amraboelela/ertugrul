# importing the requests library
import os, sys, subprocess

if len(sys.argv) > 1:
    directory = sys.argv[1]
else:
    print "please provide the directory"
    exit(-1)

outputFile = open(directory + ".txt", "w")
files = os.listdir(directory)
files.sort()
for file in files:
    if ".DS_Store" in file:
        x = 1
    else:
        outputFile.write("file '" + directory + "/" + file + "'\n")

outputFile.close()
subprocess.call(["ffmpeg", "-f", "concat", "-fase", "0", "-i", directory + ".txt", "-c", "copy", "output"])

