The translation decoding algorithm used for this homework is based from the lecture notes of Micheal Collins.

It uses a distortion parameter in addition to the default code.

The algorithm is as follows:

Where Qn is a stack with n being the number of n words currently translated. This means the max n is the length of the sentence to be translated.

Inputs: Sentence x1,x2,...,xN.

Initialize set Q0 = {q0}, Qi = NULL for i ... n

For i = 0 ... n-1:
	For each state q in beam(Qi),For each phrase p in ph(q):
		q` = next(q,p)
		Add(Qj,q`,q,p) where j = len(q`)
Return the Highest scoring state in Qn. Backpointers can be used to find the underlying sequence of phrase (and the translation)








