# importing the requests library
import sys, os 

if len(sys.argv) > 5:
    s = sys.argv[1]
    a = int(sys.argv[2])
    b = int(sys.argv[3])
    sourceLanguage = sys.argv[4]
    targetLanguage = sys.argv[5]
else:
    print "please enter the season number, first episode number, the last episode numer, the source language, and the target language"
    exit(-1)

for n in range(a, b+1):
    if s == "2":
        prefix = "ertugrul-" + s + "-" + format(n, '03d')
    else:
        prefix = "ertugrul-" + s + "-" + format(n, '02d')
    os.system("./buildEpisode " + prefix + " " + sourceLanguage + " " + targetLanguage)

