# importing the requests library
import os, sys, subprocess, os.path
from os import path

if len(sys.argv) > 2:
    prefix = sys.argv[1]
    postfix = sys.argv[2]
else:
    print "please provide prefix and postfix"
    exit(-1)

print "## combin, prefix: " + prefix
filePath = "build/" + prefix+ "/" + prefix
files = os.listdir("build/" + prefix)
files = list(filter(lambda file: file[0] != ".", files))
files = list(filter(lambda file: "-" + postfix in file, files))
files.sort()
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
    if count % 100 == 0:
        targetFile = "build/" + prefix + "-" + format(count / 100, "02d") + ".mp4"
        if not path.exists(targetFile):
            subprocessArray.extend(["-filter_complex", concatString + "concat=n=" + str(fileCount) + ":v=1:a=1", targetFile])
            subprocess.call(subprocessArray)
        fileCount = 0
        concatString = ""
        subprocessArray = ["ffmpeg", "-y"]

if count % 100 > 1:
    n = count / 100 + 1
    targetFile = "build/" + prefix + "-" + format(n, '02d') + ".mp4"
    #print "targetFile: " + targetFile
    if not path.exists(targetFile):
        subprocessArray.extend(["-filter_complex", concatString + "concat=n=" + str(fileCount) + ":v=1:a=1", targetFile])
        print "subprocessArray: " + str(subprocessArray)
        subprocess.call(subprocessArray)
concatString = ""
subprocessArray = ["ffmpeg", "-y"]
targetFile = "build/" + prefix + "-" + postfix + ".mp4"
if not path.exists(targetFile):
    for i in range(0, n):
        subprocessArray.extend(["-i", "build/" + prefix + "-" + format(i+1, '02d') + ".mp4"])
        concatString = concatString + "[" + str(i) + ":v][" + str(i) + ":a]"
    subprocessArray.extend(["-filter_complex", concatString + "concat=n=" + str(n) + ":v=1:a=1", targetFile])
    subprocess.call(subprocessArray)

