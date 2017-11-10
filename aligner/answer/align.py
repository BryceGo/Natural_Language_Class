#!/usr/bin/env python

#Bryce Golamco
#bgolamco@sfu.ca


#This algorithm uses a translation and distortion parameter from the IBM Model 2

import optparse, sys, os, logging
from collections import defaultdict


optparser = optparse.OptionParser()
optparser.add_option("-d", "--datadir", dest="datadir", default="data", help="data directory (default=data)")
optparser.add_option("-p", "--prefix", dest="fileprefix", default="hansards", help="prefix of parallel data files (default=hansards)")
optparser.add_option("-e", "--english", dest="english", default="en", help="suffix of English (target language) filename (default=en)")
optparser.add_option("-f", "--french", dest="french", default="fr", help="suffix of French (source language) filename (default=fr)")
optparser.add_option("-l", "--logfile", dest="logfile", default=None, help="filename for logging output")
optparser.add_option("-t", "--threshold", dest="threshold", default=0.5, type="float", help="threshold for alignment (default=0.5)")
optparser.add_option("-n", "--num_sentences", dest="num_sents", default=sys.maxint, type="int", help="Number of sentences to use for training and alignment")
(opts, _) = optparser.parse_args()
f_data = "%s.%s" % (os.path.join(opts.datadir, opts.fileprefix), opts.french)
e_data = "%s.%s" % (os.path.join(opts.datadir, opts.fileprefix), opts.english)

if opts.logfile:
    logging.basicConfig(filename=opts.logfile, filemode='w', level=logging.INFO)

sys.stderr.write("Training using EM algorithm...")
bitext = [[sentence.strip().split() for sentence in pair] for pair in zip(open(f_data), open(e_data))[:opts.num_sents]]
f_count = defaultdict(int) #Counts for the french word
e_count = defaultdict(int) #Counts for the english word
fe_count = defaultdict(int)

qa_count = defaultdict(int)	#Counts for alignments q(j|i,l,m)
q_count = defaultdict(int) #Counts for alignments q(i,l,m)

#Where j is the alignment number of the english sentence,
#i is the alignment number of the french sentence
#l is the length of the english sentence
#m is the length of the french sentence



t_k = defaultdict(int)
q_k = defaultdict(int)
	

iterations = 10
k = 0
#Initialize the t_k and q_k arrays
sys.stderr.write("\n")
sys.stderr.write("Initializing...")
for(a,(b,c)) in enumerate(bitext):
	for (i,f_i) in enumerate(b):
		for (j,e_j) in enumerate(c):
			t_k[(f_i,e_j)] = 1.0
			q_k[(j,i,len(c),len(b))] = 1.0
	if a%1000 == 0: sys.stderr.write(".")
sys.stderr.write("\n")

sys.stderr.write("Done initializing\n")
sys.stderr.write("Training " +  str(iterations) + " iterations.\n")

#The for loop that implements the EM algorithm (It is defaulted to run for 10 iterations)
while(k < iterations):
	k += 1
	sys.stderr.write("Iteration " + str(k) + "...\n")
	e_count = defaultdict(int)
	fe_count = defaultdict(int)
	
	for (n,(f,e)) in enumerate(bitext):
		for (i,f_i) in enumerate(f):
			Z = 0
			for (j,e_j) in enumerate(e):
				Z += t_k[(f_i,e_j)]*q_k[(j,i,len(e),len(f))]
			
			for (j,e_j) in enumerate(e):
				c = (t_k[(f_i,e_j)]*q_k[(j,i,len(e),len(f))])/Z
				fe_count[(f_i,e_j)] += c
				e_count[e_j] += c
				qa_count[(j,i,len(e),len(f))] += c
				q_count[(i,len(e),len(f))] += c

	for (f,e) in fe_count.keys():
		t_k[(f,e)] = fe_count[(f,e)]/e_count[e]

	for (j,i,l,m) in qa_count.keys():
		q_k[(j,i,l,m)] = qa_count[(j,i,l,m)]/q_count[(i,l,m)]


sys.stderr.write("Training Complete...\n")
sys.stderr.write("Aligning...\n")
#The for loop that searches for the best possible alignment
for (k,(f,e)) in enumerate(bitext):
	for (i,f_i) in enumerate(f):
		bestp = 0
		bestj = 0
		for (j,e_j) in enumerate(e):
			if t_k[(f_i,e_j)]*q_k[(j,i,len(e),len(f))] > bestp: 
				bestp = t_k[(f_i,e_j)]*q_k[(j,i,len(e),len(f))]
				bestj = j
		sys.stdout.write("%i-%i " %(i,bestj))
	sys.stdout.write("\n")

