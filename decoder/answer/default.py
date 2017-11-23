#!/usr/bin/env python
import optparse
import sys
import models
from collections import namedtuple

optparser = optparse.OptionParser()
optparser.add_option("-i", "--input", dest="input", default="data/input", help="File containing sentences to translate (default=data/input)")
optparser.add_option("-t", "--translation-model", dest="tm", default="data/tm", help="File containing translation model (default=data/tm)")
optparser.add_option("-l", "--language-model", dest="lm", default="data/lm", help="File containing ARPA-format language model (default=data/lm)")
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to decode (default=no limit)")
optparser.add_option("-k", "--translations-per-phrase", dest="k", default=1, type="int", help="Limit on number of translations to consider per phrase (default=1)")
optparser.add_option("-s", "--stack-size", dest="s", default=1, type="int", help="Maximum stack size (default=1)")
optparser.add_option("-v", "--verbose", dest="verbose", action="store_true", default=False,  help="Verbose mode (default=off)")
opts = optparser.parse_args()[0]

tm = models.TM(opts.tm,opts.k)
lm = models.LM(opts.lm)
french = [tuple(line.strip().split()) for line in open(opts.input).readlines()[:opts.num_sents]]

# tm should translate unknown words as-is with probability 1
for word in set(sum(french,())):
  if (word,) not in tm:
    tm[(word,)] = [models.phrase(word, 0.0)]

sys.stderr.write("Decoding %s...\n" % (opts.input,))

beam_width = 1000


def max_value(stack):
	max = None
	for x in stack.itervalues():
		if max == None:
			max = x.logprob
		elif x.logprob > max:
			max = x.logprob
	return max
		
def extract_english(h):
	return "" if h.predecessor is None else "%s%s " %(extract_english(h.predecessor), h.phrase.english)


for f in french:
	hypothesis = namedtuple("hypothesis", "logprob, lm_state, predecessor, phrase, byte_length, end_char")

	byte = {}	
	for i,_ in enumerate(f):
		byte[i] = 0 
	initial_hypothesis = hypothesis(0.0,lm.begin(), None, None, byte, 0)
	byte = None
	stacks = [{} for _ in f] + [{}]
	stacks[0][lm.begin()] = initial_hypothesis
	for i, stack in enumerate(stacks[:-1]):
		#maxvalue = int(max(stack.itervalues(),key=lambda h: h.logprob))		
		maxvalue = max_value(stack)
		for h in sorted(stack.itervalues(), key=lambda h: -h.logprob): #Beam
			if (h.logprob < maxvalue - beam_width):
				break
			for j in xrange(i+1,len(f) + 1):
				
				#Next
				if f[i:j] in tm:
					for phrase in tm[f[i:j]]:
						logprob = h.logprob + phrase.logprob
						lm_state = h.lm_state
					for word in phrase.english.split():
						(lm_state,word_logprob) = lm.score(lm_state, word)
						logprob += word_logprob
					logprob += lm.end(lm_state) if j == len(f) else 0.0
					new_hypothesis = hypothesis(logprob,lm_state,h,phrase)

					#Add
					if lm_state not in stacks[j] or stacks[j][lm_state].logprob < logprob:
						stacks[j][lm_state] = new_hypothesis
	winner = max(stacks[-1].itervalues(), key=lambda h : h.logprob)
	print extract_english(winner)
			
  # The following code implements a monotone decoding
  # algorithm (one that doesn't permute the target phrases).
  # Hence all hypotheses in stacks[i] represent translations of 
  # the first i words of the input sentence. You should generalize
  # this so that they can represent translations of *any* i words.
