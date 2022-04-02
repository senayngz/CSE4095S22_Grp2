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

import frequency as freq

mutual_info_dict = {}

def mutual_information_probability(n_gram,tokens):
    total = len(tokens)
    one_word_frequency = freq.frequency(1, tokens)
    n_word_frequency = freq.frequency(n_gram, tokens)

    for key in n_word_frequency.keys():
        top_part = n_word_frequency[key] / total
        bottom_part = 1
        for word in key:
            c = (word,)
            bottom_part *= one_word_frequency[c] / total

        mutual_info_dict[key] = math.log2(top_part / bottom_part)

    return dict(sorted(mutual_info_dict.items(), key=operator.itemgetter(1), reverse=True))

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

