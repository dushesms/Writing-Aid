from __future__ import print_function, unicode_literals
import spacy
import en_core_web_lg
import topic_recognition
import streamlit as st

def _lang_level(text):
  nlp = spacy.load("en_core_web_lg")
  doc = nlp(text)
  lemma = []
  for token in doc:
    lemma += [str.lower(token.lemma_)]
#interpret topic recognition results
  if topic_recognition.predict_topic(text) == 'family':
    level = 1
  elif topic_recognition.predict_topic(text) == 'hobbies and pasttimes' or 'holidays' or 'shopping' or 'work and jobs':
    level = 2
  elif topic_recognition.predict_topic(text) == 'education' or 'leisure activities':
    level = 2.5
  elif topic_recognition.predict_topic(text) == 'books and literature' or 'arts' or 'media' or 'news, lifestyles and current affairs' or 'film':
    level = 4
  elif topic_recognition.predict_topic(text) == 'scientific development' or 'technical and legal language':
    level = 5
  st.write('Your predicted level is ',level, '. See reference in the results section. ')

#load data with levelled words
  dict_vocab = {}
  d1 = open('vocabulary lists/A1 vocabulary list.txt', 'r')
  d2 = open('vocabulary lists/A2 vocabulary list.txt', 'r')
  d3 = open('vocabulary lists/B1 vocabulary list.txt', 'r')
  d4 = open('vocabulary lists/B2 vocabulary list.txt', 'r')
  d5 = open('vocabulary lists/C1 vocabulary list.txt', 'r')

  dict_vocab['A1'] = d1.read().split('\n')
  dict_vocab['A2'] = d2.read().split('\n')
  dict_vocab['B1'] = d3.read().split('\n')
  dict_vocab['B2'] = d4.read().split('\n')
  dict_vocab['C1'] = d5.read().split('\n')

  set_A1 = set(dict_vocab['A1'])
  set_A2 = set(dict_vocab['A2'])
  set_B1 = set(dict_vocab['B1'])
  set_B2 = set(dict_vocab['B2'])
  set_C1 = set(dict_vocab['C1'])

#count lexical density for each level
  set_essay = set(lemma)
  words_from_dict1 = set_A1.intersection(set_essay)
  words_from_dict2 = set_A2.intersection(set_essay)
  words_from_dict3 = set_B1.intersection(set_essay)
  words_from_dict4 = set_B2.intersection(set_essay)
  words_from_dict5 = set_C1.intersection(set_essay)
  word_count1 = len(words_from_dict1)
  word_count2 = len(words_from_dict2)
  word_count3 = len(words_from_dict3)
  word_count4 = len(words_from_dict4)
  word_count5 = len(words_from_dict5)
  total_count = len(lemma)
  lex_density1 = round((word_count1/total_count) * 100, 2)
  lex_density2 = round((word_count2/total_count) * 100, 2)
  lex_density3 = round((word_count3/total_count) * 100, 2)
  lex_density4 = round((word_count4/total_count) * 100, 2)
  lex_density5 = round((word_count5/total_count) * 100, 2)
  st.write('Percentage of words from level 1 is: ',lex_density1,
            '\n Percentage of words from level 2 is: ',lex_density2,
            '\n Percentage of words from level 3 is: ',lex_density3,
            '\n Percentage of words from level 4 is: ',lex_density4,
            '\n Percentage of words from level 5 is: ',lex_density5)