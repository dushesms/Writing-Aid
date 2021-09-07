"""
Grade prediction
with the use of lstm model trained on the Hewlett-Packard dataset that returns the grade from 0-100% which is then converted to letter grade (A-F)
glove.6B.200d embeddings are used
"""
import numpy as np
import nltk
import re
from nltk.corpus import stopwords
import math
import keras

lstm_model = keras.models.load_model("good_model_scoring.h5")

def essay_to_wordlist(essay_v, remove_stopwords):
    """Remove the tagged labels and word tokenize the sentence."""
    essay_v = re.sub("[^a-zA-Z]", " ", essay_v)
    words = essay_v.lower().split()
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]
    return words

def essay_to_sentences(essay_v, remove_stopwords):
    """Sentence tokenize the essay and call essay_to_wordlist() for word tokenization."""
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    raw_sentences = tokenizer.tokenize(essay_v.strip())
    sentences = []
    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0:
            sentences.append(essay_to_wordlist(raw_sentence, remove_stopwords))
    return sentences

def makeFeatureVec(words, model, num_features):
    """Make Feature Vector from the words list of an Essay."""
    featureVec = np.zeros((num_features,),dtype="float32")
    num_words = 0.
    # index2word_set = set(model.wv.index2word)
    for word in words:
        if word in model:
            num_words += 1
            featureVec = np.add(featureVec, model[word])
    featureVec = np.divide(featureVec,num_words)
    return featureVec

def getAvgFeatureVecs(essays, model, num_features):
    """Main function to generate the word vectors for word2vec model."""
    counter = 0
    essayFeatureVecs = np.zeros((len(essays),num_features),dtype="float32")
    for essay in essays:
        essayFeatureVecs[counter] = makeFeatureVec(essay, model, num_features)
        counter = counter + 1
    return essayFeatureVecs

def text_predict(text):
    try:
        embedding_dict={}
        with open('glove.6B.200d.txt','r') as f:
            for line in f:
                values = line.split()
                word = values[0]
                vectors = np.asarray(values[1:],'float32')
                embedding_dict[word] = vectors
        model = embedding_dict
        if len(text) > 20:
            num_features = 200
            clean_test_essays = []
            clean_test_essays.append( essay_to_wordlist(text, remove_stopwords=True ) )
            testDataVecs = getAvgFeatureVecs( clean_test_essays, model, num_features )
            testDataVecs = np.array(testDataVecs)
            testDataVecs = np.reshape(testDataVecs, (testDataVecs.shape[0], 1, testDataVecs.shape[1]))

            preds = lstm_model.predict(testDataVecs)
            preds = list(preds)[0][0]

            if math.isnan(preds):
                preds = 0
            else:
                preds = np.round( preds )

            if preds < 0:
                preds = 0
        else:
            preds = 0

        preds = int(preds)
        return preds
    except Exception:
        pass

def grade_converter(preds):
    if preds >= 93:
        grade = 'A+'
    elif preds <= 92 and preds >= 85:
        grade = 'A'
    elif preds <= 84 and preds >= 75:
        grade = 'B'
    elif preds <= 74 and preds >= 70:
        grade = 'B'
    elif preds <= 69 and preds >= 65:
        grade = 'C+'
    elif preds <= 64 and preds >= 60:
        grade = 'C'
    elif preds <= 59 and preds >= 55:
        grade = 'D+'
    elif preds <= 54 and preds >= 50:
        grade = 'D'
    else:
        grade = 'F'
    return grade