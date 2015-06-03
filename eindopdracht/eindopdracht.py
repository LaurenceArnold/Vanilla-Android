#!/usr/bin/python

import os
import nltk
from nltk.corpus import wordnet
from nltk.wsd import lesk
from nltk.tag.stanford import NERTagger

def getMaxSim(synsets1, synsets2):
    """ From slides """
    # assignment 1.3

    maxSim = None
    for syn1 in synsets1:
        for syn2 in synsets2:
            sim = syn1.lch_similarity(syn2)
            if ((maxSim == None) or (maxSim < sim)):
                maxSim = sim

    return maxSim

def main():

    # Get the directory of the file
    directory = os.getcwd()

    # All declarations for variables here
    # List for the nouns
    # Need to be outside of the loop because of the list comprehension
    nounList = []
    taggedNouns = []

    # Open NERtagger
    nerTaggerStanford = NERTagger('/Library/Python/2.7/site-packages/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz',
               '/Library/Python/2.7/site-packages/stanford-ner-2014-06-16/stanford-ner-3.4.jar')


    # Loop through maps
    for root, dirs, filenames in os.walk(directory):

        # Loop through files
        for file in filenames:

            # Check if the file is en.tok.off
            if file == "en.tok.off.pos":

                # Open file
                with open(root+'/'+file, 'r') as in_f:

                    # Loop through lines of file
                    for line in in_f:

                        # Get tokens and append to list
                        columns = line.split()

                        if columns[4].startswith == "N":
                            nerTaggerStanford.tag(columns[3])

                        newLine = ' '.join(columns)

                        print(newLine)

                        """
                        # Write results to new file
                        with open(root+'/en.tok.off.pos.ent', 'a') as posfile:
                            posfile.write(newLine + '\n')
                        """

    """
    # eerst standaard entity tagger laten runnen op de inputfiles
    # daarna de rest handmatig laten taggen via Wordnet & hypernyms

    wordSyns = wordnet.synsets(str(word), pos = 'n')
    word2Syns = wordnet.sysnets(str(word2), pos = 'n')
    result = getMaxSim(wordSyns, Word2Syns)
    """

if __name__ == "__main__":
    main()



