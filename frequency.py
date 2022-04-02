# from distutils.command.build import build
from lib2to3.pgen2 import token
from os import remove
import math
from typing import Dict
from pygments import lex
from zemberek import TurkishMorphology
from nltk import ngrams
import operator

def frequency(ngram, tokens):
    freq = dict()
    ngramsList = list(ngrams(tokens, ngram))
    for i in list(dict.fromkeys(ngramsList)):
        freq[i] = ngramsList.count(i)

    return dict(sorted(freq.items(), key=operator.itemgetter(1), reverse=True))


def partOfSpeechFilter(frequencyDict):
    posDict = dict()
    morphology = TurkishMorphology.create_with_defaults()
    tags = str()
    for ngram in frequencyDict.keys():
        for token in ngram:
            posTags = morphology.analyze(token.strip())
            posTags = str(posTags)
            if ":Adj" in posTags:
                tags += "A"
            elif ":Noun" in posTags:
                tags += "N"
        posDict[ngram] = [frequencyDict[ngram], tags]
        tags = ""
    return posDict