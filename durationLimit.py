
def lowerLimit(prefix, targetLanguage):
    durationsLimitPath = "build/durationsLimit-" + targetLanguage + ".txt"
    durationsLimitFile = open(durationsLimitPath)
    durationsLimitLines = durationsLimitFile.read().splitlines()
    durationsLimitDictionary = {}
    for durationsLimitLine in durationsLimitLines:
        lineSplit = durationsLimitLine.split(":")
        theEpisode = lineSplit[0].strip()
        if len(lineSplit) > 1:
            limit = lineSplit[1].strip()
            #print("word: " + word)
            durationsLimitDictionary[theEpisode] = int(limit)
        else:
            print("theEpisode without limit: " + theEpisode)
    prefixParts = prefix.split("-")
    episode = prefixParts[2]
    #print("episode: " + episode)
    return durationsLimitDictionary[episode]

def upperLimit(targetLanguage):
    durationUpperLimit = 22
    if targetLanguage == "ar":
        durationUpperLimit = 20000
    return durationUpperLimit
