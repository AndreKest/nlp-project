import spacy
from spacy.attrs import ORTH
from pysbd.utils import PySBDFactory

# Read text
f_input = open("Dataset_Content/CourtDecision_12327.txt", 'r')

text = f_input.read()

f_input.close()


nlp = spacy.load('de_core_news_lg')

@nlp.factory("pysbd_sentence_boundaries", default_config={"some_setting": True})
def create_my_component(nlp, name, some_setting):
     return PySBDFactory(nlp, language='de')

# add as a spacy pipeline component
nlp.add_pipe('pysbd_sentence_boundaries', before='parser')

# doc = nlp("Die hohe Kammer: \"der irgendwas.\"")
doc = nlp(text)
for sent in doc.sents:
    print(sent.text.strip(), "\n")
