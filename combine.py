# importing the requests library
import os, sys, subprocess

if len(sys.argv) > 3:
    directory = sys.argv[1]
    sourceLanguage = sys.argv[2]
    targetLanguage = sys.argv[3]
else:
    print "please provide the directory, source language, and target language"
    exit(-1)
filePath = directory + "/" + directory
#subprocess.call(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "audioFiles.txt", "-acodec", "copy", directory + "/" + directory + ".mp3", "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1"])
#subprocess.call(["ffmpeg", "-y", "-i", filePath + "-005-en.m4a", "-i", filePath + "-005-original.m4a", "-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1", filePath + ".m4a"])
#exit(0)
outputFile = open("audioFiles.txt", "w")
files = os.listdir(directory)
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
            target = "file '" + directory + "/" + file + "'\n"
        if "-" + sourceLanguage in file:
            outputFile.write("file '" + directory + "/" + file + "'\n")
            outputFile.write("file 'silence1.m4a'\n")
            outputFile.write(target)
            outputFile.write("file 'silence1.m4a'\n")
            outputFile.write("file 'silence1.m4a'\n")
    else:
        if targetLanguage == "original":
            if "-" + sourceLanguage in file or "-" + targetLanguage in file:
                subprocessArray.extend(["-i", directory + "/" + file])
                subprocessArray.extend(["-i", "silence1.m4a"])
                concatString = concatString + "[" + str(fileCount) + ":a]"
                fileCount = fileCount + 1
                concatString = concatString + "[" + str(fileCount) + ":a]"
                fileCount = fileCount + 1
            if targetLanguage in file:
                count = count + 1
                if count % 50 == 0:
                    if count / 50 > 0:
                        subprocessArray.extend(["-filter_complex", concatString + "concat=n=" + str(fileCount) + ":v=0:a=1", filePath + "-" + format(count / 50, "02d") + ".m4a"])
                        print subprocessArray
                        subprocess.call(subprocessArray)
                        fileCount = 0
                        concatString = ""
                        #exit(0)
                    subprocessArray = ["ffmpeg", "-y"]
        else:
            if "-" + sourceLanguage in file or "-" + targetLanguage in file:
                outputFile.write("file '" + directory + "/" + file + "'\n")
                outputFile.write("file 'silence1.m4a'\n")
            if targetLanguage in file:
                outputFile.write("file 'silence1.m4a'\n")
#print subprocessArray
#subprocessArray.extend(["-filter_complex", "[0:a][1:a]concat=n=2:v=0:a=1", filePath + ".m4a"])
#print subprocessArray
outputFile.close()
#subprocess.call(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "audioFiles.txt", "-c", "copy", directory + "/" + directory + ".m4a"])
#exit(0)
if targetLanguage == "original":
    if count % 50 > 1:
        n = count / 50 + 1
        subprocessArray.extend(["-filter_complex", concatString + "concat=n=" + str(fileCount) + ":v=0:a=1", filePath + "-" + format(n, '02d') + ".m4a"])
        #print subprocessArray
        subprocess.call(subprocessArray)
    #exit(0)
    concatString = ""
    subprocessArray = ["ffmpeg", "-y"]
    for i in range(0, n):
        subprocessArray.extend(["-i", filePath + "-" + format(i+1, '02d') + ".m4a"])
        concatString = concatString + "[" + str(i) + ":a]"
    subprocessArray.extend(["-filter_complex", concatString + "concat=n=" + str(n) + ":v=0:a=1", filePath + ".m4a"])
    print subprocessArray
    subprocess.call(subprocessArray)
else:
    subprocess.call(["ffmpeg", "-y", "-f", "concat", "-i", "audioFiles.txt", "-c", "copy", directory + "/" + directory + ".m4a"])

