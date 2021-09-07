from spellchecker import SpellChecker
from textblob import TextBlob
import nltk
from domain import SuggestCorrection
from utils import percentage_of_incorrect
from write_results import write_results

#this function compares the raw input text and corrected text which is the base for
def compare(text1, text2):
    l1 = text1.split()
    l2 = text2.split()
    correct = 0
    incorrect = 0
    dict_of_incorrect = {}
    for i in range(0, len(l1)):
        if l1[i] != l2[i]:
            incorrect += 1
            dict_of_incorrect[l1[i]] = {'incorrect': l1[i], 'correct': l2[i], 'position': i, 'message': 'Possible spelling mistake found.'}
        else:
            correct += 1
    return (correct, incorrect), dict_of_incorrect

def tokenize_input(text):
    words = nltk.word_tokenize(text)
    text = [word for word in words if word.isalnum()]
    return text

def correct_percentage_and_mistakes(text):
    text = tokenize_input(text)
    text = " ".join(text)
    text_corrected = TextBlob(text).correct()
    tuple_of_words, dict_of_incorrect = compare(text, text_corrected)
    percentage = percentage_of_incorrect(tuple_of_words[0], tuple_of_words[1])
    return percentage, dict_of_incorrect

def correct_percentage_and_mistakes_js(text):
    text = tokenize_input(text)
    text = " ".join(text)
    corrector = jamspell.TSpellCorrector()
    corrector.LoadLangModel('en.bin')
    text_corrected = corrector.FixFragment(text)
    tuple_of_words, dict_of_incorrect = compare(text, text_corrected)
    percentage = percentage_of_incorrect(tuple_of_words[0], tuple_of_words[1])
    return percentage, dict_of_incorrect

def spell_check_js(text):
    p, d = correct_percentage_and_mistakes_js(text)
    return SuggestCorrection(
        data=d,
        percentage_of_incorrect=p
    )

def spell_check_enchant_with_print_result(text):
    result = spell_check_enchant(text)
    write_results(text, result.percentage_of_incorrect, result.data)

def spell_check_jamspell_print_results(text):
    result = spell_check_js(text)
    write_results(text, result.percentage_of_incorrect, result.data)

def spell_check_norvig_print_results(text):
    result = spell_check_norvig(text)
    write_results(text, result.percentage_of_incorrect, result.data)


def spell_check_norvig(text):
    spell = SpellChecker()
    splitted_text = text.split()
    misspelled = spell.unknown(splitted_text)
    d = {}

    for word in misspelled:
        index = 0
        message = 'Possible spelling mistake found.'
        for i in range(len(splitted_text)):
            if splitted_text[i] == word:
                index = i+1

        d[word] = {'incorrect': word, 'correct': spell.correction(word),'position': index, 'message': message}

    p = percentage_of_incorrect(len(text.split())-len(misspelled),len(misspelled))

    return SuggestCorrection(
        data=d,
        percentage_of_incorrect=p
    )

def spell_check_enchant(text):
    glossary = enchant.Dict("en_US")
    splitted_text = text.split()
    d = {}
    misspelled = []
    for word in splitted_text:
        if glossary.check(word):
            continue
        else:
            misspelled.append(word)
    for word in misspelled:
        message = 'Possible spelling mistake found.'
        for i in range(len(splitted_text)):
            if splitted_text[i].lower() == word:
                index = i + 1
        d[word] = {'incorrect': word, 'correct': glossary.suggest(word)[0], 'position': index, 'message':message}
    p = percentage_of_incorrect(len(text.split()) - len(misspelled), len(misspelled))

    return SuggestCorrection(
        data=d,
        percentage_of_incorrect=p
    )








