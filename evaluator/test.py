import copy
from nltk.util import ngrams
def word_matches(h,ref,ngram):
	sum = 0
	temp_ref = copy.deepcopy(ref)
	temp_h = copy.deepcopy(h)
	temp_h = ngrams(temp_h,ngram)
	temp_ref = ngrams(temp_ref,ngram)

	new_h = []
	new_ref = []
	for i in temp_h:
		new_h += [i]
	for j in temp_ref:
		new_ref += [j]

	print(new_h)
	print(new_ref)

	for i in new_h	:
		if i in new_ref:
			new_ref.remove(i)
			sum += 1.0
	return sum

a = 'Israeli officials are responsible for airport security'
b = 'airport security Israeli officials are responsible'
a = a.split(' ')
b = b.split(' ')
#a = [1,2,3,4,5]
#b = [1,2,4,5,6,7]

print(word_matches(a,b,2))





