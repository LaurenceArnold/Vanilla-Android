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


def findAnimal(noun):
    synset1 = wordnet.synsets(noun, pos='n')
    if (isinstance(synset1, list)):
        synset1 = synset1[0]

    # Synsets to look for:
    animal = wordnet.synsets("animal", pos='n')[0]

    if (hypernymOf(synset1, animal)):
        return True

    return False

def findSport(noun):
    synset1 = wordnet.synsets(noun, pos='n')
    if (isinstance(synset1, list)):
        synset1 = synset1[0]

    # Synsets to look for:
    sport = wordnet.synsets("sport", pos='n')[0]

    if (hypernymOf(synset1, sport)):
        return True

    return False


def main():

    # Get the directory of the file
    directory = os.getcwd()

    # All declarations for variables here
    # List for the nouns
    # Need to be outside of the loop because of the list comprehension
    nounList = []
    taggedNouns = []

    # Open NERtagger
    #nerTaggerStanford = NERTagger('/Library/Python/2.7/site-packages/stanford-ner-2014-06-16/classifiers/english.all.3class.distsim.crf.ser.gz',
               #'/Library/Python/2.7/site-packages/stanford-ner-2014-06-16/stanford-ner-3.4.jar')


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

                        #if columns[4].startswith("N"):
                            #taggedNoun = nerTaggerStanford.tag(columns)
                            #columns.append(taggedNoun[0][3][1])

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


    """
    CitySyns = wordnet.synsets(str("Utrecht"), pos = 'n')
    #variabele getagd met LOC
    City2Syns = wordnet.synsets(str("New_York"), pos = 'n')
    CityResult = getMaxSim(CitySyns, City2Syns)
    #print(CityResult)

    CountrySyns = wordnet.synsets(str("Utrecht"), pos = 'n')
    #zelfde variabele getagd met LOC
    Country2Syns = wordnet.synsets(str("America"), pos = 'n')
    CountryResult= getMaxSim(CountrySyns, Country2Syns)
    #print(CountryResult)

    NPSyns = wordnet.synsets(str("lake"), pos = 'n')
    #zelfde variabele getagd met LOC
    NP2Syns = wordnet.synsets(str("ocean"), pos = 'n')
    result3= getMaxSim(NPSyns, NP2Syns)
    print(result3)

    NPSyns2 = wordnet.synsets(str("lake"), pos = 'n')
    #zelfde variabele getagd met LOC
    NP2Syns2 = wordnet.synsets(str("drive"), pos = 'n')
    result4= getMaxSim(CountrySyns, Country2Syns)
    print(result4)

    print(findAnimal("dog"))
    print(findSport("football"))

    #if result == "None":
        #dan is het een locatie, maar dan kunnen we dus niet als city of country taggen wat kut is

if __name__ == "__main__":
    main()



