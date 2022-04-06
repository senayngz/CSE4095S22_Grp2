# from distutils.command.build import build
import json
import FileOperation
from lib2to3.pgen2 import token
from os import remove
import re
import math
from typing import Dict
from pygments import lex
from zemberek import TurkishMorphology
from nltk import ngrams
import operator
from collections import defaultdict

class DatasetMetaData:
    def __init__(self):
        self.valueList = list()
        self.count = 0
        self.sumVal = 0
        self.variance = 0
        self.standardDeviation = 0
        self.mean = 0


def readAndTokenizeFile(filename):
    with open(filename, encoding='utf-8') as fh:
        data = json.load(fh)
    itemsList = [key + " " + value for key, value in data.items()]
    text = " ".join(itemsList)
    text.replace("�", "\'")  # ’ güzelmiş ’
    pattern = "\'(.*?) "
    redundantText = re.findall(pattern, text)  # '___ <bosluk> arasındaki 'in 'ın 'nun gibi ekleri bulur

    words = re.split(r'\W+', text)  # noktalama işaretlerine göre ayırır
    cleanText = ' '.join((item for item in words if not item.isdigit()))  # sayıları çıkarır
    tokens = [token.lower() for token in cleanText.split(" ") if
              (token != "" and len(token) > 1)]  # uzunluğu 1den fazla olanları alır

    for i in tokens:
        for t in redundantText:
            if i == t:
                if(i in tokens):
                    tokens.remove(i)

    return tokens



def meanAndVariance(tokens, offset):
    tempDict = defaultdict();
    for i in range(0, len(tokens)):
        for j in range(-offset, offset + 1):
            if(j != 0):
                if(i + j >= 0 and i + j < len(tokens)):
                    metaData : DatasetMetaData = tempDict.get((tokens[i],tokens[i + j]), DatasetMetaData())
                    metaData.count = metaData.count + 1
                    metaData.valueList.append(j)
                    metaData.sumVal = metaData.sumVal + j
                    tempDict[(tokens[i],tokens[i + j])] = metaData


    for pair in tempDict.items():
        data: DatasetMetaData = pair[1]
        if (data.count == 0 or data.count == 1):
            data.mean = math.inf
            data.variance = math.inf
            data.standardDeviation = math.inf
        else:
            data.mean = data.sumVal / data.count
            tempVar = 0
            for val in data.valueList:
                tempVar = tempVar + math.pow(data.mean - val, 2)

            tempVar = tempVar / (data.count - 1)
            data.variance = tempVar
            tempVar = math.sqrt(tempVar)
            data.standardDeviation = tempVar

    return tempDict




filePost = ".json"
filePre = "../2021-01/"
tokens = readAndTokenizeFile(filePre + "1" + filePost);
for i in range(2, 27843):
  #  tokens += readAndTokenizeFile(filePre + (i.__str__()) + filePost );
    tokens = (readAndTokenizeFile( filePre + i.__str__() + filePost) + tokens)  ;

#i = 1
#tokens = readAndTokenizeFile(filePre + (i.__str__()) + filePost )
analysisResult = meanAndVariance(tokens, 4)

fileWriteResults : dict = defaultdict();
for pair in analysisResult.items():
    data : DatasetMetaData = pair[1]
    # print("----")
    fileWriteResults[(pair[0]).__str__()] = data.variance
    # print("Token Pair = " + (pair[0]).__str__())
    # print("Count = " + (data.count).__str__())
    # print("Sum = " + (data.sumVal).__str__())
    # print("Mean = " + (data.mean).__str__())
    # print("Variance (s^2) = " + (data.variance).__str__())
    # print("STDev (s) = " + (data.standardDeviation ).__str__())
    # strVal = ""
    # for var in data.valueList:
    #     strVal = strVal + (var).__str__() + " , "
    # print("Values --> " + strVal)


FileOperation.writeToCSV(fileWriteResults, "test")

# for pair in analysisResult.items():
#     data : DatasetMetaData = pair[1]
#     print("----")
#     print("Token Pair = " + (pair[0]).__str__())
#     print("Count = " + (data.count).__str__())
#     print("Sum = " + (data.sumVal).__str__())
#     print("Mean = " + (data.mean).__str__())
#     print("Variance (s^2) = " + (data.variance).__str__())
#     print("STDev (s) = " + (data.standardDeviation ).__str__())
#     strVal = ""
#     for var in data.valueList:
#         strVal = strVal + (var).__str__() + " , "
#     print("Values --> " + strVal)








