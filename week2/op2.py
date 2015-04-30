#!/usr/bin/python

import nltk
from nltk.tag.stanford import NERTagger

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

    # Tag the file
    taggedFile = st.tag(file.split())

    # Count the tags
    for list in taggedFile:
        print("There are " + getLengthTags(list, 'LOCATION') + " locations.")
        print("There are " + getLengthTags(list, 'PERSON') + " persons.")
        print("There are " + getLengthTags(list, 'ORGANIZATION') + " organizations.")

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

    print(conllTaggedFile)
    print(mucTaggedFile)

    #########################
    ########## END ##########
    #########################

    ########################
    ### BEGIN EXERCISE 3 ###
    ########################

if __name__ == "__main__":
    main()