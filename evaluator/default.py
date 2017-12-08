#!/usr/bin/env python
import argparse # optparse is deprecated
from itertools import islice # slicing for iterators
import math, sys, copy
from nltk.corpus import wordnet

#ALPHA = 0.5
#BETA = 3.0
#GAMMA = 0.3



def word_matches(h,ref):
	sum = 0
	temp_ref = copy.deepcopy(ref)
	for i in h:
		if i in temp_ref:
			temp_ref.remove(i)
			sum += 1.0
	return sum

def precision(test,ref):
	length = float(len(test))
	x = word_matches(test,ref)
	if length == 0:
		return 0

	return x/length

def recall(test,ref):
	length = float(len(ref))
	x = word_matches(test,ref)
	if length == 0:
		return 0	
	return x/length

def F_mean(test, ref,alpha):
	p = precision(test,ref)
	r = recall(test,ref)
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
				if i == j:
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
	m = word_matches(test,ref)
	c = chunks(test,ref)
	ch = 0 if m==0 else c/m
	return (gamma * math.pow(ch, beta))

def score(test,ref,alpha,beta,gamma):
	return (1-penalty(test,ref,beta,gamma))*F_mean(test,ref,alpha)

def main():
	parser = argparse.ArgumentParser(description='Evaluate translation hypotheses.')
	parser.add_argument('-i', '--input', default='data/hyp1-hyp2-ref', help='input file (default data/hyp1-hyp2-ref)')
	parser.add_argument('-n', '--num_sentences', default=None, type=int, help='Number of hypothesis pairs to evaluate')

	parser.add_argument('-a', '--alpha', default=0.5, type=float, help='Alpha parameter of METEOR')
	parser.add_argument('-b', '--beta', default=3.0, type=float, help='Beta parameter of METEOR')
	parser.add_argument('-g', '--gamma', default=0.3, type=float, help='Gamma parameter of METEOR')
	# note that if x == [1, 2, 3], then x[:None] == x[:] == x (copy); no need for sys.maxint
	
	opts = parser.parse_args()
 	
	ALPHA = opts.alpha
	BETA = opts.beta
	GAMMA = opts.gamma
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




