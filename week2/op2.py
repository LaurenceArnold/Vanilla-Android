#!/usr/bin/python

import nltk
from nltk.tag.stanford import NERTagger

def getLengthTags(listName, name):
    tags = [el for el in listName if el[1] == name]
    return str(len(tags))

def main():


    # Open NERTagger
    st = NERTagger('/Library/Python/2.7/site-packages/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz',
                   '/Library/Python/2.7/site-packages/stanford-ner-2014-06-16/stanford-ner-3.4.jar')

    # Open file and ignore UTF-8 errors
    file = open('ada_lovelace.txt').read()
    file = unicode(file, errors='ignore')

    ########################
    ### BEGIN EXERCISE 1 ###
    ########################

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


if __name__ == "__main__":
    main()