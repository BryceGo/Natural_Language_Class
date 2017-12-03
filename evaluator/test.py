import copy

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



ref = ['the','cat','sat','on','the','mat']
hyp = ['the','cat', 'was' ,'sat','on','the','mat']
print(chunks(hyp,ref))












