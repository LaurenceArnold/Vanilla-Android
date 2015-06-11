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
        new = e.options[0]

        try:
            wiki = wikipedia.page(new)

        except:
            return 'Null'

    except wikipedia.exceptions.PageError:
        new = wikipedia.search(noun)

        try:
            wiki = wikipedia.page(new[0])

        except:
            return 'Null'

    except:
        return 'Null'


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

    Countrylist = ["country","Republic", "Monarcy", "state", "region", "Kingdom"]
    Citylist = ["city"]

    # Check for disambiguation on Wikipedia
    wiki = disambiguationWikipedia(word)

    if wiki == "Null":
        return False

    # Get first sentence
    firstSentence = wiki.content.split(".")[0]
    print(firstSentence)

    for word in firstSentence.split():
        for item in Countrylist:
            if (word.lower() == item.lower()):
                return "COU"

    for word in firstSentence.split():
        for item in Citylist:
            if (word.lower() == item.lower()):
                return "CIT"

    else:
        return "-"


def isNatural(noun):

    """
    Check if it is a natural place
    """

    naturalList = ["volcano", "river", "forest", "jungle", "ocean", "water", "lake",
    "mountain", "hill", "sea", "woods", "island", "islands", "sea"]

    # Check for disambiguation on Wikipedia
    wiki = disambiguationWikipedia(noun)

    # Get first sentence
    if wiki == "Null":
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

    if wiki == "Null":
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

    if tag == "PERSON":

        try:
            wiki = wikipedia.page(noun)

        except wikipedia.exceptions.DisambiguationError as e:
            try:
                newNoun = e.options[0]
                newNoun2 = e.options[1]

                wiki = wikipedia.page(newNoun)
                wiki2 = wikipedia.page(newNoun2)

                firstSentence1 = wiki.content.split(".")[0]
                firstSentence2 = wiki2.content.split(".")[0]

                if "born" in firstSentence1:
                    return wiki.url

                elif "born" in firstSentence2:
                    return wiki2.url

                else:
                    return "Null"

            except:
                return "Null"

        except wikipedia.exceptions.PageError:
            new = wikipedia.search(noun)

        try:
            wiki = wikipedia.page(new[0])

        except:
            return 'Null'

    else:
        # Check for disambiguation on Wikipedia
        wiki = disambiguationWikipedia(noun)

        try:
            url = wiki.url

        except:
            return "Null"

        return url

