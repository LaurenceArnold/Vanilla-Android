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

    tagsJarik = []
    tagsLaurence = []
    tagsJohan = []

    # Fill taglist for each group member
    directory = os.getcwd()
    for root, dirs, filenames in os.walk(directory):
        for file in filenames:
            if file == "en.tok.off.johan.tmp":
                with open(root+'/'+file, 'r') as in_f:
                    for line in in_f:
                        columns = line.split()
                        if (len(columns) > 5):
                            token1 = columns[5]
                            tagsJohan.append(token1)
                        else:
                            tagsJohan.append("NOPE")

            elif (file == "en.tok.off.pos Laurence.tmp"):
                with open(root+'/'+file, 'r') as in_f:
                    for line in in_f:
                        columns = line.split()
                        if len(columns) > 5:
                            token2 = columns[5]
                            tagsLaurence.append(token2)
                        else:
                            tagsLaurence.append("NOPE")

            elif (file == "en.tok.off.pos.tmp"):
                with open(root+'/'+file, 'r') as in_f:
                     for line in in_f:
                        columns = line.split()
                        if len(columns) > 5:
                             token3= columns[5]
                             tagsJarik.append(token3)
                        else:
                            tagsJarik.append("NOPE")

    # Define confusion matrix
    cm = ConfusionMatrix(tagsLaurence, tagsJohan)
    
    # Search for interesting vs non-interesting entities
    # (how often we agree on finding anything, no matter the tag)
    labelNope = set('PER COU CIT ENT ORG NAT NOPE'.split())
    tpNopes = Counter()
    fpNopes = Counter()
    fnNopes = Counter()
    
    for i in labelNope:
        for j in labelNope:
            if ((i != 'NOPE') and (j != 'NOPE')):
                tpNopes[i] += cm[i,j]
            else:
                fnNopes[i] += cm[i,j]
                fpNopes[j] += cm[i,j]
    
    
    print("\n\n##############################################################")
    print("Opdracht 3.1:\n")

    # Get the precision, recall and fscore
    precisionOne, recallOne, fscoreOne = compare(tagsLaurence, tagsJohan)
    precisionTwo, recallTwo, fscoreTwo = compare(tagsLaurence, tagsJarik)
    precisionThree, recallThree, fscoreThree = compare(tagsJohan, tagsJarik)

    # Calculate the average
    averagePrecision = (precisionOne + precisionTwo + precisionThree) / 3
    averageRecall = (recallOne + recallTwo + recallThree) / 3
    averageFscore = (fscoreOne + fscoreTwo + fscoreThree) / 3

    # Show the average
    print("Average precision: {}".format(averagePrecision))
    print("Average recall: {}".format(averageRecall))
    print("Average fscore: {}".format(averageFscore))

    labels = set('PER COU CIT ENT ORG NAT'.split())

    true_positives = Counter()
    false_negatives = Counter()
    false_positives = Counter()

    for i in labels:
        for j in labels:
            if i == j:
                true_positives[i] += cm[i,j]
            else:
                false_negatives[i] += cm[i,j]
                false_positives[j] += cm[i,j]
    
    print("##############################################################")
    print("Opdracht 3.2:\n")
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
    print("Opdracht 3.3 (matrix):\n")
    print(cm)
    print("##############################################################")

main()
