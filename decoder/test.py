

variable = []
for i in xrange(0,9):
	variable[i] = []

for i in xrange(0,9):
	for j in xrange(0,9):
		variable[i][j] = 1


for i in xrange(0,9):
	for j in xrange(0,9):
		print(variable[i][j])
