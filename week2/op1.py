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
    
def findHypernym(currentSynset, highLevelNoun):
    """ 
    For lack of a better solution.. :')
    Als iemand hier een slimmere suggestie heeft hoor ik 't graag haha
    """
    if not (isinstance(currentSynset, list)):
        tempList = []
        tempList.append(currentSynset)
        currentSynset = tempList
    
    for syn in currentSynset:
        if ((syn.hypernyms() == syn.root_hypernyms()) or (highLevelNoun)):
            # We zitten op 't 1-na-hoogste niveau
            highLevelNoun = currentSynset
            return highLevelNoun
        
        return findHypernym(syn.hypernyms(), highLevelNoun)
    
   

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
        print(findHypernym(synset, ""))
        
    # Dit resultaat is niet bepaald waar we naar op zoek zijn haha, ze
    # vallen allemaal niet onder de categorieen uit de slides. Zal wel
    # een klein foutje in de code zitten of 't is de compleet verkeerde
    # aanpak. Morgen weer een dag.

if __name__ == "__main__":
    main()

