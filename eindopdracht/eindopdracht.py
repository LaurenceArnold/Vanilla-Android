#!/usr/bin/python

import os
import nltk
from nltk.corpus import wordnet
from nltk.tag.stanford import NERTagger
import wikipedia

def getMaxSim(synsets1, synsets2):

    """ From slides """

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

    """ Look with synsets for an animal """

    synset1 = wordnet.synsets(noun, pos='n')
    if (isinstance(synset1, list)):
        synset1 = synset1[0]

    # Synsets to look for:
    animal = wordnet.synsets("animal", pos='n')[0]

    if (hypernymOf(synset1, animal)):
        return True

    return False

def findSport(noun):

    """ Look with synsets for a sport """

    synset1 = wordnet.synsets(noun, pos='n')
    if (isinstance(synset1, list)):
        synset1 = synset1[0]

    # Synsets to look for:
    sport = wordnet.synsets("sport", pos='n')[0]

    if (hypernymOf(synset1, sport)):
        return True

    return False

def findCityOrCountry(word):

    """ Check if it is a country or city """

    # If tag is location, loop through these lines
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

    # City or country is not in the Wordnet database
    else:

        # Get wikipedia content
        wiki = wikipedia.page(word)

        # Get first sentence
        firstSentence = wiki.content.split(".")[0]

        # Check for city in the first sentence
        if "city" in firstSentence:
            return "CIT"

        # City is not found in the sentence
        else:
            return "COU"

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
    "show", "musical", "song", "album", "tv", "Netflix", "film", "book", "novel"]

    # Get wikipedia content
    wiki = wikipedia.page(noun)
    # Get first sentence
    firstSentence = wiki.content.split(".")[0]

    for word in firstSentence:
        for item in entertainmentList:
            if (word.lower() == item.lower()):
                return True

    return False

def getWikiURL(tag):

    """ Get the Wikipedia URL """

    wiki = wikipedia.page(tag)

    return wiki.url

def main():
    # Get the directory of the file
    directory = os.getcwd()

    # Open NERtagger
    nerTaggerStanford = NERTagger('/Library/Python/2.7/site-packages/stanford-ner-2014-06-16/classifiers/english.muc.7class.distsim.crf.ser.gz',
                   '/Library/Python/2.7/site-packages/stanford-ner-2014-06-16/stanford-ner-3.4.jar')

    words = []
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

                    # Tag words with NER and append
                    tokenizedText = nltk.sent_tokenize(lineList)
                    taggedWords = nerTaggerStanford.tag(tokenizedText)

                    allTaggedWords = []

                    for el in taggedWords:
                        for word in el:
                            allTaggedWords.append(word)

                # Open file again
                with open(root+'/'+file, 'r') as in_f:

                    lineNumber = 0

                    for line in in_f:

                        # Get tokens and append to list
                        columns = line.split()

                        # Get the noun
                        noun = columns[3]

                        # Get the number of lines
                        currentTag = allTaggedWords[lineNumber][1]

                        # It's a Location, Person or Organization
                        if currentTag != "O":

                            if currentTag == "LOCATION":

                                # Check for locations like New-York (multiple words)
                                if currentTag == "LOCATION" and allTaggedWords[lineNumber-1][1] == "LOCATION":
                                        wordResult = str(allTaggedWords[lineNumber-1][0]) + "_" + str(noun)
                                        tagCityOrCountry = findCityOrCountry(wordResult)
                                        #print(tagCityOrCountry, wordResult)

                                # City of country exists of a single word
                                else:
                                    result = findCityOrCountry(noun)
                                    columns.append(result)

                            # It is a person
                            if currentTag == "PERSON":
                                columns.append("PER")

                            # It is an organization
                            if currentTag == "ORGANIZATION":
                                columns.append("ORG")

                        # Check for Others (Natural Places, Animals, Sports)
                        else:

                            if columns[4].startswith("N"):

                                # Check if the noun is an animal
                                if findAnimal(noun):
                                    columns.append("ANI")

                                # Check if it is a sport
                                elif findSport(noun):
                                    columns.append("SPO")

                                # Check if it is a natural place
                                elif isNatural(noun):
                                    columns.append("NAT")

                                # Check if it is entertainment
                                elif isEntertainment(noun):
                                    columns.append("ENT")

                        newLine = ' '.join(columns)
                        #print(newLine)

                        lineNumber += 1



if __name__ == "__main__":
    main()