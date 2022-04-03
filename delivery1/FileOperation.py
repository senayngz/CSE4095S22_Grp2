import json
import os
import re
import Frequency
import pandas as pd
import StopWord
from nltk.corpus import stopwords
stopWords = list(StopWord.STOP_WORDS)


def readAndTokenizeFile(filename):
    with open(filename, encoding='utf-8') as fh:
        data = json.load(fh)

    itemsList = [key + " " + value for key, value in data.items()]
    text = " ".join(itemsList)

    for apostrophe in ["’", "՚", "＇"]:  # turns different kind of apostrophes into one kind
        text = text.replace(apostrophe, "\'")

    pattern = "\'(.*?) "
    redundantText = re.findall(pattern, text)  # '___ <bosluk> arasındaki 'in 'ın 'nun gibi ekleri bulur

    stoplist = stopwords.words('turkish')  # Bring in the default Turkish NLTK stop words 

    words = re.split(r'\W+', text)  # noktalama işaretlerine göre ayırır
    cleanText = ' '.join((item for item in words if not item.isdigit()))  # sayıları çıkarır
    tokens = [token for token in cleanText.split(" ") if
              (token != "" and len(token) > 1 and token not in stoplist)]  # uzunluğu 1den fazla olanları alır

    for i in tokens:
        for t in redundantText:
            if i == t:
                tokens.remove(i)
                break
    return tokens


def readAllFilesInRepo():
    listOfTheFiles = list()
    #dosyaların olduğu path'i koyun
    #path = "C:/Users/senayangoz/Desktop/NLP/deneme"
    path = "C:/Users/mikailtorun/Desktop/Odevler/NLP/2021-01"
    for files in os.walk(path, topdown=False):
        for file in files[2]:
            listOfTheFiles.append(f"{path}/{file}")
    return listOfTheFiles


def getCorpus():
    files = readAllFilesInRepo()
    corpus = dict()
    for file in files:
        tokens = readAndTokenizeFile(file)
        freq1 = Frequency.frequency(1, tokens)
        freq = dict()
        for i in freq1.keys():
            freq[i[0]] = freq1[i]
        setOfCorpus = set(corpus)
        for ngram in setOfCorpus.intersection(set(freq)):
            corpus[ngram] += freq[ngram]
            del freq[ngram]
        corpus.update(freq)

    return corpus


def getNgrams(ngram):
    files = readAllFilesInRepo()
    corpus = dict()
    for file in files:
        tokens = readAndTokenizeFile(file)
        freq1 = Frequency.frequency(ngram, tokens)
        freq = dict()
        for i in freq1.keys():
            tempList = list()
            for m in i:
                tempList.append(m)
            str = ' '.join(tempList)
            freq[str] = freq1[i]
        setOfCorpus = set(corpus)
        for i in setOfCorpus.intersection(set(freq)):
            corpus[i] += freq[i]
            del freq[i]
        corpus.update(freq)

    return corpus


def writeToCSV(data, fileName):
    jsonString = json.dumps(data, ensure_ascii=False)
    jsonFile = open(f"{fileName}.json", "w", encoding='utf8')
    jsonFile.write(jsonString)
    jsonFile.close()


def ReadCSV(filename):
    df = pd.read_csv(filename)
    dfDict = df.to_dict('split')
    strList = dfDict["columns"]
    jsonStr = ','.join(strList)
    convertedDict = json.loads(jsonStr)
    return convertedDict

def cleanStopWords(ngrams):
    """
        hocaya sor
         keysToRemove = list()
         for key in convertedDict.keys():
            for token in key.split():
                if token in stopWords:
                    if key not in keysToRemove:
                        keysToRemove.append(key)
        for i in keysToRemove:
            del convertedDict[i]
        print (keysToRemove)
        """

#cleanData = ReadCSV("trigrams.json")

"""
corpus = getCorpus()
writeToCSV(corpus, "corpus")

bigrams = getNgrams(2)
writeToCSV(bigrams, "bigrams")

trigram = getNgrams(3)
writeToCSV(trigram, "trigrams")
"""
