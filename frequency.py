from distutils.command.build import build
import json
from lib2to3.pgen2 import token
from os import remove
import re
from typing import Dict
from pygments import lex
from zemberek import TurkishMorphology
from nltk import ngrams
import operator


def readAndTokenizeFile(filename):
    with open('27614.json', encoding='utf-8') as fh: 
        data = json.load(fh)
    itemsList = [key+" "+value for key, value in data.items()]
    text  = " ".join(itemsList)
    pattern = "\'(.*?) "
    redundantText = re.findall(pattern,text)# '___ <bosluk> arasındaki 'in 'ın 'nun gibi ekleri bulur
    
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
    
    return dict(sorted(freq.items(), key=operator.itemgetter(1),reverse=True))

def partOfSpeechFilter(frequencyDict):
    posDict = dict()
    morphology = TurkishMorphology.create_with_defaults()
    tags = str()
    for ngram in frequencyDict.keys():
        for token in ngram:
            posTags = morphology.analyze(token.strip())
            posTags = str(posTags)
            if ":Adj" in posTags:
                tags+="A"
            elif ":Noun" in posTags:
                tags+="N"
        posDict[ngram] = [frequencyDict[ngram], tags]
        tags =""
    return posDict


tokens = readAndTokenizeFile("27614.json")
freq = frequency(3, tokens)
pos = partOfSpeechFilter(freq)
print (pos)