def main():

    wordList = []

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
                    lineNum = 0
                    # Loop through lines of file
                    for line in in_f:

                        # Get tokens and append to list
                        columns = line.split()
                        if len(columns) > 3:
                            lineList += " " + str(columns[4])
                            lineNum += 1
                            wordList.append([lineNum, str(columns[4]), "", ""])


                    # Tag words with NER and append
                    tokenizedText = nltk.sent_tokenize(lineList)
                    taggedWords = nerTaggerStanford.tag(tokenizedText)

                    allTaggedWords = []

                    listIndex = 0
                    for el in taggedWords:

                        for word in el:
                            wordList[listIndex][2] = str(word[1])
                            listIndex += 1

                for item in wordList:
                    if item[3]:
                        print(item)
                        continue

                    lineNumber = item[0]
                    currentTag = item[2]
                    # It's a Location, Person or Organization
                    if currentTag != "O":
                        if currentTag == "LOCATION":
                            wordResult = item[1]
                            wordLen = 1

                            # Check for locations like New-York (multiple words)
                            # Line number is always 1 ahead of index (line 1 is index 0)
                            if wordList[lineNumber][2] == "LOCATION":
                                wordResult = wordResult + "_" + str(wordList[lineNumber][1])
                                wordLen = 2

                                if wordList[lineNumber+1][2] == "LOCATION":
                                    wordResult = wordResult + "_" + str(wordList[lineNumber+1][1])
                                    wordLen = 3

                                    if wordList[lineNumber+2][2] == "LOCATION":
                                        wordResult = wordResult + "_" + str(wordList[lineNumber+2][1])
                                        wordLen = 4

                                        if wordList[lineNumber+3][2] == "LOCATION":
                                            wordResult = wordResult + "_" + str(wordList[lineNumber+3][1])
                                            wordLen = 5

                                            if wordList[lineNumber+4][2] == "LOCATION":
                                                wordResult = wordResult + "_" + str(wordList[lineNumber+4][1])
                                                wordLen = 6


                            tagCityOrCountry = findCityOrCountry(wordResult)
                            thisLine = lineNumber - 1
                            countryWiki = getWikiURL(wordResult, currentTag)
                            for i in range(wordLen):
                                wordList[thisLine+i][2] = tagCityOrCountry
                                wordList[thisLine+i][3] = countryWiki



                        # It is a person

                        elif currentTag == "PERSON":
                            wordResult = item[1]
                            wordLen = 1

                            # Check for locations like New-York (multiple words)
                            # Line number is always 1 ahead of index (line 1 is index 0)
                            if wordList[lineNumber][2] == "PERSON":
                                wordResult = wordResult + "_" + str(wordList[lineNumber][1])
                                wordLen = 2

                                if wordList[lineNumber+1][2] == "PERSON":
                                    wordResult = wordResult + "_" + str(wordList[lineNumber+1][1])
                                    wordLen = 3

                                    if wordList[lineNumber+2][2] == "PERSON":
                                        wordResult = wordResult + "_" + str(wordList[lineNumber+2][1])
                                        wordLen = 4

                                        if wordList[lineNumber+3][2] == "PERSON":
                                            wordResult = wordResult + "_" + str(wordList[lineNumber+3][1])
                                            wordLen = 5

                                            if wordList[lineNumber+4][2] == "PERSON":
                                                wordResult = wordResult + "_" + str(wordList[lineNumber+4][1])
                                                wordLen = 6

                            thisLine = lineNumber - 1
                            personWiki = getWikiURL(wordResult, currentTag)
                            for i in range(wordLen):
                                wordList[thisLine+i][2] = "PER"
                                wordList[thisLine+i][3] = personWiki


                        # It is an organization
                        elif currentTag == "ORGANIZATION":
                            wordResult = item[1]
                            wordLen = 1

                            # Check for locations like New-York (multiple words)
                            # Line number is always 1 ahead of index (line 1 is index 0)
                            if wordList[lineNumber][2] == "ORGANIZATION":
                                wordResult = wordResult + "_" + str(wordList[lineNumber][1])
                                wordLen = 2

                                if wordList[lineNumber+1][2] == "ORGANIZATION":
                                    wordResult = wordResult + "_" + str(wordList[lineNumber+1][1])
                                    wordLen = 3

                                    if wordList[lineNumber+2][2] == "ORGANIZATION":
                                        wordResult = wordResult + "_" + str(wordList[lineNumber+2][1])
                                        wordLen = 4

                                        if wordList[lineNumber+3][2] == "ORGANIZATION":
                                            wordResult = wordResult + "_" + str(wordList[lineNumber+3][1])
                                            wordLen = 5

                                            if wordList[lineNumber+4][2] == "ORGANIZATION":
                                                wordResult = wordResult + "_" + str(wordList[lineNumber+4][1])
                                                wordLen = 6

                            thisLine = lineNumber - 1
                            orgWiki = getWikiURL(wordResult, currentTag)
                            for i in range(wordLen):
                                wordList[thisLine+i][2] = "ORG"
                                wordList[thisLine+i][3] = orgWiki

                    # Check for Others (Natural Places, Animals, Sports)
                    else:

                        # If it is a noun

                        if columns[5].startswith("N"):

                            # Check if the noun is an animal
                            if findAnimal(item[1]):
                                item[2] = "ANI"
                                item[3] = getWikiURL(item[1], currentTag)

                            # Check if it is a sport
                            elif findSport(item[1]):
                                item[2] = "SPO"
                                item[3] = getWikiURL(item[1], currentTag)

                            # Check if it is a natural place
                            elif isNatural(item[1]):
                                item[2] = "NAT"
                                item[3] = getWikiURL(item[1], currentTag)

                            # Check if it is entertainment
                            elif isEntertainment(item[1]):
                                item[2] = "ENT"
                                item[3] = getWikiURL(item[1], currentTag)

                            else:
                                item[2] = "-"
                                item[3] = "-"


                        #newLine = ' '.join(columns)
                        #print(newLine)

                    print(item)

if __name__ == "__main__":
    main()
