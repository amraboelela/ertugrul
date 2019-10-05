# importing the requests library
import sys, subprocess

if len(sys.argv) > 1:
    prefix = sys.argv[1]
else:
    print "please provide the prefix"
    exit(-1)

filePath = "data/" + prefix + "-en.vtt" 
file = open(filePath) 
lines = file.read().splitlines()
count = 0
prevStartTime = "00:00:00"
for line in lines:
    if "-->" in line:
        times = line.split(" --> ")
        startTime = times[0][:len(times[0])-4]
        print "prevStartTime: " + prevStartTime
        print "startTime: " + startTime
        if count > 4:
            targetFilePath = "data/" + prefix + "/" + prefix + "-" + format(count, '03d') + "-original"
            subprocess.call(["ffmpeg", "-y", "-i", "data/" + prefix + "-original.m4a", "-acodec", "copy", "-ss", prevStartTime, "-to", startTime, targetFilePath + "~.m4a"])
            subprocess.call(["ffmpeg", "-y", "-i", targetFilePath + "~.m4a", "-filter:a", "volume=5", targetFilePath + ".m4a"])
            subprocess.call(["rm", targetFilePath + "~.m4a"])
            #exit(0)
        prevStartTime = startTime
        count = count + 1
file.close()

