#!/usr/bin/python
import nltk
from nltk.collocations import *
from nltk.util import ngrams
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet

def hyponymOf(synset1, synset2):
    """ Returns True if synset2 is a hypernym of synset1, or if they are the same synset. Returns False otherwise. """
    if synset1 == synset2:
        return True
    for hyponym in synset1.hyponyms():
        if synset2 == hyponym:
            return True
        if hyponymOf(hyponym, synset2):
            return True
    return False

def main():

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

    allSynsets = []
    for word in result1:
        Synsets = wordnet.synsets(word)
        allSynsets.append(Synsets)
        #for synset in Synsets:
            #print(synset.name(), synset.definition())
    print("dit zijn alle synsets", allSynsets)

    relative = wordnet.synsets("relative", pos='n') # has got two synsets
    print("Dit is een relatief", relative)
    for synset in relative:
        print(synset.name(), synset.definition())
    science = wordnet.synsets("science", pos='n') #has got two synsets
    for synset in science:
        print(synset.name(), synset.definition())
    illness = wordnet.synsets("illness", pos='n')
    for synset in illness:
        print(synset.name(), synset.definition()) #has one synset

    # so now compare the hyponyms of AllSynsets to the synsets of the above three or something






if __name__ == "__main__":
    main()

