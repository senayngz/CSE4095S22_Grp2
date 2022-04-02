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



mutual_info_dict = {}


def readAndTokenizeFile(filename):
    with open(filename, encoding='utf-8') as fh:
        data = json.load(fh)
    itemsList = [key + " " + value for key, value in data.items()]
    text = " ".join(itemsList)

    for aposthrope in ["’", "՚", "＇"]:  # turns different kind of apostrophes into one kind
        text = text.replace(aposthrope, "\'")

    pattern = "\'(.*?) "
    redundantText = re.findall(pattern, text)  # '___ <bosluk> arasındaki 'in 'ın 'nun gibi ekleri bulur

    words = re.split(r'\W+', text)  # noktalama işaretlerine göre ayırır
    cleanText = ' '.join((item for item in words if not item.isdigit()))  # sayıları çıkarır
    tokens = [token.lower() for token in cleanText.split(" ") if
              (token != "" and len(token) > 1)]  # uzunluğu 1den fazla olanları alır

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


def mutual_information_probability(n_gram):
    total = len(tokens)
    one_word_frequency = frequency(1, tokens)
    n_word_frequency = frequency(n_gram, tokens)

    for key in n_word_frequency.keys():
        top_part = n_word_frequency[key] / total
        bottom_part = 1
        for word in key:
            c = (word,)
            bottom_part *= one_word_frequency[c] / total

        mutual_info_dict[key] = math.log2(top_part / bottom_part)

    return dict(sorted(mutual_info_dict.items(), key=operator.itemgetter(1), reverse=True))


def prompt_user():
    while True:
        try:
            input_ngram_size = int(input("decide the ngram size(ex: 1,2,3 ): "))
            if not input_ngram_size > 0:
                int("error :)")
            input_collocation_type = int(input("\n(1) mutually probability\n(2) zemberek\n(3) something else\nplease choose collocation type: "))
            break
        except:
            print("\tyou must enter a number!!\n")

    return input_ngram_size+1, input_collocation_type


def find_next_word(chosen_collocation_way, n_size, input_words):
    # chosen_collocation_way = mip
    possible_next_words = {}
    for key in chosen_collocation_way.keys():
        # matches all string except last word, so we can have the probability list of possible next words
        for i in range(n_size):
            if i == n_size - 1:
                possible_next_words[key[i]] = chosen_collocation_way[key]
            elif key[i] == input_words[i]:
                continue
            else:
                break

    sorted(possible_next_words)
    for word in possible_next_words:
        print(word, "\t: \t", possible_next_words[word])


def get_test_input():
    input_str = input("please write the text: ")
    input_words = input_str.split(" ")
    #  i created this function since we will need to add some other code to get rid of punctuation marks
    # todo: using same method for refining the text (in here and tokenize part) would be better.
    return input_words


tokens = readAndTokenizeFile("4.json")

n_size = 2
collaction_type = 1
# n_size, collaction_type = prompt_user()


# noun adjective separation
freq = frequency(n_size, tokens)
pos = partOfSpeechFilter(freq)

# mutual information
mip = mutual_information_probability(n_size)

collocation_way = {}
if collaction_type == 1:
    collocation_way = mip
elif collaction_type == 2:
    collocation_way = pos
elif collaction_type == 3:
    # collocation_way =
    pass


# input_str = "kanun"
# input_words = input_str.split(" ")
input_words = get_test_input()

find_next_word(collocation_way, n_size, input_words)


# print("\nmost possible outcome: \t", input_str, list(possible_next_words.items())[0][0])

# print(possible_next_words)
''''''




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
