from zemberek import TurkishMorphology

import FileOperation
from Frequency import partOfSpeechFilter
from tTest import tTest

if __name__ == '__main__':
    morphology = TurkishMorphology.create_with_defaults()

    #FREQUENCY
    bigrams_collocations_frequency = partOfSpeechFilter(FileOperation.ReadCSV("bigrams.json"), 2, morphology)
    FileOperation.writeToCSV(bigrams_collocations_frequency, "bigrams_collocations_frequency")

    trigrams_collocations_frequency = partOfSpeechFilter(FileOperation.ReadCSV("trigrams.json"), 3, morphology)
    FileOperation.writeToCSV(trigrams_collocations_frequency, "trigrams_collocations_frequency")

    #TTEST
    bigrams_collocations_tTest = tTest(FileOperation.ReadCSV("bigrams.json"))
    FileOperation.writeToCSV(bigrams_collocations_tTest, "bigrams_collocations_tTest")

    trigrams_collocations_tTest = tTest(FileOperation.ReadCSV("trigrams.json"))
    FileOperation.writeToCSV(trigrams_collocations_tTest, "trigrams_collocations_tTest")

    #MUTUALINFO
    bigrams_collocations_mutual_info = tTest(FileOperation.ReadCSV("bigrams.json"))
    FileOperation.writeToCSV(bigrams_collocations_mutual_info, "bigrams_collocations_mutual_info")

    trigrams_collocations_mutual_info = tTest(FileOperation.ReadCSV("trigrams.json"))
    FileOperation.writeToCSV(trigrams_collocations_mutual_info, "trigrams_collocations_mutual_info")

    #FREQUENCY COMBINED WITH TTEST
    bigrams_tTest = tTest(FileOperation.ReadCSV("bigrams.json"))

    trigrams_tTest = tTest(FileOperation.ReadCSV("trigrams.json"))

    bigrams_collocations_frequency_tTest = partOfSpeechFilter(bigrams_tTest, 2)
    FileOperation.writeToCSV(bigrams_collocations_frequency_tTest, "bigrams_collocations_frequency_tTest")

    trigrams_collocations_frequency_tTest = partOfSpeechFilter(trigrams_tTest, 3)
    FileOperation.writeToCSV(trigrams_collocations_frequency_tTest, "trigrams_collocations_frequency_tTest")
