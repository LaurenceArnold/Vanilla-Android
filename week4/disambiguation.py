#!/usr/bin/python
# Usage: ./disambiguation.py URL

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
    taggedWords = nltk.pos_tag(text.split())

    # Filter all nouns
    nouns = [(word, tag) for word, tag in taggedWords if tag.startswith("N")]

    # Get wordnet synsets
    for word, tag in nouns:
        print(word, tag)
        for ss in wordnet.synsets(word, "n"):
            print(ss, ss.definition())


if __name__ == "__main__":

    # Check if the lenght of input is 2
    if len(sys.argv) == 2:
        main(sys.argv)
    else:
        print("Wrong input.")