# importing the requests library
import sys, re

TAG_RE = re.compile(r'<[^>]+>')

def remove_tags(text):
    return TAG_RE.sub('', text)

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    print("please provide the file name")
    exit(-1)

cleanArray = ["-->", "color=", "9999", "WEBVTT", "Kind: captions", "Language:"]
cleanArray2 = ["RESURRECTION ERTUGRUL", "THE STORIES AND CHARACTERS DEPICTED", "HERE WERE INSPIRED BY OUR HISTORY", "NO ANIMALS WERE HARMED DURING", "THE FILMING OF THIS PRODUCTION", "Translation:"]

file = open(filename) 
lines = file.read().splitlines()
for line in lines:
    skipLine = False
    if len(line) < 4:
        skipLine = True
    for token in cleanArray:
        if token in line:
            skipLine = True
            break
    if "ertugrul-1-01" not in filename:
        for token in cleanArray2:
            if token in line:
                skipLine = True
                break
    if not skipLine:
        if not line.strip():
            print
        else:
            line = remove_tags(line)
            line = line.replace('-','')
            print line
file.close()

