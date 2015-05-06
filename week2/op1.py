#!/usr/bin/python
import nltk
from nltk.collocations import *
from nltk.util import ngrams
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet

def hypernymOf(synset1, synset2):
    """ True als synset2 een hypernym is van synset1 (of dezelfde synset)"""
    # Lecture slide 43 (week3)
    if (synset1 == synset2):
        return True
    for hypernym in synset1.hypernyms():
        if (synset2 == hypernym):
            return True
        if (hypernymOf(hypernym, synset2)):
            return True
    
    return False
    
def findHypernym(synsetList, current):
    """ Returnt van een lijst synsets de 'hoogste' hypernym """
    if (len(synsetList) == 0):
        return current
    
    listItem = synsetList.pop()
    
    if (hypernymOf(current, listItem)):
        return findHypernym(synsetList, listItem)
    else:
        return findHypernym(synsetList, current)

def main():
    text = open('ada_lovelace.txt').read()
    #source = text.decode("utf-8")
    source = text

    sents = nltk.sent_tokenize(source)
    lemmatizer = WordNetLemmatizer()

    tokens = []
    for sent in sents:
        tokens += nltk.word_tokenize(sent)
    pos_tags = nltk.pos_tag(tokens)
    nouns = [word[0] for word in pos_tags if word[1] == 'NN']

    lemmaList = []
    synsetList = []
    for word in nouns:
        # Lemmatize each word and add to the list of lemma's
        result = lemmatizer.lemmatize(word, wordnet.VERB )
        lemmaList.append(result)
        
        # Retrieve the synsets for each lemma and add to list
        lemmaSynsets = wordnet.synsets(word, pos='n')
        
        if (isinstance(lemmaSynsets, list)):
            synsetList.extend(lemmaSynsets)
        else:
            synsetList.append(lemmaSynsets)

        """
        if (len(lemmaSynsets) > 1):
            synset = findHypernym(lemmaSynsets, lemmaSynsets[0])
        else:
            synset = lemmaSynsets
        
        if not (isinstance(synset, list)):
            synsetList.append(synset)
        """

    # Print results
    print("Lemma\'s:\n", lemmaList)
    print("\n\nSynsets:\n", synsetList)
    
    # Correct synsets to look for:
    relative = wordnet.synsets("relative", pos='n')[0]
    illness = wordnet.synsets("illness", pos='n')[0]
    science = wordnet.synsets("science", pos='n')[0]
    
    """
    Om uit te vinden of we de goede hebben:
    print(relative.definition())
    print(illness.definition())
    print(science.definition())
    """
    
    # Count the hyponyms for 1A
    relativeHypo = []
    illnessHypo = []
    scienceHypo = []
    
    for synset in synsetList:
        if (hypernymOf(synset, relative)):
            relativeHypo.append(synset)
        if (hypernymOf(synset, illness)):
            illnessHypo.append(synset)
        if (hypernymOf(synset, science)):
            scienceHypo.append(synset)
    
    print("1A:\n")
    print("Relatives (" + str(len(relativeHypo)) + "):\n", relativeHypo, "\n")
    print("Illness (" + str(len(illnessHypo)) + "):\n", illnessHypo, "\n")
    print("Science (" + str(len(scienceHypo)) + "):\n", scienceHypo, "\n")

if __name__ == "__main__":
    main()

