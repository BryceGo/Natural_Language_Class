
import sys, codecs, optparse, os
import math

optparser = optparse.OptionParser()
optparser.add_option("-c", "--unigramcounts", dest='counts1w', default=os.path.join('data', 'count_1w.txt'), help="unigram counts")
optparser.add_option("-b", "--bigramcounts", dest='counts2w', default=os.path.join('data', 'count_2w.txt'), help="bigram counts")
optparser.add_option("-i", "--inputfile", dest="newinput", default=os.path.join('data', 'newinput'), help="input file to segment")
(opts, _) = optparser.parse_args()

class Pdist(dict):
    "A probability distribution estimated from counts in datafile."

    def __init__(self, filename, sep='\t', N=None, missingfn=None):
        self.maxlen = 0 
        for line in file(filename):
            (key, freq) = line.split(sep)
            try:
                utf8key = unicode(key, 'utf-8')
            except:
                raise ValueError("Unexpected error %s" % (sys.exc_info()[0]))
            self[utf8key] = self.get(utf8key, 0) + int(freq)
            self.maxlen = max(len(utf8key), self.maxlen)
        self.N = float(N or sum(self.itervalues()))
        self.missingfn = missingfn or (lambda k, N: 1./N)

    def __call__(self, key):
        if key in self: return float(self[key])/float(self.N)
        #else: return self.missingfn(key, self.N)
        elif len(key) == 1: return self.missingfn(key, self.N)
        else: return None

class Heap_Im:
	def __init__(self):
		self.size = 0
		self.array_size = 0
		self.heap = []
	def insert(self,word,start_position,log_probability,back_pointer):
		x = Node(word,start_position,log_probability,back_pointer)		
		self.heap += [x]
		self.size += 1
		self.heap_up()
	
	def remove_max(self):
		self.swap(self.size-1, 0)
		temp = self.heap[self.size-1]
		del self.heap[self.size-1]
		self.size -= 1
		self.heap_down()
		return temp
		

	def heap_up(self):
		i = self.size
		while(i > 1):
			if(self.heap[i-1].prob > self.heap[(i/2)-1].prob):
				self.swap(i-1,(i/2)-1)
			i = i/2

	def heap_down(self):
		i = 1
		while (2*i <= self.size):
			child = self.children(i)
			if(self.heap[child - 1].prob > self.heap[i-1].prob):
				self.swap(child -1,i-1)
			else:
				break
			i = child


	def children(self,i): # assumes that there are children
		if((2*i)+1 <= self.size):
			if(self.heap[2*i -1].prob > self.heap[2*i].prob):
				return 2*i
			else:
				return 2*i + 1
		else:
			return 2*i

	def swap(self,i,j):
		tmp1 = self.heap[i]
		self.heap[i] = self.heap[j]
		self.heap[j] = tmp1


	def print_heaplist(self):		
		while (self.size > 0):
			print(self.remove_max().word)


class Node:
	def __init__(self,word,start_position,log_probability,back_pointer):
		self.word = word
		self.pos = start_position
		self.prob = log_probability
		self.pointer = back_pointer
	






# the default segmenter does not use any probabilities, but you could ...
Pw  = Pdist(opts.counts1w)

comma = unicode(",", 'utf-8')





old = sys.stdout
sys.stdout = codecs.lookup('utf-8')[-1](sys.stdout)
# ignoring the dictionary provided in opts.counts
with open(opts.newinput) as f:
    for  line in f:
		heap1 = Heap_Im()
		utf8line = unicode(line.strip(), 'utf-8')
		output = [i for i in utf8line]  # segmentation is one word per character in the input
		temp = ""
		chart = []
		count = 0
		for i in output:			
			chart = chart + [None]						#Initializing the chart

		for i in output:
			count += 1
			if count > Pw.maxlen:
				break
			temp = temp + i
			if (Pw(temp) != None):
				heap1.insert(temp,0,math.log(Pw(temp)),None)
		while(heap1.size > 0):							#While heap is nonempty
			newword = ""
			count = 0
			entry = heap1.remove_max()
			endindex = len(entry.word)
			#print("Word: " + entry.word)
			#print("Position: " + str(entry.pos))
			if(chart[entry.pos + endindex-1] != None):
				if(entry.prob > chart[entry.pos + endindex-1].prob):
					chart[entry.pos + endindex-1] = entry
			else:
				chart[entry.pos + endindex-1] = entry
			
			for i in output[entry.pos + endindex::]:
				count += 1
				if(count > Pw.maxlen):	
					break
				newword = newword + i
				#print(newword)
				if(Pw(newword) != None):
					#print("Newword in for loop: " + newword)
					#print("Endindex in for loop :"+ str(endindex))
					#print(heap1.size)
					heap1.insert(newword,entry.pos + endindex,entry.prob + math.log(Pw(newword)), entry)
					#print(heap1.size)
			
			del entry
		finalindex = len(output)
		finalentry = chart[finalindex-1]
		temp = ""
		
		temp = finalentry.word			#Do while loop
		while(finalentry.pointer != None):
			finalentry = finalentry.pointer
			temp = finalentry.word + " " + temp
		print (temp)
		del heap1
		del chart

		#print " ".join(output)
sys.stdout = old























