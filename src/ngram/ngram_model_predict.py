import glob
import re
import collections

import spacy

import ngram_model

def suggest(text):
    try:
        model = ngram_model.NgramModel(n=3)
        model = model.read_model()
        d = model.predict_str(text)
        pred_next_word = max(d.keys(), key=lambda key: d[key])
    except:
        pred_next_word = None

    return pred_next_word

if __name__ == '__main__':
    # text = input("Input: ")
    text = "Es ergeben sich aus der Akte auch keinerlei Anhaltspunkte dafür, dass der Beschwerdeführerin"
    pred_next_word = suggest(text)
    print(pred_next_word)
