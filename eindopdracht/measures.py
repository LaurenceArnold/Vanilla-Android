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
            if file == "developmentfix.set":
                with open(root+'/'+file, 'r') as in_f:
                    for line in in_f:
                            columns = line.split()
                            if (len(columns) > 7):
                                token1 = columns[6]
                                goldenStandardTags.append(token1)

                            else:
                                goldenStandardTags.append("NOPE")


            elif (file == "developed.set"):
                with open(root+'/'+file, 'r') as in_f:
                    for line in in_f:
                        columns = line.split()
                        if len(columns) > 7:
                            token2 = columns[6]
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

    if len(goldenStandardTags) > len(ourTags):
        difference = len(goldenStandardTags) - len(ourTags)
        for i in range(difference):
            ourTags.append("NOPE")
    print(len(ourTags))


    cmTags = ConfusionMatrix(goldenStandardTags, ourTags)

    print("\n\n##############################################################")

    # Get the precision, recall and fscore
    #precision, recall, fscore = compare(goldenStandardTags, ourTags)



    labels = set('PER COU CIT ENT ORG NAT'.split())

    true_positives = Counter()
    false_negatives = Counter()
    false_positives = Counter()

    for i in labels:
        for j in labels:
            if i == j:
                true_positives[i] += cmTags[i,j]
            else:
                false_negatives[i] += cmTags[i,j]
                false_positives[j] += cmTags[i,j]

    print("##############################################################")

    fscores = 0

    for i in sorted(labels):
        print(i)
        if true_positives[i] == 0:
            fscore = 0
        else:
            precision = true_positives[i] / float(true_positives[i]+false_positives[i])
            recall = true_positives[i] / float(true_positives[i]+false_negatives[i])
            fscore = 2 * (precision * recall) / float(precision + recall)
            print("Precision: " + str(precision))
            print("Recall: " + str(recall))
        print("f-score: " + str(fscore) + "\n")
        fscores += fscore


    print("\n\nGemiddelde f-score: " + str(fscores / 6))
    print("##############################################################")

    print(cmTags)

main()
