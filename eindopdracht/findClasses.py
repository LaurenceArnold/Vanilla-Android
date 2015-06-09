#!/usr/bin/python
import nltk
from nltk.collocations import *
from nltk.util import ngrams
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.corpus.reader.wordnet import WordNetError
import operator


def hypernymOf(synset1, synset2):
    """ True als synset2 een hypernym is van synset1 (of dezelfde synset)"""
    if (synset1 == synset2):
        return True
    for hypernym in synset1.hypernyms():
        if (synset2 == hypernym):
            return True
        if (hypernymOf(hypernym, synset2)):
            return True

    return False


def isAnimal(noun):
    synset1 = wordnet.synsets(noun, pos='n')
    if (isinstance(synset1, list)):
        synset1 = synset1[0]
        
    # Synsets to look for:
    animal = wordnet.synsets("animal", pos='n')[0]
    
    if (hypernymOf(synset1, animal)):
        return True

    return False

def isSport(noun):
    synset1 = wordnet.synsets(noun, pos='n')
    if (isinstance(synset1, list)):
        synset1 = synset1[0]
        
    # Synsets to look for:
    sport = wordnet.synsets("sport", pos='n')[0]
    
    if (hypernymOf(synset1, sport)):
        return True

    return False

def isNatural(noun):
    naturalList = ["volcano", "river", "forest", "ocean", "water", "lake",
    "mountain", "hill", "sea", "woods", "island", "islands", "sea"]
    
    # Get wikipedia content
    wiki = wikipedia.page(noun)
    # Get first sentence
    firstSentence = wiki.content.split(".")[0]
    
    for word in firstSentence:
        for item in naturalList:
            if (word.lower() == item.lower()):
                return True
    
    return False
    
def isEntertainment(noun):
    entertainmentList = ["newspaper", "television", "radio", "magazine",
    "show", "musical", "song", "album", "tv", "Netflix"]
    
    # Get wikipedia content
    wiki = wikipedia.page(noun)
    # Get first sentence
    firstSentence = wiki.content.split(".")[0]
    
    for word in firstSentence:
        for item in entertainmentList:
            if (word.lower() == item.lower()):
                return True
    
    return False

if __name__ == "__main__":
    print(isAnimal("dog"))
    print(isSport("football"))

