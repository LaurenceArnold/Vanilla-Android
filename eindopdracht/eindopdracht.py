#!/usr/bin/python

import nltk
from nltk.corpus import wordnet
from nltk.wsd import lesk


def main():
    # Get the directory of the file
    directory = os.getcwd()

    # List for the nouns
    # Need to be outside of the loop because of the list comprehesion
    NounList = []

    # Loop through maps
    for root, dirs, filenames in os.walk(directory):

        # Loop trough files
        for file in filenames:

            # Check if the file is en.tok.off
            if file == "en.tok.off.pos.ent":

                # Open file
                with open(root+'/'+file, 'r') as in_f:

                    # Loop through lines of file
                    for line in in_f:

                        # Get tokens and append to list
                        columns = line.split()
                        token = columns[4]
                        NounList.append(token)

    nouns = [tag for tag in NounList if tag.startswith("N")]

    # eerst standaard entity tagger laten runnen op de inputfiles
    # daarna de rest handmatig laten taggen via Wordnet & hypernyms

    #dus jarik moet de eerste stap moeten we de de named entity laten runnen.



if __name__ == "__main__":
    main()



