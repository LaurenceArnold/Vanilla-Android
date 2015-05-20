#!/usr/bin/python
from collections import Counter
from nltk.metrics import ConfusionMatrix
import os, sys  


def main():
    tagsJarik = []
    tagsLaurence = []
    tagsJohan = []

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

    cm = ConfusionMatrix(tagsLaurence, tagsJarik)
    print(cm)

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

    print("TP:", sum(true_positives.values()), true_positives)
    print("FN:", sum(false_negatives.values()), false_negatives)
    print("FP:", sum(false_positives.values()), false_positives)
    print() 

    for i in sorted(labels):
        if true_positives[i] == 0:
            fscore = 0
        else:
            precision = true_positives[i] / float(true_positives[i]+false_positives[i])
            recall = true_positives[i] / float(true_positives[i]+false_negatives[i])
            print(recall)
            fscore = 2 * (precision * recall) / float(precision + recall)
        print(i, fscore)

main()
