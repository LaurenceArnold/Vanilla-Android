#!/usr/bin/python

import os
import nltk
from nltk.corpus import wordnet
from nltk.tag.stanford import NERTagger
import wikipedia

def disambiguationWikipedia(noun):

    """
    Disambiguation for Wikipedia errors
    """

    # Try to get wikipedia content
    try:
        wiki = wikipedia.page(noun)

    except wikipedia.exceptions.DisambiguationError as e:
        newNoun = e.options[0]

        try:
            wiki = wikipedia.page(newNoun)

        except:
            return False

    return wiki

def getMaxSim(synsets1, synsets2):

    """
    From slides
    """

    maxSim = None
    for syn1 in synsets1:
        for syn2 in synsets2:
            sim = syn1.lch_similarity(syn2)
            if ((maxSim == None) or (maxSim < sim)):
                maxSim = sim

    return maxSim

def hypernymOf(synset1, synset2):

    """
    True als synset2 een hypernym is van synset1 (of dezelfde synset)
    """

    if (synset1 == synset2):
        return True
    for hypernym in synset1.hypernyms():
        if (synset2 == hypernym):
            return True
        if (hypernymOf(hypernym, synset2)):
            return True

    return False


def findAnimal(noun):

    """
    Look with synsets for an animal
    """
    try:
        synset1 = wordnet.synsets(noun, pos='n')
        if (isinstance(synset1, list)):
            synset1 = synset1[0]

    except:

        return False

    # Synsets to look for:
    animal = wordnet.synsets("animal", pos='n')[0]

    if (hypernymOf(synset1, animal)):
        return True

    return False

def findSport(noun):

    """
    Look with synsets for a sport
    """

    try:
        synset1 = wordnet.synsets(noun, pos='n')
        if (isinstance(synset1, list)):
            synset1 = synset1[0]

    except:
        return False

    # Synsets to look for:
    sport = wordnet.synsets("sport", pos='n')[0]

    if (hypernymOf(synset1, sport)):
        return True

    return False

def findCityOrCountry(word):

    """
    Check if it is a country or city
    """

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

        # Check for disambiguation on Wikipedia
        wiki = disambiguationWikipedia(word)

        if wiki == False:
            return False

        # Get first sentence
        firstSentence = wiki.content.split(".")[0]

        # Check for city in the first sentence
        if "city" in firstSentence:
            return "CIT"

        # City is not found in the sentence
        else:
            return "COU"

def isNatural(noun):

    """
    Check if it is a natural place
    """

    naturalList = ["volcano", "river", "forest", "jungle", "ocean", "water", "lake",
    "mountain", "hill", "sea", "woods", "island", "islands", "sea"]

    # Check for disambiguation on Wikipedia
    wiki = disambiguationWikipedia(noun)

    # Get first sentence
    if wiki == False:
        return False

    firstSentence = wiki.content.split(".")[0]

    for word in firstSentence:
        for item in naturalList:
            if (word.lower() == item.lower()):
                return True

    return False

def isEntertainment(noun):

    """
    Check if it is an entertainment
    """

    entertainmentList = ["newspaper", "television", "radio", "magazine",
    "show", "musical", "song", "album", "tv", "Netflix", "film", "book", "novel"]

    wiki = disambiguationWikipedia(noun)

    if wiki == False:
        return False

    # Get first sentence
    firstSentence = wiki.content.split(".")[0]

    for word in firstSentence:
        for item in entertainmentList:
            if (word.lower() == item.lower()):
                return True

    return False

def getWikiURL(noun, tag):

    """
    Get the Wikipedia URL
    """

    if tag == "PER":
        searchList = wikipedia.search(noun, results=2)

        if len(searchList) == 2:
            wikipage = wikipedia.page(searchList[0])
            firstSentence = wikipage.content.split(".")[0]

            if "born" in firstSentence:
                return wikipage.url

            else:
                wikipage = wikipedia.page(searchList[1])
                firstSentence = wikipage.content.split(".")[0]

                if "born" in firstSentence:
                    return wikipage.url

                else:
                    wikipage = wikipedia.page(searchList[0])
                    return wikipage.url

    else:
        # Check for disambiguation on Wikipedia
        wiki = disambiguationWikipedia(noun)

        firstSentence = wiki.content.split(".")[0]


        try:

            url = wiki.url

        except:

            return "Null"

        return url

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
            if file == "development.set":

                # Open file
                with open(root+'/'+file, 'r') as in_f:

                    lineList = " "

                    # Loop through lines of file
                    for line in in_f:

                        # Get tokens and append to list
                        columns = line.split()
                        if len(columns) > 2:
                            lineList += " " + str(columns[4])

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
                    nextLine = in_f.read(1)
                    while nextLine != "":

                        # Get tokens and append to list
                        columns = line.split()

                        if len(columns) == 8:
                            columns.pop(7)
                            columns.pop(6)


                        # Get the noun
                        noun = columns[4]

                        # Get the number of lines
                        currentTag = allTaggedWords[lineNumber][1]

                        # It's a Location, Person or Organization
                        if currentTag != "O":

                            if currentTag == "LOCATION":

                                # Check for locations like New-York (multiple words)
                                if currentTag == "LOCATION" and allTaggedWords[lineNumber+1][1] == "LOCATION":
                                        wordResult = str(noun) + "_" + str(allTaggedWords[lineNumber+1][0])

                                        if allTaggedWords[lineNumber+2][1] == "LOCATION":
                                            wordResult += "_" + str(allTaggedWords[lineNumber+2][0])
                                            lineNumber += 2
                                            nextLine = in_f.read(2)
                                            
                                        elif allTaggedWords[lineNumber+3][1] == "LOCATION":
                                            wordResult += "_" + str(allTaggedWords[lineNumber+3][0])
                                            lineNumber += 3
                                            nextLine = in_f.read(3)

                                        elif allTaggedWords[lineNumber+4][1] == "LOCATION":
                                            wordResult += "_" + str(allTaggedWords[lineNumber+4][0])
                                            lineNumber += 4
                                            nextLine = in_f.read(4)
                                        else:
                                            lineNumber += 1
                                            nextLine = in_f.read(1)
                                            
                                        tagCityOrCountry = findCityOrCountry(wordResult)

                                        columns.append(tagCityOrCountry)


                                # City of country exists of a single word
                                else:
                                    result = findCityOrCountry(noun)
                                    columns.append(result)

                            # It is a person
                            elif currentTag == "PERSON":
                                columns.append("PER")

                            # It is an organization
                            elif currentTag == "ORGANIZATION":
                                columns.append("ORG")

                        # Check for Others (Natural Places, Animals, Sports)
                        else:

                            # If it is a noun
                            if columns[5].startswith("N"):

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

                        if len(columns) == 7:
                            tag = columns[6]
                            columns.append(getWikiURL(noun, tag))

                        newLine = ' '.join(columns)
                        print(newLine)

    

if __name__ == "__main__":
    main()
