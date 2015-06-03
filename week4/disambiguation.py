#!/usr/bin/python
# Usage: ./disambiguation.py URL

from collections import Counter
import sys
import os
import nltk
from nltk.corpus import wordnet
from nltk import word_tokenize
from nltk.wsd import lesk
from nltk import sent_tokenize


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


def getText(wiki):

    # Curl the URL
    os.system("curl '{0}' | grep '<p>' | sed 's/<[^<]*>//g' > wiki.tmp".format(wiki))

    # Read the text and return it
    with open("wiki.tmp","r") as f:
        os.system("rm wiki.tmp")
        return f.read()

def main(file):

    # Stuff for unicode decode errors
    reload(sys)
    sys.setdefaultencoding("utf-8")

    # Get the text of the  URL
    text = getText(file[1])
    tokens = nltk.word_tokenize(text)

    # POS tag words
    taggedWords = nltk.pos_tag(tokens)

    # Filter all nouns
    nouns = [(word, tag) for word, tag in taggedWords if tag.startswith("N")]

    # Set values for the answers
    amountOfPolysemousWords = 0
    amountOfSenses = 0
    listofsenses = []

    # Get wordnet synsets
    for word, tag in nouns:

        # Get the amount of senses
        senses = len(wordnet.synsets(word, "n"))

        # Check if the word is polysemous
        if senses > 1:

            # Count the polysemous words and senses
            amountOfPolysemousWords = amountOfPolysemousWords + 1
            amountOfSenses = amountOfSenses + senses

            listofsenses.append(senses)

    # Answer for question 1
    print("For this file, there are {} polysemous word".format(amountOfPolysemousWords))

    # Answer for question 3
    averageSenses = amountOfSenses/amountOfPolysemousWords
    print("For this file, the average senses are {} per polysemous word".format(averageSenses))

    # Answer for question 4
    result = Counter(listofsenses)
    print(result)

    # Answer for question 5
    words = ["cars", "quantity", "carbon", "states", "change", "life"]
    pos = "n"
    textObject = nltk.Text(tokens)
    for sent in sent_tokenize(text):
        for word in words:
            context = textObject.concordance(word)
            print("\n\n" + str(context))
            print ("\n\n The result of algorithm is: " + str(lesk(sent, word, pos)))
            print("\n\n All possible senses for " + word + ":")
            for ss in wordnet.synsets(word, "n"):
                print(ss, ss.definition())


if __name__ == "__main__":

    # Check if the length of input is 2
    if len(sys.argv) == 2:
        main(sys.argv)
    else:
        print("Wrong input, please enter a valid URL!")