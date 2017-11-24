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

beam_width = 10
distortion_limit = 5
distortion_value = -1


def num_translated(bits):
	x = 0
	for iterate in xrange(0,len(bits)):
		if bits[iterate] == "1":
			x += 1
	return x

def max_value(stack):
	max = None
	for x in stack.itervalues():
		if max == None:
			max = x.logprob
		elif x.logprob > max:
			max = x.logprob
	return max

#def byte_to_string(x,f_length):
#	string = ""
#	for i in xrange(0,f_length):
#		string = string + str(x[i])
#	return string

def eq(state1, state2):
	if state1.lm_state != state2.lm_state2:
		return False
	if state1.end_char != state.end_char:
		return False
	if state1.byte_length != state2.byte_length:
		return False
	return True

def Add(state, stack):
	for i in stack.itervalues():
		if eq(state,i):
			if i.logprob < state.logprob:
				i = state
		else:
			stack[(state.lm_state, state.byte_length, state.end_char)] = state



for f in french:
	hypothesis = namedtuple("hypothesis", "logprob, lm_state, predecessor, phrase, byte_length, end_char")

	byte = ""
	for i in xrange(0,len(f)):
		byte = byte + "0"

	initial_hypothesis = hypothesis(0.0,lm.begin(), None, None, byte, 0)
	byte = None
	stacks = [{} for _ in f] + [{}]
	stacks[0][(lm.begin(),byte,0)] = initial_hypothesis
	for i, stack in enumerate(stacks[:-1]):		
		maxvalue = max_value(stack)
		for h in sorted(stack.itervalues(), key=lambda h: -h.logprob): 
		#for h in sorted(stack.itervalues(), key=lambda h: -h.logprob)[:opts.s]:
#Beam
			if (h.logprob < maxvalue - beam_width):
				break

			for j in xrange(0,len(f)):
				#sys.stderr.write("J Ranges ------------" + str(j) + "\n")
				
				if h.byte_length[j] == "1":
					continue
				if abs(h.end_char + 1 - j) > distortion_limit: #distortion
					break			

				for k in xrange(j,len(f)):
					#sys.stderr.write("K ranges" + str(k) + "\n")
					if h.byte_length[k] == "1":
						break
					if f[j:k+1] in tm:
						for phrase in tm[f[j:k+1]]:
							#sys.stderr.write(str(phrase.english) +  "\n")
							logprob = h.logprob + phrase.logprob + (abs(h.end_char + 1 - j)*distortion_value)
							lm_state = h.lm_state
							for word in phrase.english.split():
								(lm_state,word_logprob) = lm.score(lm_state,word)
								logprob += word_logprob
							logprob += lm.end(lm_state) if num_translated(h.byte_length) == len(f) else 0.0
							
							bit_temp = h.byte_length
							for a in xrange(j,k+1):
								bit_temp = bit_temp[0:a] + "1" + bit_temp[a+1:len(f)]
		
							#if h.end_char > k:
							#	end = h.end_char
							#else:
							#	end = k
							end = k
							new_hypothesis = hypothesis(logprob,lm_state,h,phrase,bit_temp,end)
							
							#Add
							bytes_used = num_translated(bit_temp)

							if (lm_state,bit_temp,end) not in stacks[bytes_used] or stacks[bytes_used][(lm_state,bit_temp,end)].logprob < logprob:
								stacks[bytes_used][(lm_state,bit_temp,end)] = new_hypothesis
							#Add(new_hypothesis, stacks[bytes_used])						
							#if lm_state not in stacks[bytes_used] or stacks[bytes_used][lm_state].logprob < logprob:
							#	stacks[bytes_used][lm_state] = new_hypothesis

	winner = max(stacks[-1].itervalues(), key=lambda h : h.logprob)

	def extract_english(h):
		return "" if h.predecessor is None else "%s%s " %(extract_english(h.predecessor), h.phrase.english)

	print extract_english(winner)
	#sys.stderr.write(str(winner) + "\n")
	#x = num_translated(winner.byte_length)
	#sys.stderr.write(str(x))
	#
#hypothesis = namedtuple("hypothesis", "logprob, lm_state, predecessor, phrase, byte_length, end_char")

		
  # The following code implements a monotone decoding
  # algorithm (one that doesn't permute the target phrases).
  # Hence all hypotheses in stacks[i] represent translations of 
  # the first i words of the input sentence. You should generalize
  # this so that they can represent translations of *any* i words.

if False:
	"""

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
	"""
