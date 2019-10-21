# importing the requests library
import os, sys, subprocess, os.path
from os import path

if len(sys.argv) > 1:
    prefix = sys.argv[1]
    #sourceLanguage = sys.argv[2]
    #targetLanguage = sys.argv[3]
else:
    print "please provide the prefix"
    exit(-1)
filePath = "data/" + prefix+ "/" + prefix
files = os.listdir("data/" + prefix)
files.sort()
target = ""
subprocessArray = ["ffmpeg", "-y"]
count = 0
fileCount = 0
concatString = ""
for file in files:
    subprocessArray.extend(["-i", "data/" + prefix + "/" + file])
    #subprocessArray.extend(["-i", "silence1.m4a"])
    concatString = concatString + "[" + str(fileCount) + ":a]"
    fileCount = fileCount + 1
    #concatString = concatString + "[" + str(fileCount) + ":a]"
    #fileCount = fileCount + 1
    count = count + 1
    if count % 100 == 0:
        targetFile = "data/" + prefix + "-" + format(count / 100, "02d") + ".mp4"
        if not path.exists(targetFile):
            subprocessArray.extend(["-filter_complex", concatString + "concat=n=" + str(fileCount) + ":v=0:a=1", targetFile])
            subprocess.call(subprocessArray)
            fileCount = 0
            concatString = ""
            subprocessArray = ["ffmpeg", "-y"]

if count % 100 > 1:
    n = count / 100 + 1
    targetFile = "data/" + prefix + "-" + format(n, '02d') + ".mp4"
    if not path.exists(targetFile):
        subprocessArray.extend(["-filter_complex", concatString + "concat=n=" + str(fileCount) + ":v=0:a=1", targetFile])
        subprocess.call(subprocessArray)
concatString = ""
subprocessArray = ["ffmpeg", "-y"]
targetFile = "data/" + prefix + ".mp4"
if not path.exists(targetFile):
    for i in range(0, n):
        subprocessArray.extend(["-i", "data/" + prefix + "-" + format(i+1, '02d') + ".mp4"])
        concatString = concatString + "[" + str(i) + ":a]"
    subprocessArray.extend(["-filter_complex", concatString + "concat=n=" + str(n) + ":v=0:a=1", targetFile])
    subprocess.call(subprocessArray)

