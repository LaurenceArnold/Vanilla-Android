#!/usr/bin/python
import nltk
from nltk.corpus import brown
from nltk import FreqDist
from nltk.tag import UnigramTagger

words = brown.tagged_words(categories='mystery')

# Exercise 2A
print("There are" + " " + str(len(words)) + " " + "words")
print("There are" + " " + str(len(brown.tagged_sents(categories='mystery'))) + " " + "sentences")

# Exercise 2B
print(brown.tagged_words(categories='mystery')[99])
print(brown.tagged_words(categories='mystery')[100])

# Exercise 2C
listOfTags = []
[listOfTags.append(item[1]) for item in words if item[1] not in listOfTags]
print("There are" + " "+ str(len(listOfTags))+ " " + "tags")

# Exercise 2D
listWords = [word[0] for word in words]
listOfWords = nltk.FreqDist(listWords)
print("The top 10 words and their counts are: ", listOfWords.most_common(10))

# Exercise 2E
listWords = [word[1] for word in words]
listOfWords = nltk.FreqDist(listWords)
print("The top 10 POS tags and their counts are: ", listOfWords.most_common(10))