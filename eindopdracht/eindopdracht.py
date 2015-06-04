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

def findCityorCountry(word):
    #If tag is location, loop through these lines

    CitySyns = wordnet.synsets(str(word), pos = 'n')
    City2Syns = wordnet.synsets(str("New_York"), pos = 'n')
    CityResult = getMaxSim(CitySyns, City2Syns)

    CountrySyns = wordnet.synsets(str(word), pos = 'n')
    Country2Syns = wordnet.synsets(str("America"), pos = 'n')
    CountryResult= getMaxSim(CountrySyns, Country2Syns)

    if CityResult > CountryResult:
        return "CIT"

    elif CountryResult > CityResult:
        return "COU"

    else:
        return "LOCATION"


def main():

    # Get the directory of the file
    directory = os.getcwd()

    # Open NERtagger
    nerTaggerStanford = NERTagger('/Library/Python/2.7/site-packages/stanford-ner-2014-06-16/classifiers/english.muc.7class.distsim.crf.ser.gz',
                   '/Library/Python/2.7/site-packages/stanford-ner-2014-06-16/stanford-ner-3.4.jar')


    # Loop through maps
    for root, dirs, filenames in os.walk(directory):

        # Loop through files
        for file in filenames:

            # Check if the file is en.tok.off
            if file == "en.tok.off.pos":

                # Open file
                with open(root+'/'+file, 'r') as in_f:

                    lineList = " "

                    # Loop through lines of file
                    for line in in_f:

                        # Get tokens and append to list
                        columns = line.split()

                        lineList += " " + str(columns[3])

                        """
                        # Write results to new file
                        with open(root+'/en.tok.off.pos.ent', 'a') as posfile:
                            posfile.write(newLine + '\n')
                        """

                    # Tag words with NER and append
                    tokenizedText = nltk.sent_tokenize(lineList)
                    taggedWords = nerTaggerStanford.tag(tokenizedText)

                    allTaggedWords = []

                    for el in taggedWords:
                        for word in el:
                            allTaggedWords.append(word)


                with open(root+'/'+file, 'r') as in_f:

                    lineNumber = 0

                    for line in in_f:

                        # Get tokens and append to list
                        columns = line.split()

                        # Get the number of lines
                        currentTag = allTaggedWords[lineNumber][1]

                        # It's a Location, Person or Organization
                        if currentTag != "O":

                            if currentTag == "LOCATION" or currentTag == "ORGANIZATION" or currentTag == "PERSON":

                                # Check for location, and dubble location, like New York or Sri Lanka
                                if currentTag == "LOCATION" and allTaggedWords[lineNumber-1][1] == "LOCATION":
                                        print("dubbele tag!", currentTag)

                                elif currentTag == "LOCATION":
                                    tagCityorCountry = findCityorCountry(columns[3])
                                    #print(tagCityorCountry, columns[3])

                                else:
                                    columns.append(currentTag)


                        # Check for Others
                        else:

                            if columns[4].startswith("N"):

                                columns.append(currentTag)

                        newLine = ' '.join(columns)
                        #print(newLine)

                        lineNumber += 1

    """
    # eerst standaard entity tagger laten runnen op de inputfiles
    # daarna de rest handmatig laten taggen via Wordnet & hypernyms


    """

    NPSyns = wordnet.synsets(str("lake"), pos = 'n')
    #zelfde variabele getagd met LOC
    NP2Syns = wordnet.synsets(str("ocean"), pos = 'n')
    result3= getMaxSim(NPSyns, NP2Syns)
    #print(result3)

    NPSyns2 = wordnet.synsets(str("lake"), pos = 'n')
    #zelfde variabele getagd met LOC
    NP2Syns2 = wordnet.synsets(str("drive"), pos = 'n')
    #result4= getMaxSim(CountrySyns, Country2Syns)
    #print(result4)

    #print(findAnimal("dog"))
    #print(findSport("football"))



    #En als woord Other is, dan checken of het iets anders is dmv van de functies

if __name__ == "__main__":
    main()



