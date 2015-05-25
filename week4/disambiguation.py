#!/usr/bin/python
# Usage: ./disambiguation.py URL

from collections import Counter
import sys
import os
import nltk
from nltk.corpus import wordnet

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

    # POS tag words
    taggedWords = nltk.pos_tag(nltk.word_tokenize(text))

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

            print("\n\n All possible senses for " + word + ":")

            # Loop the synsets and print them
            for ss in wordnet.synsets(word, "n"):
                print(ss, ss.definition())




    # Answer for question 1
    print("For this file, there are {} polysemous word".format(amountOfPolysemousWords))

    # Answer for question 3
    averageSenses = amountOfSenses/amountOfPolysemousWords
    print("For this file, the average senses are {} per polysemous word".format(averageSenses))

    # Answer for question 4
    result = Counter(listofsenses)
    print(result)



if __name__ == "__main__":

    # Check if the length of input is 2
    if len(sys.argv) == 2:
        main(sys.argv)
    else:
        print("Wrong input, please enter a valid URL!")