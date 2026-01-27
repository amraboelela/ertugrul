# importing the requests library
import sys, os
from pathlib import Path

# Get the project root directory (parent of scripts/)
script_dir = Path(__file__).parent
project_root = script_dir.parent
os.chdir(project_root)

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

for n in range(a, b+1):
    if s == "2":
        prefix = title + "-" + s + "-" + str(n).zfill(3)
    else:
        prefix = title + "-" + s + "-" + str(n).zfill(2)
    os.system("scripts/cleanEpisode " + prefix + " " + sourceLanguage + " " + targetLanguage)

