import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
import spacy
from spacy import displacy
import os
import gensim
import ngram_model
import re


nlp = spacy.load('de_core_news_lg')

app = Flask(__name__)
app.config.from_object(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

# WordEmbeddings Initialisierung
modelWordEmbeddings = gensim.models.Word2Vec.load(os.path.dirname(__file__) + "/word2vec/word2vec_model.model")

# N-Gram Initialisierung
model = ngram_model.NgramModel(nlp, n=3)
model = model.read_model()

@app.route('/predict', methods=['POST'])
def predict():
    """
        Erstellender Autocomplete-Vorschläge mithilfe von N-Grammen und Word-Embeddings.
    """
    request_data = request.get_json()
    # Den ganzen Text verwenden
    # text = request_data["text"].strip()
    # Den Text bis zum letzten Leerzeichen verwenden
    text = " ".join(request_data["text"].split(" ")[:-1])
    suggestField = request_data["fieldType"]

    print(suggestField, flush=True)

    predictions = []
    dictPredictionProbabilities = {}
    # Welche Predictions sollen verwendet werden
    addWordEmbeddingPredictions = True
    addNGramPredictions = True

    # Vorschläge des WordEmbeddings
    if (addWordEmbeddingPredictions):
        suggestions = suggestWordEmbedding(text)
        # print(suggestions, flush=True)
        if suggestions != None:
            for word, probability in suggestions:
                dictPredictionProbabilities[word] = probability

    # Vorschläge N-Gram
    if (addNGramPredictions):
        suggestions = suggestNgram(text)
        # print(suggestions, flush=True)
        if suggestions != None:
            for word, probability in suggestions.items():
                dictPredictionProbabilities[word] = probability
    
    # Nach Wahrscheinlichkeit sortieren
    sortedByProbability = dict(sorted(dictPredictionProbabilities.items(), key=lambda item: item[1], reverse=True))

    # In die Ergebnisliste einfügen
    for word, probability in sortedByProbability.items():
        prediction = text + " " + word
        if prediction not in predictions:
            predictions.append(prediction)
    
    # Wenn keine Prediction erstellt wird, versuche stattdessen das
    # letzte Wort auszubessern (Spellchecker).
    if len(predictions) == 0:
        spellCorrections = spellChecker(request_data["text"], suggestField)
        for textCorrection in spellCorrections:
            predictions.append(textCorrection)

    return jsonify(predictions)

def suggestWordEmbedding(text):
    """
        Vorhersagen des nächsten Wortes mithilfe von WordEmbeddings.
    """
    # Preprocess input
    predictOn = text

    suggestions = gensim.utils.simple_preprocess(predictOn)
    suggestions = modelWordEmbeddings.predict_output_word(suggestions)

    return suggestions

def suggestNgram(text):
    """
        Vorhersagen des nächsten Wortes mithilfe von N-Grammen.
    """
    try:
        # create tokens from input
        autocompletion = [token.text for token in nlp(text)]

        # predict the next word
        d = model.predict(autocompletion)

        # take just the maximum
        sortedByProbability = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))

        return sortedByProbability
    except:
        return None

def spellChecker(text, field):
    """
        Sucht nach möglicher Autovervollständigung mithilfe von Solr.
    """
    print("no suggestion - use spellchecker", flush=True)
    suggestions = []
    word = text.split(" ")[-1]
    if word == None or word == "":
        return suggestions

    result = []
    solrSearch = "http://database:8983/solr/court-decisions/select"
    solrSearch += f"?q={field}:{word}*"
    # https://solr.apache.org/guide/6_6/highlighting.html
    solrSearch += f"&hl=true&hl.fl={field}&hl.fragsize=1&hl.encoder=html"
    solrSearch += "&hl.simple.pre=<suggestion>&hl.simple.post=<%2Fsuggestion>"
    result = requests.get(solrSearch)
    responseHl = result.json()["highlighting"]

    for id in responseHl:
        for textHl in responseHl[id][field]:
            textHl = re.search('<suggestion>(.*)</suggestion>', textHl).group(1)
            if textHl != None:
                textHl = textHl.rstrip(';')
                textHl = textHl.rstrip(',')
                textHl = textHl.rstrip('.')
                textHl = textHl.rstrip('!')
                textHl = textHl.rstrip('?')
                textHl = textHl.rstrip('"')
                textHl = textHl.rstrip('\'')
            suggestions.append(textHl)

    suggestions = list(set(suggestions))
    return suggestions

