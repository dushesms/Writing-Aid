import pandas as pd
from sklearn.model_selection import train_test_split
import re
from nltk.corpus import stopwords
import numpy as np
from scipy import sparse as sp_sparse
from collections import Counter
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.tree import DecisionTreeClassifier
import pickle
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import average_precision_score


df = pd.read_csv('topics eaquals.csv')

df_topic = df[["Tags", "Description"]]
df_topic['Text'] = df_topic['Description']


df_topic = df_topic.dropna().reset_index()

df_topic['Tags'] = [tag.split('\n') for tag in df_topic['Tags']]

df_topic = df_topic.reset_index(drop = True)

d = {}
for i in range(len(df_topic)):
  for j in df_topic.loc[i, 'Tags']:
    if j in d:
      d[j] += 1
    else:
      d[j] = 1

d_new = list({k: v for k, v in d.items() if v <= 30}.keys())

for i in range(len(df_topic)):

    for index, tag in enumerate(list(df_topic.loc[i,'Tags'])):
        if tag in d_new:
            df_topic.loc[i, 'Tags'][index] = 0
    #df_topic.loc[i,'Tags'] = [0 if j in d_new else j for j in df_topic.loc[i, 'Tags']]

for i in range(len(df_topic)):

    for index, tag in enumerate(list(df_topic.loc[i,'Tags'])):
        if tag in d_new:
            df_topic.loc[i, 'Tags'][index] = 0
    #df_topic.loc[i,'Tags'] = [0 if j in d_new else j for j in df_topic.loc[i, 'Tags']]

    k = 1
    while k:
        try:
            df_topic.loc[i, 'Tags'].remove(0)
        except:
            k = 0

for i in range(len(df_topic)):
  if len(df_topic.loc[i,'Tags']) == 0:
    df_topic = df_topic.drop(i)

X, Y = df_topic['Text'].values, df_topic['Tags'].values

df_topic = df_topic.reset_index(drop=True)

d_tags = {}
for i in range(len(df_topic)):
  for j in df_topic.loc[i, 'Tags']:
    if j in d_tags:
      d_tags[j] += 1
    else:
      d_tags[j] = 1

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
STOPWORDS = set(stopwords.words('english'))


def text_prepare(text):
    text = text.lower() # lowercase text
    text = text.replace("\n", " ")
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
    text =BAD_SYMBOLS_RE.sub('', text) # delete symbols which are in BAD_SYMBOLS_RE from text
    text = ' '.join([word for word in text.split() if word not in STOPWORDS]) # delete stopwors from text
    text = text.strip()
    return text

X = [text_prepare(x) for x in X]

X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.1, random_state = 1145)

tags_counts = {}
# Dictionary of all words from train corpus with their counts.
words_counts = {}

words_counts = Counter([word for line in X for word in line.split(' ')])
most_common_words = sorted(words_counts.items(), key=lambda x: x[1], reverse=True)

DICT_SIZE = 5000
WORDS_TO_INDEX = {p[0]:i for i,p in enumerate(most_common_words[:DICT_SIZE])}
INDEX_TO_WORDS = {WORDS_TO_INDEX[k]:k for k in WORDS_TO_INDEX}
ALL_WORDS = WORDS_TO_INDEX.keys()

def my_bag_of_words(text, words_to_index, dict_size):
    
    result_vector = np.zeros(dict_size)
    for word in text.split():
      if word in words_to_index:
        result_vector[words_to_index[word]]+=1
    return result_vector

X_train_mybag = sp_sparse.vstack([sp_sparse.csr_matrix(my_bag_of_words(text, WORDS_TO_INDEX, DICT_SIZE)) for text in X_train])
X_test_mybag = sp_sparse.vstack([sp_sparse.csr_matrix(my_bag_of_words(text, WORDS_TO_INDEX, DICT_SIZE)) for text in X_test])
print('X_train shape ', X_train_mybag.shape)
print('X_test shape ', X_test_mybag.shape)

def tfidf_features(X_train, X_test):
    
    tfidf_vectorizer = TfidfVectorizer(token_pattern='(\S+)', min_df=5, max_df=0.9, ngram_range=(1,2))
    tfidf_vectorizer.fit(X_train)

    X_train = tfidf_vectorizer.transform(X_train)
    X_test = tfidf_vectorizer.transform(X_test)
    
    return X_train, X_test, tfidf_vectorizer.vocabulary_

X_train_tfidf, X_test_tfidf, tfidf_vocab = tfidf_features(X_train, X_test)
tfidf_reversed_vocab = {i:word for word,i in tfidf_vocab.items()}

filename = open("topics_vocabulary.pkl", "wb")
pickle.dump(tfidf_vocab, filename)
filename.close()


"""Create the dictionary of tags and their counts. """


d_new_reversed = list({k: v for k, v in d.items() if v > 30}.keys())
mlb = MultiLabelBinarizer(classes=sorted(d_new_reversed))
y_train = mlb.fit_transform(Y_train)
y_test = mlb.fit_transform(Y_test)
pkl_filename = "binarizer.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(mlb, file)

def train_classifier(X_train, y_train,C=2.0,penalty='l2'):

    # Create and fit LogisticRegression wrapped into OneVsRestClassifier.
    lr = DecisionTreeClassifier()
    
    ovr = OneVsRestClassifier(lr)
    ovr.fit(X_train, y_train)
    return ovr

classifier_mybag = train_classifier(X_train_mybag, y_train)
classifier_tfidf = train_classifier(X_train_tfidf, y_train)

y_val_predicted_labels_tfidf = classifier_tfidf.predict(X_test_tfidf)
y_val_predicted_labels_mybag = classifier_mybag.predict(X_test_mybag)

y_val_pred_inversed = mlb.inverse_transform(y_val_predicted_labels_tfidf)
y_val_inversed = mlb.inverse_transform(y_test)
for i in range(15):
    print('Title:\t{}\nTrue labels:\t{}\nPredicted labels:\t{}\n\n'.format(
        X_test[i],
        ','.join(y_val_inversed[i]),
        ','.join(y_val_pred_inversed[i])
    ))

def print_evaluation_scores(y_val, predicted):
    accuracy=accuracy_score(y_val,predicted)
    f1_macro=f1_score(y_val,predicted,average='macro')
    f1_micro=f1_score(y_val,predicted,average='micro')
    f1_weighted=f1_score(y_val,predicted,average='weighted')
    precision_macro=average_precision_score(y_val,predicted,average='macro')
    precision_micro=average_precision_score(y_val,predicted,average='micro')
    precision_weighted=average_precision_score(y_val,predicted,average='weighted')
    print(accuracy)

print('Bag-of-words')
print_evaluation_scores(y_test, y_val_predicted_labels_mybag)
print('Tfidf')
print_evaluation_scores(y_test, y_val_predicted_labels_tfidf)


pkl_filename = "topic_recognition_model.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(classifier_tfidf, file)

