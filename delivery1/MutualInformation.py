import math
import operator

from FileOperation import ReadCSV


def mutual_information_probability(frequencyDict):
    corpus = ReadCSV("corpus.json")
    mutual_info_dict = dict()
    total = 0
    for i in corpus.keys():
        total += corpus[i]

    for i in frequencyDict.keys():
        ngramFreq = frequencyDict[i] / total
        value = 1
        for word in i.split():
            value *= corpus[word] / total

        mutual_info_dict[i] = math.log2(ngramFreq / value)

    return dict(sorted(mutual_info_dict.items(), key=operator.itemgetter(1), reverse=True))

