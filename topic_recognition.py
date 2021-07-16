import pickle
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

from sklearn.multiclass import OneVsRestClassifier

topic_classifier: OneVsRestClassifier = pickle.load( open( "topic_recognition_model.pkl", "rb" ) )
vocab = pickle.load( open( "topics_vocabulary.pkl", "rb" ) )


def predict_topic(text):
    REPLACE_BY_SPACE_RE = re.compile( '[/(){}\[\]\|@,;]' )
    BAD_SYMBOLS_RE = re.compile( '[^0-9a-z #+_]' )
    STOPWORDS = set( stopwords.words( 'english' ) )

    text = text.lower()  # lowercase text
    text = text.replace( "\n", " " )
    text = REPLACE_BY_SPACE_RE.sub( ' ', text )  # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub( '', text )  # delete symbols which are in BAD_SYMBOLS_RE from text
    text = [word for word in text.split() if word not in STOPWORDS]  # delete stopwors from text
    tfidf_vectorizer = TfidfVectorizer(token_pattern='(\S+)', vocabulary=vocab)

    r = tfidf_vectorizer.fit_transform( text )
    prediction = topic_classifier.predict( r )
    mlb = pickle.load( open( "binarizer.pkl", "rb" ) )
    prediction = mlb.inverse_transform( prediction )
    prediction = list([i[0] for i in prediction if len(i) > 0])[:3]
    return ", ".join(prediction)

print(predict_topic("Do your business continues to wanting to work together and advance this project? Mark aren you currently working on some of biggest projects? What I learned about your company are very interesting, and I was happy to meets your employees your employees. Each of your employees were speaking very highly of they're career. it was good to hear some of the employees's opinions about your company. Lets collaborate together! There is many opportunities for us by working in partnership. Last year our company make 2354687$ in profit, we called it, 'our best year ever'. Afterward we expanded too three more countries. Everyday we work to improve our company to the extent possible, anybody will tell you we are always on the move.   Nothing is better than constant progress, we always works to advance because the new!"))
