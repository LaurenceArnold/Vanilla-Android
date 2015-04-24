#!/usr/bin/python
import nltk
from nltk.corpus import brown
from nltk import FreqDist
from nltk.tag import UnigramTagger

words = brown.tagged_words(categories='mystery')

# Exercise 2A
print(len(words)) #57169
print(len(brown.tagged_sents(categories='mystery'))) #3886

# Exercise 2B
print(brown.tagged_words(categories='mystery')[99]) # I, PPSS
print(brown.tagged_words(categories='mystery')[100]) # Suddenly, RB

# Exercise 2C
listOfTags = []
[listOfTags.append(item[1]) for item in words if item[1] not in listOfTags]
print(len(listOfTags)) # 169 tags

# Exercise 2D
