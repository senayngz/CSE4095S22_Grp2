import json
import re

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

def get_test_input():
    #  i created this function since we will need to add some other code to get rid of punctuation marks
    # todo: using same method for refining the text (in here and tokenize part) would be better.
    return input("please write the text: ").split(" ")