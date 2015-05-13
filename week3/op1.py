#!/usr/bin/python

import nltk
import os, sys


def main():

    # Get the directory of the file
    directory = os.getcwd()

    # Loop through maps
    for root, dirs, filenames in os.walk(directory):

        # Every f is a file
        for file in filenames:

            # Check if the file is en.tok.off
            if file == "en.tok.off":

                # Open file
                with open(root+'/'+file, 'r') as in_f:

                    # Loop through lines of file
                    for line in in_f:

                        # Empty list for tokens per line
                        tokenList = []

                        # Get tokens and append to list
                        columns = line.split()
                        token = columns[3]
                        tokenList.append(token)

                        # POS tag token
                        taggedTokens = nltk.pos_tag(tokenList)

                        print(taggedTokens)



if __name__ == "__main__":
    main()
