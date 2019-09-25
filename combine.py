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
subprocess.call(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "audioFiles.txt", "-c", "copy", directory + ".m4a"])
#subprocess.call(["ffmpeg", "-loop", "1", "-i", directory + ".png", "-i", directory + ".m4a", "-c:v", "libx264", "-tune", "stillimage", "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p", "-shortest", directory + ".mp4"])

