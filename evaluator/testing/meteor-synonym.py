#!/usr/bin/env python
import argparse # optparse is deprecated
from itertools import islice # slicing for iterators
import math,sys,copy,nltk
from nltk.util import ngrams
from nltk.corpus import wordnet


#ALPHA = 0.9
#BETA = 3.0
#GAMMA = 0.5

ALPHA = 0.8
BETA = 0.5
GAMMA = 0.3

#This version cannot have more than a unigram (Note)
def synonym(word):
	try:
		syn = wordnet.synsets(word)
		synonyms = []

		for i in syn:
			for j in i.lemmas():
				synonyms += [j.name().encode('ascii')]
		synonyms = list(set(synonyms))
	except:
		return []

	return synonyms


def word_matches(h,ref,ngram):
	sum = 0
	temp_ref = copy.deepcopy(ref)
	temp_h = copy.deepcopy(h)
	new_h = []
	new_ref = []
	
	if ngram > 1:
		temp_h = ngrams(temp_h,ngram)
		temp_ref = ngrams(temp_ref,ngram)
	
	for i in temp_h:
		new_h += [i]
	for j in temp_ref:
		new_ref += [j]

	for i in new_h:
		if i in new_ref:
			new_ref.remove(i)
			sum += 1.0
	
	for i in new_h:
		for j in new_ref:
			if i in synonym(j):
				sum += 1.0
				new_ref.remove(j)
				break
	return sum


def precision(test,ref,ngram):
	length = float(len(test) - ngram + 1)
	x = word_matches(test,ref,ngram)
	if length == 0:
		return 0
	return x/length

def recall(test,ref,ngram):
	length = float(len(ref) - ngram + 1)
	x = word_matches(test,ref, ngram)
	if length == 0:
		return 0
	return x/length

def F_mean(test, ref,alpha):
	p = precision(test,ref,1)
	r = recall(test,ref,1)
	if ((alpha*p) + ((1-alpha)*r)) == 0:
		return 0
	fmean = p*r
	fmean = fmean/((alpha*p) + ((1-alpha)*r))
	return fmean

def chunks(test,ref):
	sum = 0
	test_array = copy.deepcopy(test)
	ref_array = copy.deepcopy(ref)
	newarray = {}
	start = True
	back_ref_pos = 0
	back_test_pos = 0

	traversed = []
	for i in xrange(0,len(test)):
		traversed += [0]


	for iteratei, i in enumerate(ref_array):
		if i in test_array:
			for iteratej,j in enumerate(test_array):
				if i == j or (i in synonym(j)):
					if traversed[iteratej] == 1:
						continue
					traversed[iteratej] = 1
					newarray[iteratei] = (iteratei,j,iteratej)
					break

	for ref_pos, test_value, test_pos in newarray.itervalues():
		if start == True:
			start = False
			back_ref_pos = ref_pos
			back_test_pos = test_pos
			continue
		
		if (ref_pos == back_ref_pos+1) and (test_pos == back_test_pos+1):			
			back_ref_pos = ref_pos
			back_test_pos = test_pos
			continue
		else:
			sum += 1.0
			back_ref_pos = ref_pos
			back_test_pos = test_pos
	sum += 1.0
	return sum



def penalty(test,ref,beta,gamma):
	m = word_matches(test,ref,1)
	c = chunks(test,ref)
	ch = 0 if m==0 else c/m
	return (gamma * math.pow(ch, beta))

def score(test,ref,alpha,beta,gamma):
	return (1-penalty(test,ref,beta,gamma))*F_mean(test,ref,alpha)

def bleu(test,ref):
	mul = 1
	for i in xrange(1,5):
		value = precision(test,ref,i)
		mul *= value
	mul= math.pow(mul,1/4)

	pen = [1,len(ref)/len(test)]
	return min(pen)*mul




def main():
	parser = argparse.ArgumentParser(description='Evaluate translation hypotheses.')
	parser.add_argument('-i', '--input', default='data/hyp1-hyp2-ref', help='input file (default data/hyp1-hyp2-ref)')
	parser.add_argument('-n', '--num_sentences', default=None, type=int, help='Number of hypothesis pairs to evaluate')
	# note that if x == [1, 2, 3], then x[:None] == x[:] == x (copy); no need for sys.maxint
	opts = parser.parse_args()
 
    # we create a generator and avoid loading all sentences into a list
	def sentences():
		with open(opts.input) as f:
			for pair in f:
				yield [sentence.strip().split() for sentence in pair.split(' ||| ')]
 
    # note: the -n option does not work in the original code

	for h1, h2, ref in islice(sentences(), opts.num_sentences):		
		
		h1_match = score(h1,ref,ALPHA,BETA,GAMMA)
		h2_match = score(h2,ref,ALPHA, BETA, GAMMA)
		print(1 if h1_match > h2_match else # \begin{cases}
			(0 if h1_match == h2_match
					else -1)) # \end{cases}
 
# convention to allow import of this file as a module
if __name__ == '__main__':
	main()




