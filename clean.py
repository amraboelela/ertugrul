# importing the requests library
import sys, re

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print "please provide the file name"
    exit(-1)

file = open(filename) 
lines = file.read().splitlines()
for line in lines:
    if not line.strip():
        print
    elif "-->" in line or len(line) < 4 or "color=" in line or "9999" in line:
        x = 0
    else:
        line = remove_tags(line)
        line = line.replace('-','')
        print line
file.close()
