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

        if wiki == "Null":
            return "Null"

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

                        if len(columns) > 5:
                            lineList += " " + unicode(str(columns[4]),errors='ignore')
                            lineNum += 1
                            wordList.append([lineNum, columns[0], columns[1], columns[2], columns[3], str(columns[4]), columns[5],"", "" ])

                    # Tag words with NER and append
                    tokenizedText = nltk.sent_tokenize(lineList)
                    taggedWords = nerTaggerStanford.tag(tokenizedText)

                    listIndex = 0
                    for el in taggedWords:

                        for word in el:
                            wordList[listIndex][7] = str(word[1])
                            listIndex += 1

                for item in wordList:
                    if item[8]:
                        continue

                    lineNumber = item[0]
                    currentTag = item[7]

                    # It's a Location, Person or Organization
                    if currentTag != "O":

                        if currentTag == "LOCATION":
                            wordResult = item[5]
                            wordLen = 1

                            # Check for locations like New-York (multiple words)
                            # Line number is always 1 ahead of index (line 1 is index 0)
                            if wordList[lineNumber][7] == "LOCATION":
                                wordResult = wordResult + "_" + str(wordList[lineNumber][5])
                                wordLen = 2

                                if wordList[lineNumber+1][7] == "LOCATION":
                                    wordResult = wordResult + "_" + str(wordList[lineNumber+1][5])
                                    wordLen = 3

                                    if wordList[lineNumber+2][7] == "LOCATION":
                                        wordResult = wordResult + "_" + str(wordList[lineNumber+2][5])
                                        wordLen = 4

                                        if wordList[lineNumber+3][7] == "LOCATION":
                                            wordResult = wordResult + "_" + str(wordList[lineNumber+3][5])
                                            wordLen = 5

                                            if wordList[lineNumber+4][7] == "LOCATION":
                                                wordResult = wordResult + "_" + str(wordList[lineNumber+4][5])
                                                wordLen = 6


                            tagCityOrCountry = findCityOrCountry(wordResult)
                            thisLine = lineNumber - 1
                            countryWiki = getWikiURL(wordResult, currentTag)
                            for i in range(wordLen):
                                wordList[thisLine+i][7] = tagCityOrCountry
                                wordList[thisLine+i][8] = countryWiki

                        # It is a person
                        elif currentTag == "PERSON":
                            wordResult = item[5]
                            wordLen = 1

                            # Check for locations like New-York (multiple words)
                            # Line number is always 1 ahead of index (line 1 is index 0)
                            if wordList[lineNumber][7] == "PERSON":
                                wordResult = wordResult + "_" + str(wordList[lineNumber][5])
                                wordLen = 2

                                if wordList[lineNumber+1][7] == "PERSON":
                                    wordResult = wordResult + "_" + str(wordList[lineNumber+1][5])
                                    wordLen = 3

                                    if wordList[lineNumber+2][7] == "PERSON":
                                        wordResult = wordResult + "_" + str(wordList[lineNumber+2][5])
                                        wordLen = 4

                                        if wordList[lineNumber+3][7] == "PERSON":
                                            wordResult = wordResult + "_" + str(wordList[lineNumber+3][5])
                                            wordLen = 5

                                            if wordList[lineNumber+4][7] == "PERSON":
                                                wordResult = wordResult + "_" + str(wordList[lineNumber+4][5])
                                                wordLen = 6

                            thisLine = lineNumber - 1
                            personWiki = getWikiURL(wordResult, currentTag)
                            for i in range(wordLen):
                                wordList[thisLine+i][7] = "PER"
                                wordList[thisLine+i][8] = personWiki


                        # It is an organization
                        elif currentTag == "ORGANIZATION":
                            wordResult = item[5]
                            wordLen = 1

                            # Check for locations like New-York (multiple words)
                            # Line number is always 1 ahead of index (line 1 is index 0)
                            if wordList[lineNumber][7] == "ORGANIZATION":
                                wordResult = wordResult + "_" + str(wordList[lineNumber][5])
                                wordLen = 2

                                if wordList[lineNumber+1][7] == "ORGANIZATION":
                                    wordResult = wordResult + "_" + str(wordList[lineNumber+1][5])
                                    wordLen = 3

                                    if wordList[lineNumber+2][7] == "ORGANIZATION":
                                        wordResult = wordResult + "_" + str(wordList[lineNumber+2][5])
                                        wordLen = 4

                                        if wordList[lineNumber+3][7] == "ORGANIZATION":
                                            wordResult = wordResult + "_" + str(wordList[lineNumber+3][5])
                                            wordLen = 5

                                            if wordList[lineNumber+4][7] == "ORGANIZATION":
                                                wordResult = wordResult + "_" + str(wordList[lineNumber+4][5])
                                                wordLen = 6

                            thisLine = lineNumber - 1
                            orgWiki = getWikiURL(wordResult, currentTag)
                            for i in range(wordLen):
                                wordList[thisLine+i][7] = "ORG"
                                wordList[thisLine+i][8] = orgWiki

                        # It is a DATE for example, we don't need this in our output, so replace it for nothing
                        else:
                            item.pop(8)
                            item.pop(7)

                    # Check for Others (Natural Places, Animals, Sports)
                    elif currentTag == "O":

                        # If it is a noun, we need to check if it is an entity we need
                        if item[6].startswith("N"):

                            # Check if the noun is an animal
                            if findAnimal(item[5]):
                                item[7] = "ANI"
                                item[8] = getWikiURL(item[5], currentTag)

                            # Check if it is a sport
                            elif findSport(item[5]):
                                item[7] = "SPO"
                                item[8] = getWikiURL(item[5], currentTag)

                            # Check if it is a natural place
                            elif isNatural(item[1]):
                                item[7] = "NAT"
                                item[8] = getWikiURL(item[5], currentTag)

                            # Check if it is entertainment
                            elif isEntertainment(item[5]):
                                item[7] = "ENT"
                                item[8] = getWikiURL(item[5], currentTag)

                            # The tag has no meaning, so delete the last 2 fields
                            else:
                                item.pop(8)
                                item.pop(7)

                        # Delete the last 2 fields because it is not even a noun
                        else:
                            item.pop(8)
                            item.pop(7)

                        #newLine = ' '.join(columns)
                        #print(newLine)

                    # Remove our linenumber used in some pieces of code
                    item.pop(0)
                    print(item)

if __name__ == "__main__":
    main()