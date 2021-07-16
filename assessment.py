import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from keras.models import Sequential
from keras import layers
from keras import regularizers
from keras import backend as K
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.metrics import classification_report
from keras import callbacks
import math
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import tensorflow as tf

df = pd.read_csv('WIDA assessment graded essays.csv')

df.columns = ['Text', 'Score']

def round_num(score):
  decimal = score - int(score)
  if decimal <= 0.5:
    return int(score)
  else:
    return int(score) + 1

df['Score'] = [round_num(score) for score in df['Score']]

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')

def text_prepare(text):
    text = text.lower() # lowercase text
    text = text.replace("\n", " ")
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub('', text) # delete symbols which are in BAD_SYMBOLS_RE from text
    text = text.strip()
    return text

X = df['Text'].values
Y = df['Score'].values

X = [text_prepare(x) for x in X]

Y_df = pd.DataFrame(columns = set(df['Score']) , index = range(len(df)))
for index,score in enumerate(list(df['Score'])):
  Y_df.loc[index, score] = 1
Y_df = Y_df.fillna(0)

X_train, X_test, Y_train, Y_test = train_test_split(X,Y_df, test_size = 0.2, random_state = 1145)

max_words = 10000
max_len = 200

tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(X_train)
sequences = tokenizer.texts_to_sequences(X_train)
X_train = pad_sequences(sequences, maxlen=max_len)

sequences = tokenizer.texts_to_sequences(X_test)
X_test = pad_sequences(sequences, maxlen=max_len)

model = Sequential()

model.add(layers.Embedding(max_words, 20))
model.add(layers.LSTM(10))
model.add(layers.Dense(6, activation = 'softmax'))

model.summary()

model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['accuracy','AUC'])

callback = [callbacks.EarlyStopping(patience = 2, restore_best_weights=True)]

a = model.fit(X_train, Y_train, epochs = 45, validation_data=(X_test,Y_test), callbacks=callback)

tf.keras.models.save_model('saved_model')

text_sample = "I thenk don Dog is bad. Dog want bath plei and swem I wan be a pelot kids fet becuse thei eat meny fast food thei like burgers and drenk cola I wan be halthee"

text_sample = text_prepare(text_sample)

sequences = tokenizer.texts_to_sequences([text_sample])
seq = pad_sequences(sequences, maxlen=max_len)
model.predict(seq)

X = df['Text'].values

Y = df['Score'].values

X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.2, random_state = 1145)

def tfidf_features(X_train, X_test):
    
    tfidf_vectorizer = TfidfVectorizer(token_pattern='(\S+)', min_df=5, max_df=0.9, ngram_range=(1,2))
    tfidf_vectorizer.fit(X_train)

    X_train = tfidf_vectorizer.transform(X_train)
    X_test = tfidf_vectorizer.transform(X_test)
    
    return X_train, X_test, tfidf_vectorizer

X_train_tfidf, X_test_tfidf, tfidf_vocab = tfidf_features(X_train, X_test)
tfidf_vocab = {i:word for word,i in tfidf_vocab.items()}

filename = open("assessment_vocabulary.pkl", "wb")
pickle.dump(tfidf_vocab, filename)
filename.close()

X_train, X_test, vocab = tfidf_features(X_train, X_test)

from sklearn.linear_model import LogisticRegression

def simple_logistic_classify(X_train, Y_train, X_test, Y_test, _C=1.0):
    model = LogisticRegression(C=_C).fit(X_train, Y_train)
    score = model.score(X_test, Y_test)
    print('Test Score with', 'features', score)
    return model

b = simple_logistic_classify(X_train, Y_train, X_test, Y_test)

pkl_filename = "assessment_level_model.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(classifier_tfidf, file)


tf_text = vocab.transform([text_sample])

b.predict(tf_text)
