# importing the requests library
import os, sys, subprocess

if len(sys.argv) > 1:
    directory = sys.argv[1]
else:
    print "please provide the directory"
    exit(-1)

files = os.listdir(directory)
files.sort()
for file in files:
    if ".DS_Store" in file:
        x = 1
    else:
        print file
