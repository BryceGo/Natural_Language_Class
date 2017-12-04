import copy
from nltk.util import ngrams
from nltk.corpus import wordnet


def synonym(word):
	syn = wordnet.synsets(word)
	synonyms = []

	for i in syn:
		for j in i.lemmas():
			synonyms += [j.name().encode('ascii')]
	synonyms = list(set(synonyms))
	return synonyms

print(synonym("crying"))






