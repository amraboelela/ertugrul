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
#print directory
#subprocess.call(["mkdir", directory + "/silence"])
for file in files:
    if ".DS_Store" in file:
        x = 1
    else:
        #silenceFile = directory + "/silence/" + file.replace(".m4a", "-silence.m4a")
        #subprocess.call(["ffmpeg", "-f", "lavfi", "-t", "1", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100", "-i", directory + "/" + file, "-filter_complex", """[1:a][0:a]concat=n=2:v=0:a=1""", "-strict", "-2", silenceFile])
        outputFile.write("file '" + directory + "/" + file + "'\n")
        outputFile.write("file 'silence1.m4a'\n")
        if "-en" not in file:
            outputFile.write("file '" + directory + "/" + file + "'\n")
            outputFile.write("file 'silence1.m4a'\n")
            outputFile.write("file 'silence1.m4a'\n")

outputFile.close()
subprocess.call(["ffmpeg", "-f", "concat", "-safe", "0", "-i", "audioFiles.txt", "-c", "copy", directory + ".m4a"])

