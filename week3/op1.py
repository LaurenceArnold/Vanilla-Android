#!/usr/bin/python
# DON'T EXECUTE
# ONLY WHEN THERE ARE NO TAGGED FILES


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

                        # POS tag token w
                        taggedTokens = nltk.pos_tag(tokenList)

                        # Add token to the line
                        columns.append(taggedTokens[0][1])
                        newLine = ' '.join(columns)

                        # Write results to new file
                        with open(root+'/en.tok.off.pos.en', 'a') as posfile:
                            posfile.write(newLine + '\n')


if __name__ == "__main__":
    main()
