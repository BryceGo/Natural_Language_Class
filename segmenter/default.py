#Bryce Golamco
#bgolamco@sfu.ca


import sys, codecs, optparse, os
import math

optparser = optparse.OptionParser()
optparser.add_option("-c", "--unigramcounts", dest='counts1w', default=os.path.join('data', 'count_1w.txt'), help="unigram counts")
optparser.add_option("-b", "--bigramcounts", dest='counts2w', default=os.path.join('data', 'count_2w.txt'), help="bigram counts")
optparser.add_option("-i", "--inputfile", dest="input", default=os.path.join('data', 'input'), help="input file to segment")
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


	def insert1(self, filename, sep='\t', N=None, missingfn=None):
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
        elif len(key) == 1: return self.missingfn(key, self.N)
        else: return None

class Heap_Im: 		#Heap to store that values of the entries
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


max_size_line = 30 	#Sets the maximum characters in a line (This is differnt from maxlen of an entry)


old = sys.stdout
sys.stdout = codecs.lookup('utf-8')[-1](sys.stdout)
# ignoring the dictionary provided in opts.counts
with open(opts.input) as f:
    for xz in f:
		i = unicode(xz.strip(),'utf-8')
		line_count = 1
		line_size = len(i)
		output_line = ""
		newline = []
	
		line_count1 = 0
		while(line_size > max_size_line):		#This loop segments the line to a maximum of 30 characters, If a line has more than 30 characters it treats that line as more than 1 line depending on the number of characters. This is done so that the program will be able to run in less than a minute
			x = i[line_count1*max_size_line:(line_count1+1)*max_size_line]
			newline = newline + [x]
			line_size = len(i[(line_count1+1)*max_size_line:])
			line_count1 += 1
		
		x = i[line_count1*max_size_line:(line_count1+1)*max_size_line]
		newline = newline + [x]
		line_size = len(i[(line_count1+1)*max_size_line:])
		for line in newline:
			heap1 = Heap_Im()
			utf8line = line
			output = [i for i in utf8line]  # segmentation is one word per character in the input
			temp = ""
			chart = []
			count = 0
			for i in output:							#This initializes the chart 
				chart = chart + [None]
			for i in output:							
				count += 1
				if count > Pw.maxlen:
					break
				temp = temp + i
				if (Pw(temp) != None):
					heap1.insert(temp,0,math.log10(Pw(temp)),None)	#Inserts values into the chart
			while(heap1.size > 0):							#While heap is nonempty cycle through checking the chart if the chart have a bigger probability. Otherwise, the new probability will be changed to the current one.
				newword = ""
				count = 0
				entry = heap1.remove_max()
				endindex = len(entry.word)
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
					if(Pw(newword) != None):
						heap1.insert(newword,entry.pos + endindex,entry.prob + math.log10(Pw(newword)), entry) 	#Adds the new entry
			
				del entry
			finalindex = len(output)
			finalentry = chart[finalindex-1]
			temp = ""
		
			temp = finalentry.word			#Do while loop to iteratively cycle through the answer. The answer first be on the last word, but it will have a pointer pointing to the word before that and so on.. until the whole sentence is outputted.
			while(finalentry.pointer != None):
				finalentry = finalentry.pointer
				temp = finalentry.word + " " + temp


			if(line_count == 1):
				output_line = temp
			else:
				output_line = output_line + " " + temp
			
			line_count += 1
			
			del heap1
			del chart
		print(output_line)

sys.stdout = old























