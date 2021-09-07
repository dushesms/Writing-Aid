from __future__ import print_function, unicode_literals
import topic_recognition
import streamlit as st
from nltk.tokenize import word_tokenize
from operator import itemgetter
from nltk.stem import WordNetLemmatizer
import nltk
nltk.download('wordnet')
import os

def round_num(score):
  decimal = score - int(score)
  if decimal >= 0.5:
    return int(score)+1
  else:
    return int(score)

def topic_level(text):
# interpret topic recognition results
  try:
    points = []
    predictions = topic_recognition.predict_topic(text)
    topics = predictions.split(', ')
    for i in range(0, len(topics)):
      topic = topics[i]

      if topic == 'family':
        point = 1
      elif (topic == 'hobbies and pasttimes') or (topic =='holidays') or (topic =='shopping') or (topic =='work and jobs'):
        point = 2
      elif (topic == 'education') or (topic =='leisure activities'):
        point = 2.5
      elif (topic == 'books and literature') or (topic == 'arts') or (topic=='media') or (topic =='news, lifestyles and current affairs') or (topic == 'film'):
        point = 4
      elif (topic == 'scientific developments') or (topic == 'technical and legal'):
        point = 5
      else:
        point = 0
      points.append(point)
    level_topic = round_num(sum(points)/len(points))
    return level_topic
  except Exception:
    pass

def _lang_level(text):
  try:
    #tokenization and lemmatization of the input text
    sentence_words = word_tokenize(text)
    wordnet_lemmatizer = WordNetLemmatizer()
    lemmas =[]
    punctuations = "?:!.,;"
    for word in sentence_words:
      if word in punctuations:
        sentence_words.remove(word)
      lemma = wordnet_lemmatizer.lemmatize(word, pos="v")
      lemmas.append(lemma)
  except Exception:
    pass

#reading the vocabulary lists into the dictionary with key as the name of level
  dict_vocab = {}
  for filename in os.listdir("vocabulary lists"):
    if filename.endswith("vocabulary list.txt"):
      with open("vocabulary lists/" + filename, 'r') as d:
          dict_vocab[filename[:2]]=d.read().split('\n')

  for word in dict_vocab['C1']:
    word.lower()

  #st.write(dict_vocab)
  set_A1 = set(dict_vocab['A1'])
  set_A2 = set(dict_vocab['A2']).difference(set_A1)
  set_B1 = set( dict_vocab['B1'] ).difference(set_A1)
  set_B1 = set_B1.difference(set_A2)
  set_B2 = set(dict_vocab['B2']).difference(set_B1)
  set_C1 = set(dict_vocab['C1']).difference(set_B2)
  set_C2 = set( dict_vocab['C2'] ).difference(set_C1)
  vocab_lists_sets =[set_A1,set_A2,set_B1,set_B2,set_C1,set_C2]

#count lexical density for each level
  set_essay = set(lemmas)
  words_found = []
  words_counts = []
  for i in range(0, len(vocab_lists_sets)):
    words_from_dict = vocab_lists_sets[i].intersection(set_essay)
    words_found.append(words_from_dict)

  for i in range(0, len(words_found)):
    word_count = len(words_found[i])
    words_counts.append(word_count)

  total_count = len(lemmas)
  lex_dens_list = []
  for i in range(0, len(words_counts)):
    lex_density = round((words_counts[i]/total_count) * 100, 2)
    lex_dens_list.append(lex_density)
  return lex_dens_list, words_found

#calculate lexical density
def lex_dens_level(text):
  lex_dens_list,words_found =_lang_level(text)
  indices, L_sorted = zip(*sorted(enumerate(lex_dens_list), key=itemgetter(1)))
  level_ld = (indices[0]+indices[1])/2
  return level_ld

def write_lex_density(text):
  try:
    level_ld = lex_dens_level(text)
    level_topic = topic_level(text)


    if level_topic > 0:
      level_av = round_num((level_ld + level_topic)/2)
    else:
      level_av = round_num(level_ld)

    lex_dens_list,words_found = _lang_level(text)
    st.write('Based on your topic and vocabulary complexity, your level of English is {level_av}.'.format(level_av=level_av))
    for i in range (0,len(lex_dens_list)):
      st.write('Percentage of words from level {num} in your text is: {lex_density}%  Words you used: {words}'.format(num = i+1, lex_density=lex_dens_list[i], words =  list(words_found[i])))
      i +=1

  except Exception:
    pass
