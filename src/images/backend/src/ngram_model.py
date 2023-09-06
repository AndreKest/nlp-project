# N-Gramm Modellklasse 
# Basiert auf dem Notebook von: https://github.com/openlegaldata/oldp-notebooks/blob/master/notebooks/ngram_model.ipynb
import collections
import pickle
import os

import numpy as np
import spacy

np.random.seed(42)

class Corpus:
    """ Erzeugt den Corpus zum trainieren der N-Gramme. """
    def __init__(self, lst_Text, test_percentage=0.1):
        """ Erstellt eine Liste von Sätzen und eine Liste mit allen vorkommenden Wörtern aus den Daten. """
        self.test_percentage = test_percentage
        self.lst_Text = lst_Text
        self.lst_doc = []
        
        self.lst_sentences = []
        
        # use spacy NLP to do the tokenization and sentence boundary detection
        nlp = spacy.load('de_core_news_lg')
        
        cnt = 0
        for i, text in enumerate(self.lst_Text):
            # Ausgabe für Debugging 
            if cnt == 1000:
                print(i)
                cnt = 0
            # Spacy NLP Pipeline kann nur Texte mit maximal 1000000 Wörten verarbeiten
            # Überspringt Texte, die Länger sind
            if len(text) > 1000000:
                print("greater 1000000")
                continue
            
            doc = nlp(text)

            self.create_sentences(doc)
            self.create_words(doc)
            
            cnt += 1
      
        # Um die N-Gramme anschließend zu erzeugen, werden die Sätze
        # und das Alphabet wieder eingelesen und in der Corpus Klasse abgespeichert
        with open("/home/9cce/NLP/src/ngram"+"/ngram_3_sentences.txt", 'r') as f:
            for line in f:
                lst_sentence = []
                for word in line.split():
                    lst_sentence.append(word)
                self.lst_sentences.append(lst_sentence)

        with open("/home/9cce/NLP/src/ngram"+"/ngram_3_tokens.txt", 'r') as f:
            self.lst_tokens = [line.strip() for line in f]
            
                

    def get_words(self):
        """ Return: Die Wörter """
        for token in self.lst_tokens:
            yield token
    
    def get_sentences(self, test=False):
        """ Return: Die Sätze """
        for sent in self.lst_sentences:
            # split into training and test sentences, according to the given percentage
            if (np.random.random() >= self.test_percentage and not test) or \
               (np.random.random() < self.test_percentage and test):
                yield sent
        
                
    def get_ngrams(self, n, test=False):
        """ Bestimmt die N-Gramme. """
        for sent in self.get_sentences(test=test):
            if len(sent) < 10:
                continue
            for pos in range(len(sent)):
                if len(sent)-pos < n:
                    break
                yield (*[sent[pos+i] for i in range(n)],)

    def create_sentences(self, doc):
        """ Erstellt eine Liste von Sätzen und speichert diese ab. Das abspeichern ist nötig, da es sonst zu einem zu großen Ressourcen
        Verbrauch kommt.  """
        
        # Erstellt eine Liste von Sätzen
        lst_sentences = []
        for sent in doc.sents:
            lst_token_tmp = [token.text for token in sent]
            lst_sentences.append(lst_token_tmp)
        
        # Schreibt die erstellten Sätze in die Datei mit den schon erzeugten Sätzen (hängt am Ende der Datei an)
        with open("/home/9cce/NLP/src/ngram"+"/ngram_3_sentences.txt", 'a') as f:
            for sentence in lst_sentences:
                for word in sentence:
                    f.write(word+' ')
                f.write('\n')
        
        
    def create_words(self, doc):
        """ Erstellt eine Wortliste basierend auf allen in den Texten vorkommenden Wörten. Das Lesen und Schreiben der Liste ist nötig,
        da es sonst zu einem zu großen Ressourcen Verbrauch des PCs kommt. """
        
        # Erstellt eine Liste von Tokens (Wörtern)
        lst_tokens = []
        tmp = []
        for token in doc:
            lst_tokens.append(token.text)

        # Liest das schon bekannte Alphabet ein
        if os.path.exists("/home/9cce/NLP/src/ngram"+"/ngram_3_tokens.txt") == True:
            with open("/home/9cce/NLP/src/ngram"+"/ngram_3_tokens.txt", 'r') as f:
                tmp = [line.strip() for line in f]
        
        # Hängt die Wörter des neuen Dokuments an die bestehenden an
        # Wandelt die Liste in eine Menge um, da in einem Alphabet kein Wort zweimal vorkommt
        lst_tokens.extend(tmp)
        lst_tokens = set(lst_tokens)

        # Schreibt das neue Alphabet 
        with open("/home/9cce/NLP/src/ngram"+"/ngram_3_tokens.txt", 'w') as f:
            for tok in lst_tokens:
                f.write(tok+'\n')


class NgramModel:
    """ Erzeugt das N-Gramm Modell. """
    
    def __init__(self, nlp, n=3):
        self.n = n
        self.ngrams = None
        self.alphabet = None
        self.nlp = nlp
    
    def learn(self, corpus):
        """ Startet das erzeugen der N-Gramme (Lernvorgang). """
        self.ngrams = collections.Counter(corpus.get_ngrams(self.n))
        self.alphabet = set(corpus.get_words())
        
    def predict(self, context):
        """ Ermittelt das am häufigst vorkommende N-Gramm. """    
        
        # Das N-Gramm muss mindestens die Länge n-1 sein
        if len(context) < self.n - 1:
            raise ValueError('The context has to be at least of length {}!'.format(self.n - 1))
        if len(context) >= self.n:
            context = context[-self.n + 1:]
            
        matches = {}
        # Hängt an die Eingabe (die n + 1 letzten Wörter der Eingabe) ein Wort aus dem bekannten Alphabet an und prüft,
        # ob das entstandene Konstrukt aus die letzten n+1 Wörter der Eingabe und ein Wort aus dem Alphabet in der Liste der N-Gramme
        # vorkommt und falls ja wie oft
        for word in self.alphabet:
            count = self.ngrams[tuple(context) + (word,)]
            if count > 0:
                matches[word] = count
        total_count = sum(matches.values(), 0.0)
        return {k: v / total_count for k, v in matches.items()}
    
    def predict_str(self, context_str):
        """ Tokensiert die Eingabe und ruft die self.predict() Funktion auf. 
        Falls schon eine Liste von Tokens übergeben wird, kann gleich die self.predict() Funktion
        aufgerufen werden. """
        context = [token.text for token in self.nlp(context_str)]
        return self.predict(context)

    def save_model(self):
        """ Speichert das entstandene Modell (N-Gramme und Alphabet) ab. """
        with open("/home/9cce/NLP/src/ngram"+"/ngram_"+str(self.n)+"_model.pickle", 'wb') as f:
            pickle.dump(self.ngrams, f)
        with open("/home/9cce/NLP/src/ngram"+"/alphabet_"+str(self.n)+"_model.pickle", 'wb') as f:
            pickle.dump(self.alphabet, f)

    def read_model(self):
        """ Liest das bereits trainierte Modell ein. """
        with open(os.path.dirname(__file__)+"/ngram/ngram_"+str(self.n)+"_model.pickle", 'rb') as f:
            self.ngrams = pickle.load(f)
        with open(os.path.dirname(__file__)+"/ngram/alphabet_"+str(self.n)+"_model.pickle", 'rb') as f:
            self.alphabet = pickle.load(f)
        return self