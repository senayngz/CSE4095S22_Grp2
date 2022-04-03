import math
import operator


def mutual_information_probability(n_gram):
    total = len(tokens)
    one_word_frequency = frequency(1, tokens)
    two_word_frequency = frequency(n_gram, tokens)

    for i in two_word_frequency.keys():
        freq_b = two_word_frequency[i] / total
        bottom_part = 1
        for j in i:
            c = (j,)
            bottom_part *= one_word_frequency[c] / total

        mutual_info_dict[i] = math.log2(freq_b / bottom_part)

    print(dict(sorted(mutual_info_dict.items(), key=operator.itemgetter(1), reverse=True)))