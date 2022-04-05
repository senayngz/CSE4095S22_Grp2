from zemberek import TurkishMorphology

import FileOperation
import MutualInformation
from Frequency import partOfSpeechFilter
from tTest import tTest


def main_method():
    '''    '''

    freq_test()
    print("freq test is done")

    t_test()
    print("t-test is done")


    MutualInformation.find_results()
    print("mutual info test is done")


    freq_with_t_test()
    print("all tests are done")



def freq_with_t_test():
    #FREQUENCY COMBINED WITH TTEST
    bigrams_tTest = tTest(FileOperation.ReadCSV("n-grams/bigrams.json"))

    trigrams_tTest = tTest(FileOperation.ReadCSV("n-grams/trigrams.json"))

    bigrams_collocations_frequency_tTest = partOfSpeechFilter(bigrams_tTest, 2)
    FileOperation.writeToCSV(bigrams_collocations_frequency_tTest, "results/bigrams_collocations_frequency_tTest")

    trigrams_collocations_frequency_tTest = partOfSpeechFilter(trigrams_tTest, 3)
    FileOperation.writeToCSV(trigrams_collocations_frequency_tTest, "results/trigrams_collocations_frequency_tTest")


def freq_test():
    morphology = TurkishMorphology.create_with_defaults()
    #FREQUENCY
    bigrams_collocations_frequency = partOfSpeechFilter(FileOperation.ReadCSV("n-grams/bigrams.json"), 2, morphology)
    FileOperation.writeToCSV(bigrams_collocations_frequency, "results/bigrams_collocations_frequency")

    trigrams_collocations_frequency = partOfSpeechFilter(FileOperation.ReadCSV("n-grams/trigrams.json"), 3, morphology)
    FileOperation.writeToCSV(trigrams_collocations_frequency, "results/trigrams_collocations_frequency")


def t_test():
    #TTEST
    bigrams_collocations_tTest = tTest(FileOperation.ReadCSV("n-grams/bigrams.json"))
    FileOperation.writeToCSV(bigrams_collocations_tTest, "results/bigrams_collocations_tTest")

    trigrams_collocations_tTest = tTest(FileOperation.ReadCSV("n-grams/trigrams.json"))
    FileOperation.writeToCSV(trigrams_collocations_tTest, "trigrams_collocations_tTest")