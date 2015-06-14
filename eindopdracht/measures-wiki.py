#!/usr/bin/python
from collections import Counter
from nltk.metrics import ConfusionMatrix
import os, sys

def main():

    ourTags = []
    goldenStandardTags = []

    # Fill taglist for each group member
    directory = os.getcwd()
    for root, dirs, filenames in os.walk(directory):
        for file in filenames:
            if file == "testfix.set":
                with open(root+'/'+file, 'r') as in_f:
                    for line in in_f:
                            columns = line.split()
                            if (len(columns) > 7):
                                token1 = columns[7]
                                if token1.startswith("http://"):
                                    newUrl = "https"
                                    token1 = newUrl + token1[4:]
                                goldenStandardTags.append(token1)

                            else:
                                goldenStandardTags.append("NOPE")


            elif (file == "developedfinal.set"):
                with open(root+'/'+file, 'r') as in_f:
                    for line in in_f:
                        columns = line.split()
                        if len(columns) > 7:
                            token2 = columns[7]
                            if token2.startswith("http://"):
                                newUrl = "https"
                                token2 = newUrl + token2[4:]
                            ourTags.append(token2)
                        else:
                            ourTags.append("NOPE")


    # Define confusion matrix

    for word in goldenStandardTags:
        if word == "-":
            word.replace(word, "NOPE")



    for word in ourTags:
        if word == "-":
            word.replace(word, "NOPE")

    truePos = 0
    falseNeg = 0
    falsePos = 0
    trueNeg = 0
    correct = 0
    wrong = 0
    correctTag = 0
    wrongTag = 0
    
    counter = 0
    for item in goldenStandardTags:
        if item == "NOPE":
            if ourTags[counter] == "NOPE":
                correct += 1
                trueNeg += 1
            else:
                wrong += 1
                falsePos += 1
        else:
            if ourTags[counter] != "NOPE":
                truePos += 1
                if ourTags[counter] == item:
                    correct += 1
                    correctTag += 1
                else:
                    wrongTag += 1
            else:
                falseNeg= 1
                wrong += 1
        counter += 1
    
    precision = truePos / float(truePos+falsePos)
    recall = truePos / float(truePos+falseNeg)
    fscore = 2 * (precision * recall) / float(precision + recall)
    
    print("Wiki found vs not-found:")
    print("Correct: {}\nWrong: {}".format(correct, wrong))
    print("True Positives: {}\nFalse Positives: {}".format(truePos, falsePos))
    print("True Negatives: {}\nFalse Negatives: {}".format(trueNeg, falseNeg))
    print("Precision: {}\nRecall: {}\nF-score: {}".format(precision, recall, fscore))
    print("\n\nThe actual Wiki pages (only at True Positives):")
    print("Correct Wiki page: {}\nWrong Wiki page: {}".format(correctTag, wrongTag))
main()
