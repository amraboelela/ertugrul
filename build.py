# importing the requests library
import sys, os 

if len(sys.argv) > 3:
    s = sys.argv[1]
    a = int(sys.argv[2])
    b = int(sys.argv[3])
else:
    print "please enter the season number, first episode number and the last episode numer"
    exit(-1)

for n in range(a, b+1):
    prefix = "ertugrul-" + s + "-" + format(n, '02d')
    os.system("./buildEpisode " + prefix)
