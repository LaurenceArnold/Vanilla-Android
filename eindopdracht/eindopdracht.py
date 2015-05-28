#!/usr/bin/python

import nltk
from nltk.corpus import wordnet
from nltk.wsd import lesk
from nltk.tag.stanford import NERTagger


def main():

    # Get the directory of the file
    directory = os.getcwd()

    # All declaretions for variables here
    # List for the nouns
    # Need to be outside of the loop because of the list comprehesion
    nounList = []
    taggedNouns = []

    # Loop through maps
    for root, dirs, filenames in os.walk(directory):

        # Loop trough files
        for file in filenames:

            # Check if the file is en.tok.off
            if file == "en.tok.off.pos.ent":

                # Open file
                with open(root+'/'+file, 'r') as in_f:

                    # Loop through lines of file
                    for line in in_f:

                        # Get tokens and append to list
                        columns = line.split()
                        token = columns[4]
                        nounList.append(token)

    nouns = [tag for tag in nounList if tag.startswith("N")]

    # MUC NER tagger
    muc = NERTagger('/Library/Python/2.7/site-packages/stanford-ner-2014-06-16/classifiers/english.muc.7class.distsim.crf.ser.gz',
                   '/Library/Python/2.7/site-packages/stanford-ner-2014-06-16/stanford-ner-3.4.jar')

    # Tag all the nouns
    muc.tag(nouns)



    # eerst standaard entity tagger laten runnen op de inputfiles
    # daarna de rest handmatig laten taggen via Wordnet & hypernyms




if __name__ == "__main__":
    main()



