#!/usr/bin/python

import nltk
import os, sys

def main():

    # Get the directory of the file
    directory = os.getcwd()

    # Loop through maps
    for root, dirs, filenames in os.walk(directory):
        for f in filenames:
            if f == "en.tok.off":
                print(f)Bug fix


if __name__ == "__main__":
    main()
