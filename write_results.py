import nltk
import streamlit as st
from __init__ import annotated_text
import re

def tokenize_input(text):
    words = nltk.word_tokenize(text)
    text = [word for word in words if word.isalnum()]
    return text

def write_results(text:str, p:float, d:dict):
    st.write("Percentage of mistakes: " + str(round(p, 2)) + "%")
    #print(f"{text=}, {p=}, {d=}")
    splitted_text = text.split()
    l = len(splitted_text) / 13 * 28

    errors_metadata = []
    for key, value in d.items():
        mistake_word = value['incorrect']
        if mistake_word not in text:
            continue
        #if mistake_word in text:
        find_the_word = re.finditer(mistake_word, text)
        for match in find_the_word:
            start = match.start()
            end = match.end()
            #start = text.find(mistake_word)
            #end = start + len(mistake_word)
            errors_metadata.append((start, end))

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


"""st.write("Percentage of mistakes: " + str(round(p, 2)) + "%")
    splitted_text = text.split()
    positions_of_incorrect = [i['position'] for i in d.values()]
    for i in range(1, len(splitted_text)+1):
        if not i in positions_of_incorrect:
            splitted_text[i-1] = " " + splitted_text[i-1] + " "
        if i in positions_of_incorrect:
            splitted_text[i-1] = (splitted_text[i-1], "", "#faa")
    l = len(splitted_text) / 13 * 28
    annotated_text(l, *splitted_text)
    st.write("Incorrect: ")
    for key, value in d.items():
        annotated_text(35, (key, "", "#faa"), " must be written as ", (str(value['correct']), "", "#afa"))
    
    
        for index in range(len(splitted_text)):
            if splitted_text[index].lower() == mistake_word.lower():
                positions_of_incorrect = index
                index+=1
                if not i in positions_of_incorrect:
                    splitted_text[i - 1] = " " + splitted_text[i - 1] + " "
                if i in positions_of_incorrect:
                    splitted_text[i - 1] = (splitted_text[i - 1], "", "#faa")    
        
        """


"""annotated_word = (text[start:end], "", "#faa")
            splitted_text.append(text[:start])
            splitted_text.append(annotated_word)
            splitted_text_end.append(text[end:])
        annotated_text(150, *splitted_text)"""