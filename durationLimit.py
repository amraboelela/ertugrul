
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

def timeStamp(prefix, targetLanguage, minutes, seconds, milliseconds):
    result = minutes * 60 + seconds + float(milliseconds) / 1000
    shiftedSeconds = 0
    if targetLanguage == "ar":
        subPrefix = prefix[:11]
        if subPrefix == "ertugrul-1-":
            episode = prefix[11:13]
            print("episode: " + episode)
            if episode == "01" or episode == "02" or episode == "04" or episode == "06":
                shiftedSeconds = 60 + 43
            elif episode == "03" or episode == "05":
                shiftedSeconds = 60 + 41
            elif episode == "12":
                shiftedSeconds = 2 * 60 + 7
            elif episode == "13" or episode == "20":
                shiftedSeconds = 2 * 60
            else:
                shiftedSeconds = 2 * 60 + 2
    result = result - shiftedSeconds
    if result < 0:
        result = 0
    return result
