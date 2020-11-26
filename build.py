# importing the requests library
import sys, os 

if len(sys.argv) > 6:
    title = sys.argv[1]
    s = sys.argv[2]
    a = int(sys.argv[3])
    b = int(sys.argv[4])
    sourceLanguage = sys.argv[5]
    targetLanguage = sys.argv[6]
else:
    print("please enter the title, season number, first episode number, last episode numer, source language, and the target language")
    exit(-1)

os.system("./download " + title + " " + targetLanguage)
#exit(0)
for n in range(a, b+1):
    if s == "2":
        prefix = title + "-" + s + "-" + format(n, '03f')
    else:
        prefix = title + "-" + s + "-" + format(n, '02f')
    os.system("./buildEpisode " + prefix + " " + sourceLanguage + " " + targetLanguage)
