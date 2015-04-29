#!/usr/bin/python
import nltk
from nltk.collocations import *
from nltk.util import ngrams

text = open('holmes.txt').read()
tokens = nltk.wordpunct_tokenize(text)

#exercise 1A:
charactertypes = nltk.FreqDist(text)
keys = charactertypes.keys()
keys.sort()
print(keys)
print ("there are" + " " + str(len(charactertypes.keys())) + " " + "character types")

#exercise 1B:
wordtypes = nltk.FreqDist(tokens)
keys2 = wordtypes.keys()
keys2.sort()
print(keys2)
print("There are" + " " + str(len(wordtypes.keys())) + " " + "word types")

#exercise 1C:
unigramschr = list(ngrams(text,1))
most_common_unigramchr = nltk.FreqDist(unigramschr)
answer1 = most_common_unigramchr.most_common(20)
print("Top 20 character-level unigrams, ordered by descending frequency: ", answer1)

bigramschr = list(ngrams(text,2))
most_common_bigramschr = nltk.FreqDist(bigramschr)
answer2 = most_common_bigramschr.most_common(20)
print("Top 20 character-level bigrams, ordered by descending frequency: ", answer2)

trigramchr = list(ngrams(text,3))
most_common_trigramchr = nltk.FreqDist(trigramchr)
answer3 = most_common_trigramchr.most_common(20)
print("Top 20 character-level trigrams, ordered by descending frequency: ", answer3)

# exercise 1D:
unigrams = list(ngrams(tokens,1))
most_common_unigrams = nltk.FreqDist(unigrams)
answera = most_common_unigrams.most_common(20)
print("Top 20 word-level unigrams, ordered by descending frequency:", answera)

bigrams = list(ngrams(tokens,2))
most_common_bigrams = nltk.FreqDist(bigrams)
answerb = most_common_bigrams.most_common(20)
print("Top 20 word-level bigrams, ordered by descending frequency:", answerb)

trigrams = list(ngrams(tokens,3))
most_common_trigrams= nltk.FreqDist(trigrams)
answerc = most_common_trigrams.most_common(20)
print("Top 20 word-level trigrams, ordered by descending frequency:", answerc)

# Exercise 2A:
bigram_measures = nltk.collocations.BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(tokens)
scored = finder.score_ngrams(bigram_measures.raw_freq)
sorted1 = sorted(bigram for bigram, score in scored)
PMI= finder.nbest(bigram_measures.pmi, 20)
print("the most likely 20 collocations using PMI: ", PMI)
Square = finder.nbest(bigram_measures.chi_sq,20)
print("the most likely 20 collocations using x2: ", Square)
