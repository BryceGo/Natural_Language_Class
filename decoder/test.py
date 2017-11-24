
j = 2
k = 4
bit_temp = "00000"
for a in xrange(j,k+1):
	bit_temp = bit_temp[0:a] + "1" + bit_temp[a+1:len(bit_temp)]

print(bit_temp)