@app.route('/search/text', methods=['POST'])
def searchText():
    """
        Route die aufgerufen wird wenn eine Textsuche abgeschickt wird.
        Rückgabe der Suchergebnisse
    """
    request_data = request.get_json()
    text = request_data["text"]

    sentences = []
    result = []
    solrSearch = "http://database:8983/solr/court-decisions/select"
    solrSearch += f"?q=rawText:\"{text}\" OR rawText:*{text}*"
    # https://solr.apache.org/guide/6_6/highlighting.html
    solrSearch += "&hl=true&hl.fl=rawText&hl.fragsize=0&hl.encoder=html"
    solrSearch += "&hl.simple.pre=<strong>&hl.simple.post=<%2Fstrong>"
    solrSearch += "&start=" + str((int(request_data["currPage"]) - 1)*10)
    result = requests.get(solrSearch)
    response = result.json()["response"]
    responseHl = result.json()["highlighting"]

    for doc in response["docs"]:
        text = doc["rawText"]
        if doc["id"] in responseHl and len(responseHl[doc["id"]]) > 0:
            text = responseHl[doc["id"]]["rawText"][0]
            
        sentences.append({
            "id": doc["id"], 
            "docId": doc["docId"], 
            "sentenceNumber": doc["sentenceNumber"], 
            "rawText": doc["rawText"],
            "textFormatted": text
        })


    responseToSend = {
        "sentences": sentences,
        "numFound": response["numFound"]
    }

    return jsonify(responseToSend)

class QuintupleRecognition(object):
    def __init__(self):
        """
        """
    
    def handleChildren(self, quintuple, token):
        """
        Rekursive Behandlung der Kinder eines Tokens. Fügt jedes Element dem Quintupel hinzu.
        """
        for child in token.children:
            if child.dep_ == "sb" or child.dep_ == "oa" or child.dep_ == "da":
                if child.dep_ in quintuple.keys():
                    quintuple[child.dep_].append(child.text)
                else:
                    quintuple[child.dep_] = [child.text]
                
                quintuple = self.handleChildren(quintuple, child)

            elif child.dep_ == "cd": 
                quintuple['rest'].append(child.text)
                
                if token.dep_ in quintuple.keys():
                    quintuple[token.dep_] += [x.text for x in list(child.children)]
                else:
                    quintuple = self.handleChildren(quintuple, child)
                
            else:
                if child.dep_ != "dep":
                    quintuple['rest'].append(child.text)
                    quintuple = self.handleChildren(quintuple, child)
            
        return quintuple

    def createQuintuple(self, sentence):
        """
        Finden des ROOT-Elements eines Satzes und erstellen des Quintupels.
        """
        for token in sentence:
            if token.dep_ == "ROOT":
                quintuple = {
                    'ROOT': [],
                    'sb': [],
                    'rest': []
                }

                quintuple[token.dep_].append(token.text)
                quintuple = self.handleChildren(quintuple, token)

                return quintuple

