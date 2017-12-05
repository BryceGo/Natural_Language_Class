import os
import random

maximum = 0.0
max_a = 0
max_b = 0
max_g = 0

alpha = round(random.uniform(0,0.9),2)
beta = round(random.uniform(1,4.5),2)
gamma = round(random.uniform(0,0.9),2)


curr_a = 0
curr_b = 0
curr_g = 0
INC_ALPHA = 0.1
INC_BETA = 0.5
INC_GAMMA = 0.1

prev_answer = 0
error = 10000
local_max = -1


i = 1

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
elif i == 2:
	beta += INC_BETA
elif i == 3:
	gamma += INC_GAMMA			

alpha += INC_ALPHA
file.close()
