Bryce Golamco
bgolamco@sfu.ca


The algorithm used was based on the baseline algorithm on the description.
It was:



for t = 1, …, T, for j = 1, …, n
Use the Viterbi algorithm to find the output of the model on the jth training sentence (the function perc_test in perc.py implements the Viterbi algorithm) where Tnj is the set of all tag sequences of length nj


z[1:n]=argmax[1:n]∑wΦ(x(j)[1:nj],u[1:nj])

    If z[1:n]≠t(j)[1:n]

then update the weight vector:

ws=ws+Φs(x(j)[1:nj],t(j)[1:nj])−Φs(x(j)[1:nj],z[1:nj])



The features implemented were features 00 all through 22
The output train was tested through 2 epochs

