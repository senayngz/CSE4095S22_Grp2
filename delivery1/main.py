import FileOperation
from Frequency import partOfSpeechFilter
from tTest import tTest

if __name__ == '__main__':
    bigrams_collocations_frequency = partOfSpeechFilter(FileOperation.ReadCSV("bigrams.json"), 2)
    FileOperation.writeToCSV(bigrams_collocations_frequency, "bigrams_collocations_frequency")

    trigrams_collocations_frequency = partOfSpeechFilter(FileOperation.ReadCSV("trigrams.json"), 3)
    FileOperation.writeToCSV(trigrams_collocations_frequency, "trigrams_collocations_frequency")

    bigrams_collocations_tTest = tTest(FileOperation.ReadCSV("bigrams.json"))
    FileOperation.writeToCSV(bigrams_collocations_tTest, "bigrams_collocations_tTest")

    trigrams_collocations_tTest = tTest(FileOperation.ReadCSV("trigrams.json"))
    FileOperation.writeToCSV(trigrams_collocations_tTest, "trigrams_collocations_tTest")
