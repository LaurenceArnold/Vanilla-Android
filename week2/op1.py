#!/usr/bin/python
import nltk
from nltk.collocations import *
from nltk.util import ngrams
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
import operator

def hypernymOf(synset1, synset2):
    """ True als synset2 een hypernym is van synset1 (of dezelfde synset)"""
    # Lecture slide 43 (week3), assignment 1.1
    if (synset1 == synset2):
        return True
    for hypernym in synset1.hypernyms():
        if (synset2 == hypernym):
            return True
        if (hypernymOf(hypernym, synset2)):
            return True
    
    return False

def twiceUp(syn):
    # assigment 1.2
    hyperSyn = syn.hypernyms()
    
    if (isinstance(hyperSyn, list)):
        if (hyperSyn):
            return hyperSyn[0].hypernyms()
    else:
        return hyperSyn.hypernyms()
    
def findHypernym(currentSynset, highLevelNoun):
    """ 
    For lack of a better solution.. :')
    Als iemand hier een slimmere suggestie heeft hoor ik 't graag haha
    """
    # assignment 1.2
    print("Current synset: ", currentSynset)
    if (isinstance(currentSynset, list)):
        print("Hypernym of ^: ", currentSynset[0].hypernyms())
    else:
        print("Hypernym of ^: ", currentSynset.hypernyms())
    print("High level noun: ", highLevelNoun)
    
    if not (isinstance(currentSynset, list)):
        tempList = []
        tempList.append(currentSynset)
        currentSynset = tempList
    
    for syn in currentSynset:
        if ((syn.hypernyms() == syn.root_hypernyms()) or (highLevelNoun)):
            # We zitten op 't 1-na-hoogste niveau
            highLevelNoun = currentSynset
            print(highLevelNoun[0].definition())
            return highLevelNoun
        
        return findHypernym(syn.hypernyms(), highLevelNoun)
    
def getMaxSim(synsets1, synsets2):
    """ From slides """
    # assignment 1.3
    
    maxSim = None
    for syn1 in synsets1:
        for syn2 in synsets2:
            sim = syn1.lch_similarity(syn2)
            if ((maxSim == None) or (maxSim < sim)):
                maxSim = sim
    
    return maxSim

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
    
    # Assignment 1.1:
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
    
    print("1.1:\n")
    print("Relatives (" + str(len(relativeHypo)) + "):\n", relativeHypo, "\n")
    print("Illness (" + str(len(illnessHypo)) + "):\n", illnessHypo, "\n")
    print("Science (" + str(len(scienceHypo)) + "):\n", scienceHypo, "\n")
    
    # Assignment 1.2:
    
    print("\n\n\n")
    for synset in synsetList:
        #print(findHypernym(synset, ""))
        print(twiceUp(synset))
    
    # De functie findHypernym() vindt steeds het 1-na-hoogste resultaat,
    # maar in tegenstelling tot wat de slides zeggen zijn dat niet die
    # top level nouns. Die zitten vele malen lager. Functie twiceUp() gaat
    # 2 levels omhoog. Soms is dat goed, soms niet hoog genoeg. Iemand een
    # tactische manier om altijd t goede niveau te bereiken?
    
    # Assignment 1.3:
    carSyns = wordnet.synsets("car", pos='n')
    autoSyns = wordnet.synsets("automobile", pos='n')
    coastSyns = wordnet.synsets("coast", pos='n')
    shoreSyns = wordnet.synsets("shore", pos='n')
    foodSyns = wordnet.synsets("food", pos='n')
    fruitSyns = wordnet.synsets("fruit", pos='n')
    journeySyns = wordnet.synsets("journey", pos='n')
    monkSyns = wordnet.synsets("monk", pos='n')
    slaveSyns = wordnet.synsets("slave", pos='n')
    moonSyns = wordnet.synsets("moon", pos='n')
    stringSyns = wordnet.synsets("string", pos='n')
    
    simDict = {"car <> auto: ": getMaxSim(carSyns, autoSyns),
    "coast <> shore: ": getMaxSim(coastSyns, shoreSyns), 
    "food <> fruit: ": getMaxSim(foodSyns, fruitSyns), 
    "journey <> car: ": getMaxSim(journeySyns, carSyns), 
    "monk <> slave: ": getMaxSim(monkSyns, slaveSyns),
    "moon <> string: ": getMaxSim(moonSyns, stringSyns)}
    
    sortDesc = sorted(simDict.items(), key=operator.itemgetter(1), reverse=True)
    
    [print(sim[0], sim[1]) for sim in sortDesc]
    
    

if __name__ == "__main__":
    main()

