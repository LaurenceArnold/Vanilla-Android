#!/usr/bin/python
from collections import Counter
from nltk.metrics import ConfusionMatrix
import os, sys

def compare(listOne, listTwo):

    truePositive = len([i for i, j in zip(listOne, listTwo) if i != 'NOPE' and j != 'NOPE'])
    falseNegative = len([i for i, j in zip(listOne, listTwo) if i == 'NOPE' and j != 'NOPE'])
    falsePositive = len([i for i, j in zip(listOne, listTwo) if i != 'NOPE' and j == 'NOPE'])

    precision = truePositive / float(truePositive+falsePositive)
    recall = truePositive / float(truePositive+falseNegative)
    fscore = 2 * (precision * recall) / float(precision + recall)

    return precision, recall, fscore

def main():

    ourTags = []
    goldenStandardTags = []

    # Fill taglist for each group member
    directory = os.getcwd()
    for root, dirs, filenames in os.walk(directory):
        for file in filenames:
            if file == "development.set":
                with open(root+'/'+file, 'r') as in_f:
                    linenr = 0
                    for line in in_f:
                        if linenr <= 2286:
                            columns = line.split()

                            if (len(columns) > 7):
                                token1 = columns[6]
                                links1 = columns[7]
                                goldenStandardTags.append(token1)

                            else:
                                goldenStandardTags.append("NOPE")

                            linenr += 1



            elif (file == "developed.set"):
                with open(root+'/'+file, 'r') as in_f:
                    for line in in_f:
                        columns = line.split()
                        if len(columns) > 7:
                            token2 = columns[6]
                            links2 = columns[7]
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


    cmTags = ConfusionMatrix(goldenStandardTags, ourTags)

    print("\n\n##############################################################")

    # Get the precision, recall and fscore
    precision, recall, fscore = compare(goldenStandardTags, ourTags)


    # Show the average
    print("Average precision: {}".format(precision))
    print("Average recall: {}".format(recall))
    print("Average fscore: {}".format(fscore))

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
