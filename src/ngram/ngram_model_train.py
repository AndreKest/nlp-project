# train the ngram model
# ----------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------#
import glob
import re
import collections

import spacy

import ngram_model

# preprocessing the data
def remove_whitespace(content):
    content = re.sub(r'( |\xa0)+', ' ', content)
    return '\n'.join([s for s in content.splitlines() if s.strip()])


def remove_pattern(content, regex, replace_with=''):
    pattern = re.compile(regex)
    while True:
        m = re.search(pattern, content)
        if m is None:
            break
        content = content[:m.start(0)] + replace_with + content[m.end(0):]
    return content

def clean(content):
    tmp = []
    for c in content:
        c = remove_pattern(c, r'\n|\t', replace_with=' ')
        c = remove_pattern(c, r'<[^>]+>')
        c = remove_whitespace(c)
        tmp.append(c)
    return tmp


# ----------------------------------------------------------------------------------#
# ----------------------------------------------------------------------------------#
# path
PATH_DATA = "./tmp"
PATH_MODEL = "./src/ngram"


# ----------------------------------------------------------------------------------#
# input the data
LIST_DATA = glob.glob(PATH_DATA+"/*.txt")
lst_Text = []
for data in LIST_DATA:
    with open(data, mode='r', encoding='UTF-8') as f:
        lst_Text.append(f.read())

lst_Text = clean(lst_Text)


# ----------------------------------------------------------------------------------#
# create the corpus from the data
corpus = ngram_model.Corpus(lst_Text)

# ----------------------------------------------------------------------------------#
# train the ngram model
model = ngram_model.NgramModel(n=3)
model.learn(corpus)

# ----------------------------------------------------------------------------------#
# save the trained model
model.save_model()