import operator

from nltk import ngrams


def frequency(ngram, tokens):
    freq = dict()
    ngramsList = list(ngrams(tokens, ngram))
    for i in list(dict.fromkeys(ngramsList)):
        freq[i] = ngramsList.count(i)

    return dict(sorted(freq.items(), key=operator.itemgetter(1), reverse=True))


def partOfSpeechFilter(frequencyDict, ngrams, morphology):
    posDict = dict()
    filteringTagsTrigrams = ["NNN", "NNV", "NAN", "VNN", "NVN", "NNA", "ANN", "ANV"]
    filteringTagsBigrams = ["NN", "AN", "NA", "NV"]
    tags = str()
    for ngram in frequencyDict.keys():
        for token in ngram.split():
            posTags = morphology.analyze(token.strip())
            posTags = str(posTags)
            if ":Adj" in posTags:
                tags += "A"
            elif ":Noun" in posTags:
                tags += "N"
            elif ":Verb" in posTags:
                tags += "V"
        if len(tags) == len(ngram.split()):
            if ngrams == 3:
                if tags in filteringTagsTrigrams:
                    posDict[ngram] = [frequencyDict[ngram], tags]
            elif ngrams == 2:
                if tags in filteringTagsBigrams:
                    posDict[ngram] = [frequencyDict[ngram], tags]
        tags = ""
    return dict(sorted(posDict.items(), key=operator.itemgetter(1), reverse=True))

