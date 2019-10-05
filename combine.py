# importing the requests library
import os, sys, subprocess

if len(sys.argv) > 3:
    prefix = sys.argv[1]
    sourceLanguage = sys.argv[2]
    targetLanguage = sys.argv[3]
else:
    print "please provide the prefix, source language, and target language"
    exit(-1)
filePath = "data/" + prefix+ "/" + prefix
outputFile = open("audioFiles.txt", "w")
files = os.listdir("data/" + prefix)
reverse = False
if sourceLanguage < targetLanguage:
    reverse = False
else:
    reverse = True
files.sort()
target = ""
subprocessArray = ["ffmpeg", "-y"]
count = 0
fileCount = 0
concatString = ""
for file in files:
    if reverse:
        if "-" + targetLanguage in file:
            target = "file '" + "data/" + prefix + "/" + file + "'\n"
        if "-" + sourceLanguage in file:
            outputFile.write("file '" + "data/" + prefix + "/" + file + "'\n")
            outputFile.write("file 'silence1.m4a'\n")
            outputFile.write(target)
            outputFile.write("file 'silence1.m4a'\n")
            outputFile.write("file 'silence1.m4a'\n")
    else:
        if targetLanguage == "otr":
            #if "-" + sourceLanguage in file or "-" + targetLanguage in file:
            subprocessArray.extend(["-i", "data/" + prefix + "/" + file])
            subprocessArray.extend(["-i", "silence1.m4a"])
            concatString = concatString + "[" + str(fileCount) + ":a]"
            fileCount = fileCount + 1
            concatString = concatString + "[" + str(fileCount) + ":a]"
            fileCount = fileCount + 1
            #if targetLanguage in file:
            count = count + 1
            if count % 100 == 0:
                if count / 100 > 0:
                    subprocessArray.extend(["-filter_complex", concatString + "concat=n=" + str(fileCount) + ":v=0:a=1", "data/" + prefix + "-" + format(count / 100, "02d") + ".m4a"])
                    print "subprocessArray: " + str(subprocessArray)
                    subprocess.call(subprocessArray)
                    fileCount = 0
                    concatString = ""
                    #exit(0)
                subprocessArray = ["ffmpeg", "-y"]
        else:
            if "-" + sourceLanguage in file or "-" + targetLanguage in file:
                outputFile.write("file '" + "data/" + prefix + "/" + file + "'\n")
                outputFile.write("file 'silence1.m4a'\n")
            if targetLanguage in file:
                outputFile.write("file 'silence1.m4a'\n")
outputFile.close()
#exit(0)
if targetLanguage == "otr":
    if count % 100 > 1:
        n = count / 100 + 1
        subprocessArray.extend(["-filter_complex", concatString + "concat=n=" + str(fileCount) + ":v=0:a=1", "data/" + prefix + "-" + format(n, '02d') + ".m4a"])
        print "subprocessArray: " + str(subprocessArray)
        subprocess.call(subprocessArray)
    #exit(0)
    concatString = ""
    subprocessArray = ["ffmpeg", "-y"]
    for i in range(0, n):
        subprocessArray.extend(["-i", "data/" + prefix + "-" + format(i+1, '02d') + ".m4a"])
        concatString = concatString + "[" + str(i) + ":a]"
    subprocessArray.extend(["-filter_complex", concatString + "concat=n=" + str(n) + ":v=0:a=1", "data/" + prefix + ".m4a"])
    print subprocessArray
    subprocess.call(subprocessArray)
else:
    subprocess.call(["ffmpeg", "-y", "-f", "concat", "-i", "audioFiles.txt", "-c", "copy", "data/" + prefix + ".m4a"])

