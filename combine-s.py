# importing the requests library
import os, sys, subprocess, os.path
from os import path

if len(sys.argv) > 1:
    prefix = sys.argv[1]
else:
    print "please provide the prefix"
    exit(-1)

print "## combin, prefix: " + prefix
filePath = "build/" + prefix+ "/" + prefix
files = os.listdir("build/" + prefix)
files.sort()
files = list(filter(lambda file: file[0] != ".", files))
target = ""
subprocessArray = ["ffmpeg", "-y"]
count = 0
fileCount = 0
concatString = ""
for file in files:
    subprocessArray.extend(["-i", "build/" + prefix + "/" + file])
    concatString = concatString + "[" + str(fileCount) + ":v][" + str(fileCount) + ":a]"
    fileCount = fileCount + 1
    count = count + 1
    #if count > 15:
    #    break

targetFile = "build/" + prefix + ".mp4"
if not path.exists(targetFile):
    subprocessArray.extend(["-filter_complex", concatString + "concat=n=" + str(fileCount) + ":v=1:a=1", targetFile])
    print "subprocessArray: " + str(subprocessArray)
    subprocess.call(subprocessArray)

