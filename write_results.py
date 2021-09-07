"""
Highlight the mistakes in the text in red and suggestions in green using the html component htbuilder.
"""
import re
import nltk
import streamlit as st
from __init__ import annotated_text

def tokenize_input(text):
    words = nltk.word_tokenize(text)
    text = [word for word in words if word.isalnum()]
    return text

def write_results(text:str, p:float, d:dict):
    text_copy = text[:]
    st.write("Percentage of mistakes: " + str(round(p, 2)) + "%")
    splitted_text = text_copy.split()
    l = len(splitted_text) / 13 * 28

    errors_metadata = []
    for key, value in d.items():
        mistake_word = value['incorrect']
        if mistake_word not in text_copy:
            continue
        if mistake_word in text_copy:
            find_the_word = re.finditer('[^A-Za-z]'+mistake_word+'[^A-Za-z]', text )
            for match in find_the_word:
                start = match.start()
                end = match.end()
                # start = text.find(mistake_word)
                # end = start + len(mistake_word)
                errors_metadata.append( (start, end) )

    text_with_annotations = []
    prev_end = 0
    for start, end in sorted(errors_metadata):
        if prev_end == 0:
            pass
        text_with_annotations.append(text[prev_end:start])
        text_with_annotations.append((text[start:end], "", "#faa"))
        prev_end = end
    if prev_end < len(text):
        text_with_annotations.append(text[prev_end:])

    annotated_text(l, *text_with_annotations )

    st.write("Mistakes found: ")
    for key, value in d.items():
        corrects = value['correct']
        corrects_of_list = corrects if type(corrects) is list else [corrects]
        corrects_text = str.join(" or ", corrects_of_list)
        message = value['message']
        annotated_text(50, "Instead of ", (key, "", "#faa"), " should be ", (corrects_text, "", "#afa"), "      Explanation:  ",message)