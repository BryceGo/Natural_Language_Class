import os
import random
import sys

local_max = -1

gamma = 1
alpha = 1
beta = 5
count = 0

while(gamma > 0):
	alpha = 1
	while(alpha > 0):
		beta = 5
		while(beta > 0):
			count += 1
			iteration_number = "Iteration Number : " + str(count) + " .....\n"
			output1 = "python default.py -a " + str(alpha) + " -b " + str(beta)+ " -g " + str(gamma) + " > output"
			output2 = "python check.py < output"
			output3 = "python score-evaluation.py < output > results"
			os.system(output1)
			os.system(output2)
			os.system(output3)
			sys.stderr.write(iteration_number)
			
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
			file.close()
			
			out_err1 = "Max value currently is: " + str(local_max) + "\n"
			out_err2 = "Alpha : " + str(curr_a) + "\n"
			out_err3 = "Beta : " + str(curr_b) + "\n"
			out_err4 = "Gamma : " + str(curr_g) + "\n"

			sys.stderr.write(out_err1)
			sys.stderr.write(out_err2)
			sys.stderr.write(out_err3)
			sys.stderr.write(out_err4)

			hill_climb_file = open("hill_results/hill_results_max","w")
			hill_climb_file.write("Maximum Found is: " + str(local_max) + "\n")
			hill_climb_file.write("Alpha is " + str(curr_a) + "\n")
			hill_climb_file.write("Beta is " + str(curr_b) + "\n")
			hill_climb_file.write("Gamma is " + str(curr_g) + "\n")
			hill_climb_file.close()

			beta -= 0.5
		alpha -= 0.05
	gamma -= 0.05
	

