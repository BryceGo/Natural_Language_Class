

def num_translated(bits):
	x = 0
	for a in xrange(0,len(bits)):
		if bits[a] == 1:
			x += 1
	return x

b = {}

b[0] = 1
b[7] = 1
b[6] = 1
b[5] = 1
b[4] = 1
b[3] = 1
b[2] = 1

b[8] = 0
b[9] = 0
b[10] = 0


print(num_translated(b))


