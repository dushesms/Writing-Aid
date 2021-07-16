from tensorflow import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import re

model = keras.models.load_model('saved_model')
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy', 'AUC'])

REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
def text_prepare(text):
    text = text.lower() # lowercase text
    text = text.replace("\n", " ")
    text = REPLACE_BY_SPACE_RE.sub(' ', text) # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = BAD_SYMBOLS_RE.sub('', text) # delete symbols which are in BAD_SYMBOLS_RE from text
    text = text.strip()
    return text

def predict(text):
    max_len = 200
    text_sample = text_prepare(text)
    tokenizer = Tokenizer()
    sequences = tokenizer.texts_to_sequences([text_sample])
    seq = pad_sequences( sequences, maxlen=max_len )
    prediction = model.predict(seq)
    list_predictions = prediction[0]
    if list_predictions[0] == max(list_predictions):
        level = '1'
    elif list_predictions[1] == max(list_predictions):
        level = '2'
    elif list_predictions[2] == max( list_predictions ):
        level = '3'
    elif list_predictions[3] == max( list_predictions ):
        level = '4'
    elif list_predictions[4] == max( list_predictions ):
        level = '5'
    elif list_predictions[5] == max( list_predictions ):
        level = '6'
    return level