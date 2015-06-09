#!/usr/bin/python
import nltk
from nltk.collocations import *
from nltk.util import ngrams
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus.reader.wordnet import WordNetError
from pprint import pprint
import operator


lake = wordnet.synsets("book", pos='n')[0]
print(lake)
hyp = lambda s:s.hypernyms()
pprint(lake.tree(hyp))
