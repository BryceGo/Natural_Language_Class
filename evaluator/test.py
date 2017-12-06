import os
import random
import sys
maximum = -1
max_a = 0
max_b = 0
max_g = 0

curr_a = 0
curr_b = 0
curr_g = 0


for a in xrange(0,20):
	alpha = round(random.uniform(0.5,1),2)
	beta = round(random.uniform(2.5,5),2)
	gamma = round(random.uniform(0.3,1),2)

	INC_ALPHA = 0.1
	INC_BETA = 0.5
	INC_GAMMA = 0.1

	local_max = -1

	for i in xrange(1,4):
		for j in xrange(0,10):

			iteration_number = "Iteration Number : " + str(a) + " .....\n"
			sys.stderr.write(iteration_number)
			sys.stderr.write("Reading Turn ")
			sys.stderr.write(str(i))
			sys.stderr.write(" with iteration number : ")
			sys.stderr.write(str(j))
			sys.stderr.write(" ....................\n")

			output1 = "python default.py -a " + str(alpha) + " -b " + str(beta)+ " -g " + str(gamma) + " > output"
			output2 = "python check.py < output"
			output3 = "python score-evaluation.py < output > results"
			os.system(output1)
			os.system(output2)
			os.system(output3)
			
			file = open("results", "r")

			for line in file:
				continue
			last = line
			last = last.strip()
			last = last.split(" ")

			answer = float(last[2])
			if answer > local_max:
				local_max = answer
				curr_a = alpha
				curr_b = beta
				curr_g = gamma
			else:
				if i == 1:
					INC_ALPHA = -INC_ALPHA/2
				elif i == 2:
					INC_BETA = -INC_BETA/2
				elif i == 3:
					INC_GAMMA = -INC_GAMMA/2

			if i == 1:
				alpha += INC_ALPHA
				alpha = min(alpha,1.0)
				alpha = max(alpha,0)
			elif i == 2:
				beta += INC_BETA
				beta = min(beta,5.0)
				beta = max(beta,0)
			elif i == 3:
				gamma += INC_GAMMA
				gamma = min(gamma, 1.0)
				gamma = max(0,gamma)

			file.close()

	maximum = local_max
	max_a = curr_a
	max_b = curr_b
	max_g = curr_g
	
	hill_climb_file = open("hill_results/hill_results" + str(a),"w")
	hill_climb_file.write("Maximum Found is: " + str(maximum) + "\n")
	hill_climb_file.write("Alpha is " + str(max_a) + "\n")
	hill_climb_file.write("Beta is " + str(max_b) + "\n")
	hill_climb_file.write("Gamma is " + str(max_g) + "\n")
	
	hill_climb_file.close()







