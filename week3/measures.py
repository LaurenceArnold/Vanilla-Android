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
            if file == "en.tok.off.johan":
                with open(root+'/'+file, 'r') as in_f:
                    for line in in_f:
                        columns = line.split()
                        if (len(columns) > 5):
                            token = columns[5]
                            
                            if not len(tagsJohan) > 101:
                                tagsJohan.append(token)
            if ((file == "en.tok.off Laurence") or (file == "en.tok.off.pos Laurence")):
                with open(root+'/'+file, 'r') as in_f:
                    for line in in_f:
                        columns = line.split()
                        if len(columns) > 5:
                            token = columns[5]
                            tagsLaurence.append(token)


    #ref  = 'DET NN VB DET JJ NN NN IN DET NN'.split()
    #tagged = 'DET VB VB DET NN NN NN IN DET NN'.split()
    
    print(len(tagsLaurence), len(tagsJohan))
    cm = ConfusionMatrix(tagsLaurence, tagsJohan)
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
            fscore = 2 * (precision * recall) / float(precision + recall)
        print(i, fscore)

main()
