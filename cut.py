# importing the requests library
import sys, subprocess

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print "please provide the vtt file name"
    exit(-1)

prefix = filename[:len(filename)-7]
#print prefix
file = open(filename) 
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
            targetFilePath = prefix + "/" + prefix + "-" + format(count, '03d') + "-original"
            subprocess.call(["ffmpeg", "-y", "-i", prefix + "-original.m4a", "-acodec", "copy", "-ss", prevStartTime, "-to", startTime, targetFilePath + "~.m4a"])
            #subprocess.call(["ffmpeg", "-y", "-i", prefix + "-original.m4a", "-ss", prevStartTime, "-t", startTime, prefix + "/" + prefix + "-" + format(count, '03d') + "-original.m4a"])
            subprocess.call(["ffmpeg", "-y", "-i", targetFilePath + "~.m4a", "-filter:a", "volume=5", targetFilePath + ".m4a"])
            subprocess.call(["rm", targetFilePath + "~.m4a"])
            #exit(0)
        prevStartTime = startTime
        count = count + 1
file.close()

