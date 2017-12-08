#!/usr/bin/env python
import argparse # optparse is deprecated
from itertools import islice # slicing for iterators
import math,sys,copy,nltk
from nltk.util import ngrams

#ALPHA = 0.5
#BETA = 3.0
#GAMMA = 0.3



def word_matches(h,ref,ngram):
	sum = 0
	temp_ref = copy.deepcopy(ref)
	temp_h = copy.deepcopy(h)
	if ngram > 1:
		temp_h = ngrams(temp_h,ngram)
		temp_ref = ngrams(temp_ref,ngram)

	new_h = []
	new_ref = []
	for i in temp_h:
		new_h += [i]
	for j in temp_ref:
		new_ref += [j]

	for i in new_h	:
		if i in new_ref:
			new_ref.remove(i)
			sum += 1.0
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

def F_mean(test, ref,alpha,ngram):
	p = precision(test,ref,ngram)
	r = recall(test,ref,ngram)
	if ((alpha*p) + ((1-alpha)*r)) == 0:
		return 0
	fmean = p*r
	fmean = fmean/((alpha*p) + ((1-alpha)*r))
	return fmean

def chunks(test,ref,ngram):
	sum = 0
	test_array = copy.deepcopy(test)
	ref_array = copy.deepcopy(ref)
	newarray = {}
	start = True
	back_ref_pos = 0
	back_test_pos = 0
	
	if ngram > 1:
		test_array = ngrams(test_array,ngram)
		ref_array = ngrams(ref_array,ngram)
	

	new_test = []
	new_ref = []
	for i in test_array:
		new_test += [i]
	for j in ref_array:
		new_ref += [j]

	test_array = new_test
	ref_array = new_ref	
	
	traversed = []
	for i in xrange(0,len(test_array)):
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



def penalty(test,ref,beta,gamma,ngram):
	m = word_matches(test,ref,ngram)
	c = chunks(test,ref,ngram)
	ch = 0 if m==0 else c/m
	return (gamma * math.pow(ch, beta))


def score(test,ref,alpha,beta,gamma):
	sum = 0
	for i in xrange(1,5):		
		sum += (1-penalty(test,ref,beta,gamma,i))*F_mean(test,ref,alpha,i)
	return sum

def main():
	parser = argparse.ArgumentParser(description='Evaluate translation hypotheses.')
	parser.add_argument('-i', '--input', default='data/hyp1-hyp2-ref', help='input file (default data/hyp1-hyp2-ref)')
	parser.add_argument('-n', '--num_sentences', default=None, type=int, help='Number of hypothesis pairs to evaluate')

	parser.add_argument('-a', '--alpha', default=0.8, type=float, help='Alpha parameter of METEOR')
	parser.add_argument('-b', '--beta', default=0.5, type=float, help='Beta parameter of METEOR')
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
		#h1_match = bleu(h1,ref)
		#h2_match = bleu(h2,ref)
		h1_match = score(h1,ref,ALPHA,BETA,GAMMA)
		h2_match = score(h2,ref,ALPHA, BETA, GAMMA)


		print(1 if h1_match > h2_match else # \begin{cases}
			(0 if h1_match == h2_match
					else -1)) # \end{cases}
 
# convention to allow import of this file as a module
if __name__ == '__main__':
	main()




