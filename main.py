import frequency as freq
import mutual_information as mut_in
import general


n_size = 2
tokens = general.readAndTokenizeFile("4.json")
collaction_type = 1
# n_size, collaction_type = prompt_user()


#freq

# noun adjective separation
freqs = freq.frequency(n_size, tokens)
pos = freq.partOfSpeechFilter(freqs)
print(pos)
#mutual
mip = mut_in.mutual_information_probability(n_size,tokens)

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
input_words = general.get_test_input()

mut_in.find_next_word(collocation_way, n_size, input_words)