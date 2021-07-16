from nltk.collocations import *
from nltk.corpus import stopwords
from Spell_check import tokenize_input




def collocations_check(text):
    text = tokenize_input(text)
    bigram_finder = BigramCollocationFinder.from_words(corpus)



text = ' Ive excepted the fact '
print(collocations_check(text))