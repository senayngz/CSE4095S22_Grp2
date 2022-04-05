import math
import operator

from FileOperation import ReadCSV


def tTest(frequencyDict):
    criticalValue = 2.576   # value corresponding to a=0.1%
    corpus = ReadCSV("n-grams/corpus.json")
    total = 0
    for i in corpus.keys():
        total += corpus[i]
    tTestCollocations = dict()

    for i in frequencyDict.keys():
        value = frequencyDict[i]
        sampleMean = value / total
        meanOfDist = 1
        for word in i.split():
            meanOfDist *= corpus[word] / total
        try:
            t = (sampleMean - meanOfDist) / math.sqrt(sampleMean / total)
        except:
            t = 0
        if t > criticalValue:
            tTestCollocations[i] = [[frequencyDict[i], t] for i in frequencyDict.keys()]

    return dict(sorted(tTestCollocations.items(), key=operator.itemgetter(1), reverse=True))



