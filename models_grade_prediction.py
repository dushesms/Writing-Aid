from gensim.models import KeyedVectors
from nltk.corpus import stopwords
import numpy as np
import keras
import predict_grade

#predictions based on the lstm model trained on HP dataset for 10 and 12 as a maximum grade.
#Word2vec embedding is used
model_10 = keras.models.load_model("final_lstm.h5")
model_12 = keras.models.load_model("final_lstm_12.h5")

def essay_to_wordlist(essay_v, remove_stopwords):
    words = essay_v.lower().split()
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]
    return (words)

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
    index2word_set = set(model.wv.index2word)
    for word in words:
        if word in index2word_set:
            num_words += 1
            featureVec = np.add(featureVec,model[word])
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

#all predictions combined and average is calculated
def predict_level(text):
    num_features = 300
    model = KeyedVectors.load_word2vec_format( "word2vecmodel.bin", binary=True )
    clean_test_essays = []
    clean_test_essays.append( essay_to_wordlist( text, remove_stopwords=True ) )
    testDataVecs = getAvgFeatureVecs( clean_test_essays, model, num_features )
    testDataVecs = np.array(testDataVecs)
    testDataVecs = np.reshape( testDataVecs, (testDataVecs.shape[0], 1, testDataVecs.shape[1]) )


    preds_1 = int(np.around(model_10.predict(testDataVecs)))
    preds_2 = int(np.around(model_12.predict(testDataVecs)))
    preds_3 = predict_grade.text_predict(text)/16.66
    preds = round((preds_1+preds_2+preds_3)/3)

    return preds



