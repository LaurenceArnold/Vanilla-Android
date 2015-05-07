#!/usr/bin/python

import nltk
from nltk.tag.stanford import NERTagger
from nltk.corpus import wordnet
from nltk.collocations import *

def getLengthTags(listName, name):
    tags = [el for el in listName if el[1] == name]
    return str(len(tags))

def main():

    # Open file and ignore UTF-8 errors
    file = open('ada_lovelace.txt').read()
    file = unicode(file, errors='ignore')

    ########################
    ### BEGIN EXERCISE 1 ###
    ########################

    # Open NERTagger
    st = NERTagger('/Library/Python/2.7/site-packages/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz',
                   '/Library/Python/2.7/site-packages/stanford-ner-2014-06-16/stanford-ner-3.4.jar')
    """
    # Tag the file
    taggedFile = st.tag(file.split())

    # Count the tags
    for list in taggedFile:
        print("There are {} locations.".format(getLengthTags(list, 'LOCATION')))
        print("There are {} persons.".format(getLengthTags(list, 'PERSON')))
        print("There are {} organizations.".format(getLengthTags(list, 'ORGANIZATION')))

    #########################
    ########## END ##########
    #########################

    ########################
    ### BEGIN EXERCISE 2 ###
    ########################

    conll = NERTagger('/Library/Python/2.7/site-packages/stanford-ner-2014-06-16/classifiers/english.conll.4class.distsim.crf.ser.gz',
                   '/Library/Python/2.7/site-packages/stanford-ner-2014-06-16/stanford-ner-3.4.jar')
    muc = NERTagger('/Library/Python/2.7/site-packages/stanford-ner-2014-06-16/classifiers/english.muc.7class.distsim.crf.ser.gz',
                   '/Library/Python/2.7/site-packages/stanford-ner-2014-06-16/stanford-ner-3.4.jar')

    conllTaggedFile = conll.tag(file.split())
    mucTaggedFile = muc.tag(file.split())

    print("{}".format(conllTaggedFile))
    print("{}".format(mucTaggedFile))

    #########################
    ########## END ##########
    #########################
    """
    ########################
    ### BEGIN EXERCISE 3 ###
    ########################

    # Tokenize the text in the file
    tokenizedText = nltk.sent_tokenize(file)

    # POS-tag the tokenized text
    tokens = []
    for sent in tokenizedText:
        tokens += nltk.word_tokenize(sent)
    posTags = nltk.pos_tag(tokens)

    # Get nouns
    nouns = [word[0] for word in posTags if word[1] == 'NN']

    # Tag nouns
    taggedNouns = st.tag(nouns)

    # Print all tagged nouns with a string format
    for el in taggedNouns[0]:
        print("Noun is {} and tag is {}".format(el[0],el[1]))

if __name__ == "__main__":
    main()