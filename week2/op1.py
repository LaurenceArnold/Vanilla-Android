#!/usr/bin/python
import nltk
from nltk.collocations import *
from nltk.util import ngrams
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet

text = open('ada_lovelace.txt').read()
source = text.decode("utf-8")
sents = nltk.sent_tokenize(source)
lemmatizer = WordNetLemmatizer()

tokens = []
for sent in sents:
    tokens += nltk.word_tokenize(sent)
pos_tags = nltk.pos_tag(tokens)
verbs = [word[0] for word in pos_tags if word[1] == 'VB' or word[1] == 'VBD' or word[1] == 'VBG' or word[1] == 'VBN' or word[1] =='VBP' or word[1] =='VBZ']

result1 = []
for word in verbs:
    result = lemmatizer.lemmatize(word, wordnet.VERB )
    result1.append(result)

print(result1)