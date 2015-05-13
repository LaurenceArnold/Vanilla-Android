#!/usr/bin/python

import nltk
import os, sys

def main():

    # Get the directory of the file
    directory = os.getcwd()

    # Loop through maps
    for root, dirs, filenames in os.walk(directory):




        # every f is a file
        for file in filenames:

            # Check if the file is en.tok.off
            if file == "en.tok.off":

                # Open file
                with open(root+'/'+file, 'r') as in_f:

                    # Empty list for tokens per file
                    tokenList = []

                    # Loop throug lines of file
                    for line in in_f:

                        #variabele[1] in pos Tags in loop.append(line))

                        columns = line.split()
                        
                        print(columns)
                        [tokenList.append(token) for token in columns[3]]

                    print(tokenList)


if __name__ == "__main__":
    main()
