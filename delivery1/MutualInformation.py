import math
import operator
import FileOperation


def mutual_information_probability(frequency_dict):
    corpus = FileOperation.ReadCSV("n-grams/corpus.json")
    mutual_info_dict = dict()
    total = 0
    for i in corpus.values():
        total += i

    for i in frequency_dict.keys():
        n_gram_freq = frequency_dict[i] / total
        probability = 1
        for word in i.split():
            probability *= corpus[word] / total

        if probability > 3:
            mutual_info_dict[i] = math.log2(n_gram_freq / probability)

    return dict(sorted(mutual_info_dict.items(), key=operator.itemgetter(1), reverse=True))


def find_results():
    bigrams_collocations_mutual_info = mutual_information_probability(FileOperation.ReadCSV(
        "n-grams/bigrams.json"))
    FileOperation.writeToCSV(bigrams_collocations_mutual_info, "results/bigrams_collocations_mutual_info")

    trigrams_collocations_mutual_info = mutual_information_probability(FileOperation.ReadCSV(
        "n-grams/trigrams.json"))
    FileOperation.writeToCSV(trigrams_collocations_mutual_info, "results/trigrams_collocations_mutual_info")
