# importing the requests library
import sys

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print "please provide the file name and the target language"
    exit(-1)

file = open(filename) 
lines = file.read().splitlines()
for line in lines:
    if not line.strip():
        print
    elif "-->" in line or len(line) < 4 or "color=" in line or "9999" in line:
        x = 0
    else:
        print line
file.close()