@app.route('/search/fields', methods=['POST'])
def searchFields():
    """
        Route die aufgerufen wird wenn eine Feldersuche abgeschickt wird.
        Rückgabe der Suchergebnisse
    """
    request_data = request.get_json()

    sentences = []
    result = []
    solrSearch = f"http://database:8983/solr/court-decisions/select?q=*:*"
    for key in request_data.keys():   
        solrSearch += addQueryPart(key, request_data[key])

    # https://solr.apache.org/guide/6_6/highlighting.html
    solrSearch += "&hl=true&hl.fl=rawText&hl.fragsize=0&hl.encoder=html"
    solrSearch += "&hl.simple.pre=<strong>&hl.simple.post=<%2Fstrong>"
    solrSearch += "&start=" + str((int(request_data["currPage"]) - 1)*10)

    result = requests.get(solrSearch)
    response = result.json()["response"]
    responseHl = result.json()["highlighting"]

    for doc in response["docs"]:
        text = doc["rawText"]
        if doc["id"] in responseHl and len(responseHl[doc["id"]]) > 0:
            text = responseHl[doc["id"]]["rawText"][0]

        sentences.append({
            "id": doc["id"], 
            "docId": doc["docId"], 
            "sentenceNumber": doc["sentenceNumber"], 
            "rawText": doc["rawText"],
            "textFormatted": text
        })

    responseToSend = {
        "sentences": sentences,
        "numFound": response["numFound"]
    }

    return jsonify(responseToSend)


def addQueryPart(key, value):
    """
        Erstellt den Query für ein spezifisches Feld im Solr.
    """
    if (value == "" or value == None or key == "currPage"):
        return ""
    if isinstance(value, list):
        queryPart = ""
        for element in value:
            queryPart+=f" AND ({key}:\"{element}\" {key}:*{element}*)"
        return queryPart
    else:
        return f" AND ({key}:\"{value}\" {key}:*{value}*)"

@app.route('/search/sentence', methods=['POST'])
def searchSentence():
    """
        Route die aufgerufen wird wenn eine Struktursuche abgeschickt wird.
        Rückgabe der Suchergebnisse
    """
    request_data = request.get_json()
    text = request_data["text"]

    if text == "" or text == None:
        return jsonify(
            {
                "sentences": [],
                "numFound": 0
            }
        )

    document = nlp(text)
    recognition = QuintupleRecognition()

    quintuple = recognition.createQuintuple(list(document.sents)[0])

    quintuple["root"] = quintuple["ROOT"]
    quintuple["nsubj"] = quintuple["sb"]
    del quintuple["ROOT"]
    del quintuple["sb"]

    sentences = []
    result = []
    solrSearch = f"http://database:8983/solr/court-decisions/select?q=*:*"
    for key in quintuple.keys():   
        solrSearch += addQueryPart(key, quintuple[key])

    solrSearch += "&start=" + str((int(request_data["currPage"]) - 1)*10)

    result = requests.get(solrSearch)
    response = result.json()["response"]

    for doc in response["docs"]:
        sentences.append({
            "id": doc["id"], 
            "docId": doc["docId"], 
            "sentenceNumber": doc["sentenceNumber"], 
            "rawText": doc["rawText"],
            "textFormatted": doc["rawText"]
        })

    responseToSend = {
        "sentences": sentences,
        "numFound": response["numFound"]
    }

    return jsonify(responseToSend)

@app.route('/parse', methods=['GET'])
def parseSentence():
    """
        Reparsed einen Satz mithilfe von spaCy.
        Rückgabe des gerenderten Dependenzbaumes
    """
    query_params = request.args
    text = query_params['text']
    document = nlp(text)

    html = displacy.render(document, style="dep", page=True)

    return jsonify(html)

@app.route('/viewDoc', methods=['GET'])
def viewDoc():
    """
        Sucht nach den in Solr gespeicherten Sätzen des angegebenen Dokumentes.
    """
    query_params = request.args
    docId = query_params['docId']

    responseToSend = []
    result = []
    solrSearch = f"http://database:8983/solr/court-decisions/select?q=docId:" + docId
    solrSearch += f"&sort=sentenceNumber%20asc&rows=2147483647"

    result = requests.get(solrSearch)
    response = result.json()["response"]

    for doc in response["docs"]:
        responseToSend.append({
            "sentenceNumber": doc["sentenceNumber"], 
            "rawText": doc["rawText"]
        })

    return jsonify(responseToSend)