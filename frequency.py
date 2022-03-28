# from distutils.command.build import build
import json
from lib2to3.pgen2 import token
from os import remove
import re
import math
from typing import Dict
from pygments import lex
from zemberek import TurkishMorphology
from nltk import ngrams
import operator


def readAndTokenizeFile(filename):
    with open(filename, encoding='utf-8') as fh:
        data = json.load(fh)
    itemsList = [key+" "+value for key, value in data.items()]
    text = " ".join(itemsList)
    text.replace( "�", "\'" ) # ’ güzelmiş ’
    pattern = "\'(.*?) "
    redundantText = re.findall(pattern, text)# '___ <bosluk> arasındaki 'in 'ın 'nun gibi ekleri bulur

    words = re.split(r'\W+', text)  #noktalama işaretlerine göre ayırır
    cleanText = ' '.join((item for item in words if not item.isdigit())) #sayıları çıkarır
    tokens = [token.lower() for token in cleanText.split(" ") if (token != "" and len(token)>1)] #uzunluğu 1den fazla olanları alır

    for i in tokens:
        for t in redundantText:
            if i == t:
                tokens.remove(i)
    return tokens

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


tokens = readAndTokenizeFile("4.json")
freq = frequency(3, tokens)

# print(freq)

pos = partOfSpeechFilter(freq)
print(pos)





# mutual information
mutual_info_dict = {}


def mutual_information_probability(n_gram):
    total = len(tokens)
    one_word_frequency = frequency(1, tokens)
    two_word_frequency = frequency(n_gram, tokens)

    for i in two_word_frequency.keys():
        freq_b = two_word_frequency[i]/total
        bottom_part = 1
        for j in i:
            c = (j,)
            bottom_part *= one_word_frequency[c] /total

        mutual_info_dict[i] = math.log2(freq_b/bottom_part)

    print(dict(sorted(mutual_info_dict.items(), key=operator.itemgetter(1), reverse=True)))


'''
mutual_information_probability(2)
mutual_information_probability(3)

#mutual_probs[]


for i in range(total):
    mutual_prob = frequency(2, tokens)
    mutual_info_dict[ str(tokens[i]) +", " + str(tokens[i+1]) ] = math.log2(mutual_prob * prob_a * prob_b)
    




print("total count:", total)

for dict in occurence_count_list:
    print(dict, occurence_count_list[dict])
'''
