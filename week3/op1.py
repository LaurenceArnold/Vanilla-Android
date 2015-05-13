#!/usr/bin/python

import nltk
import os, sys

def main():

    # Get the directory of the file
    directory = os.getcwd()

    # Loop through maps
    for root, dirs, filenames in os.walk(directory):

        # every f is a file
        for f in filenames:

            # If file is the token file
            if f == "en.tok.off":
                with open(root+'/'+f, 'r') as in_f:
                    for line in in_f:
                        #variabele[1] in pos Tags in loop.append(line))



if __name__ == "__main__":
    main()
