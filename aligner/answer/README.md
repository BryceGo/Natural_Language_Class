Bryce Golamco
bgolamco@sfu.ca


The algorithm used to solve this alignment problem is the EM algorithm that was shown in the slides.
This python script is based off of the IBM Model 2 which has a translation parameter and a distortion parameter.

The algorithm of the IBM Model 2 is quite similar to the IBM model 1 and is as follows:

where t_k is the array of the translation parameter
where q_k is the array of the distortion parameter
where l is the length of the english sentence
where m is the length of the french sentence


k = 0
Initialize t_k
Initialize q_k

repeat iterations:
	k += 1
	for each (french,english) in sentences:
		for each f in french:
			Z = 0
			for each e in english:
				Z += t_k(f|e)*q_k(e|f,l,m) #Note that it is the translation parameter multiplied by the distortion parameter
			for each e in english:
				c = t_k(f|e)*q_k(e|f,l,m)
				count(f,e) += c
				count(e) += c
				count(e|f,l,m) += c
				count(f,l,m) += c
	for each(f,e) in count:
		Set t_k(f|e) = count(f,e)/count(e)
	for each q_k(e|f,l,m) in count:
		Set q_k(e|f,l,m) = count(e|f,l,m)/count(f,l,m)




Finding the maximum alignment is to simply iterate through all possible alignments in the sentence and return the maximum one. 
(It is the default argmax algorithm given) Which is:



for each (french,english) in sentences:
	for each f in french:
		bestp = 0
		bestj = 0
		for each e in english:
			if t(f|e) > bestp:
				bestp = t(f|e)
				bestj = j
		align f to e_bestj















