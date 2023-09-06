import collections
import pickle
import os

import numpy as np
import spacy

from pysbd.utils import PySBDFactory


np.random.seed(42)

class Corpus:
    def __init__(self, lst_Text, test_percentage=0.1):
        self.test_percentage = test_percentage
        self.lst_Text = lst_Text
        self.lst_doc = []

        # append all court decisions as one text to create the spacy pipeline (token, sentence)
        # text = ""
        # for t in lst_Text:
        #     text += t
        
        # use spacy NLP to do the tokenization and sentence boundary detection
        nlp = spacy.load('de_core_news_lg')
        # @nlp.factory("pysbd_sentence_boundaries", default_config={"some_setting": True})
        # def create_my_component(nlp, name, some_setting):
        #     return PySBDFactory(nlp, language='de')
        # add as a spacy pipeline component
        # nlp.add_pipe('pysbd_sentence_boundaries', before='parser')
        
        for text in lst_Text:
            self.lst_doc.append(nlp(text))

    def get_words(self):
        for doc in self.lst_doc:
            for token in doc:
                yield token.text
    
    def get_sentences(self, test=False):
        for doc in self.lst_doc:
            for sent in doc.sents:
                # split into training and test sentences, according to the given percentage
                if (np.random.random() >= self.test_percentage and not test) or \
                    (np.random.random() < self.test_percentage and test):
                    yield sent
                
    def get_ngrams(self, n, test=False):
        for sent in self.get_sentences(test=test):
            if len(sent) < 10:
                continue
            for pos in range(len(sent)):
                if len(sent)-pos < n:
                    break
                yield (*[sent[pos+i].text for i in range(n)],)


class NgramModel:
    def __init__(self, n=3):
        self.n = n
        self.ngrams = None
        self.alphabet = None
    
    def learn(self, corpus):
        self.ngrams = collections.Counter(corpus.get_ngrams(self.n))
        self.alphabet = set(corpus.get_words())
        
    def predict(self, context):    
        if len(context) < self.n - 1:
            raise ValueError('The context has to be at least of length {}!'.format(self.n - 1))
        if len(context) >= self.n:
            context = context[-self.n + 1:]
            
        matches = {}
        for word in self.alphabet:
            count = self.ngrams[tuple(context) + (word,)]
            if count > 0:
                matches[word] = count
        total_count = sum(matches.values(), 0.0)
        return {k: v / total_count for k, v in matches.items()}
    
    def predict_str(self, context_str):
        nlp = spacy.load('de_core_news_lg')
        context = [token.text for token in nlp(context_str)]
        return self.predict(context)

    def save_model(self):
        with open(os.path.dirname(__file__)+"/ngram_"+str(self.n)+"_model.pickle", 'wb') as f:
            pickle.dump(self.ngrams, f)
        with open(os.path.dirname(__file__)+"/alphabet_"+str(self.n)+"_model.pickle", 'wb') as f:
            pickle.dump(self.alphabet, f)

    def read_model(self):
        with open(os.path.dirname(__file__)+"/ngram_"+str(self.n)+"_model.pickle", 'rb') as f:
            self.ngrams = pickle.load(f)
        with open(os.path.dirname(__file__)+"/alphabet_"+str(self.n)+"_model.pickle", 'rb') as f:
            self.alphabet = pickle.load(f)
        return self