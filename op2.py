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
print(words[99])
print(words[100])

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

# Exercise 2F
# dus [0] is het woord, [1] is de POS-tag die wordt meegegeven
adverbs = [word[0] for word in words if word[1] == 'RB']
result = nltk.FreqDist(adverbs)
print("There are ", str(len(result)), "words with the RB-tag")
print("The most common are: ", result.most_common(1))

#Exercise 2G:
adjectiv = [word[0] for word in words if word[1] == 'JJ']
result2 = nltk.FreqDist(adjectiv)
print("There are: ", str(len(result2)), "words with the JJ-tag")
print("The most common are ", result2.most_common(1))
