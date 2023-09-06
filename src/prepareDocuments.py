import gzip
import shutil
import json
import os
import spacy
from bs4 import BeautifulSoup
from spacy import displacy
from spacy.attrs import ORTH, NORM
from pysbd.utils import PySBDFactory
from pathlib import Path

# Eigene Bibliotheken
from lib.utils import QuintupleRecognition, QuintupleXmlParser

print("Start...")

####################################
# Konstanten
####################################
DIR_DATA = "../data/"
DIR_TMP = "../tmp/"
DIR_DB = "../src/images/solr/import-data/data/" # Speicherplatz der konvertierten XML-Dateien
CHARACTER_ENCODING = "UTF-8"
FILE = "top1000.json"
AMOUNT_OF_FILES = 1000

####################################
# Tempverzeichnis bereinigen
####################################
files = [file for file in os.listdir(DIR_TMP) if not file.endswith(".gitkeep")]
for file in files:
    os.remove(os.path.join(DIR_TMP, file))

####################################
# Parser initialisieren
####################################
print("Parser initialisieren")
parser = QuintupleXmlParser()
recognition = QuintupleRecognition()

####################################
# Entpacken des gezipten Gerichtsurteil-Archives
# in das tmp Verzeichnis zur weiteren Verarbeitung
####################################
print("Entpacken")
with gzip.open(os.path.join(DIR_DATA, FILE + ".gz"), 'rb') as f_in:
    with open(os.path.join(DIR_TMP, FILE), 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

####################################
# Nach </span> wird ein Leerzeichen eingefügt, damit
# in der späteren Bearbeitung beide Inhalte voneinander
# getrennt erkannt werden können.
#
# Beispiel:
#   <span>Hallo Welt!</span>Wie geht es dir
#   => 
#   <span>Hallo Welt!</span> Wie geht es dir
####################################
def addWhitespacesAfterEverySpanTag(soup):
    for index in soup.find_all('span'):
        index.append(" ")
    return soup

####################################
# Die einzelnen Gerichtsurteile werden ausgelesen (JSON-Format)
# und mit dem passenden Encoding zu einzelnen
# Textdateien konvertiert.
####################################
print("Gerichtsurteile auslesen")
with open(os.path.join(DIR_TMP, FILE), mode="r", encoding=CHARACTER_ENCODING) as f:
    for _ in range(AMOUNT_OF_FILES):
        line = f.readline()
        parsed_line = json.loads(line)

        id = parsed_line["id"]
        content = parsed_line["content"]

        soup = BeautifulSoup(content, "lxml")

        soup = addWhitespacesAfterEverySpanTag(soup)

        fwrite = open(os.path.join(DIR_TMP, str(id) + ".txt"), "w", encoding=CHARACTER_ENCODING)
        fwrite.write(soup.text)
        fwrite.close()

####################################
# Laden des spaCy-Models
####################################
nlp = spacy.load('de_core_news_lg')

####################################
# Behandelt die korrekte Trennung in Sätze trotz Abkürzungen.
# Dazu wird zusätzlich eine Liste vorhandener Abkürzungen verwendet,
# die manuell hinzugefügt worden ist.
#
# Erstellt durch:
# - TODO: 
####################################
@nlp.factory("pysbd", default_config={"language": 'de'})
def createPySBDFactory(nlp, name, language):
    return PySBDFactory(nlp, language)

nlp.add_pipe('pysbd', before='parser')

####################################
# Generiert aus den einzelnen Sätzen jedes Gerichtsdokuments
# eine XML-Datei, die in Solr importiert werden kann.
####################################
def pipelineFile(directory, file, encoding):    
    with open(os.path.join(directory, file), mode="r", encoding=encoding) as f:
        content = f.read()
        if (len(content) > 1000000):
            # SpaCy unterstützt die Ausführung von sehr großen Dokumenten nicht.
            # Statt das Dokument nicht in die Datenbank hinzuzufügen, könnte man
            # auch das Limit erhöhen.
            # Wir haben uns hier dazu entschlossen, das nicht zu tun.
            # Wenn man es doch tun möchte:
            # nlp = spacy.load('de_core_news_lg') 
            # nlp.max_length = 2000000 # Oder größer, vergrößert den RAM-Bedarf
            print("--- Dokument zu groß: " + file)
            return
        
        document = nlp(content)
        filename = Path(f.name).stem

        preparedDocumentSentenceFields = []

        for index, sentence in enumerate(document.sents):
            quintuple = recognition.createQuintuple(sentence)
            if (quintuple is not None):    
                documentField = parser.generateXmlSingleSentence(filename, str(index), sentence.text.strip(), quintuple)
                # Die docs werden gesammelt
                preparedDocumentSentenceFields.append(documentField)
        # Die Quintupel-Docs werden in eine Datei geschrieben
        path = os.path.join(DIR_DB, f"data_document_{filename}_sentences.xml")
        parser.writeXmlFile(preparedDocumentSentenceFields, path, 'utf8')

####################################
# Die Pipeline für alle Textdokumente
# im Tempverzeichnis starten.
####################################
print("Pipeline gestartet")
index = 1
for file in os.listdir(DIR_TMP):
    if file.endswith(".txt"):
        print(str(index) + "/" + str(AMOUNT_OF_FILES) + " - " + file)
        index = index + 1
        pipelineFile(DIR_TMP, file, CHARACTER_ENCODING)

