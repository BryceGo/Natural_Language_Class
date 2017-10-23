"""

You have to write the perc_train function that trains the feature weights using the perceptron algorithm for the CoNLL 2000 chunking task.

Each element of train_data is a (labeled_list, feat_list) pair. 

Inside the perceptron training loop:

    - Call perc_test to get the tagging based on the current feat_vec and compare it with the true output from the labeled_list

    - If the output is incorrect then we have to update feat_vec (the weight vector)

    - In the notation used in the paper we have w = w_0, w_1, ..., w_n corresponding to \phi_0(x,y), \phi_1(x,y), ..., \phi_n(x,y)

    - Instead of indexing each feature with an integer we index each feature using a string we called feature_id

    - The feature_id is constructed using the elements of feat_list (which correspond to x above) combined with the output tag (which correspond to y above)

    - The function perc_test shows how the feature_id is constructed for each word in the input, including the bigram feature "B:" which is a special case

    - feat_vec[feature_id] is the weight associated with feature_id

    - This dictionary lookup lets us implement a sparse vector dot product where any feature_id not used in a particular example does not participate in the dot product

    - To save space and time make sure you do not store zero values in the feat_vec dictionary which can happen if \phi(x_i,y_i) - \phi(x_i,y_{perc_test}) results in a zero value

    - If you are going word by word to check if the predicted tag is equal to the true tag, there is a corner case where the bigram 'T_{i-1} T_i' is incorrect even though T_i is correct.

"""

import perc
import sys, optparse, os
from collections import defaultdict


def train_tags(train):
	output = []
	i = 0
	while(i < len(train)):
		x = train[i].split()
		output.append(x[2])
		i = i + 1
	return output

def word_list(train):
	output = []
	i = 0
	while(i < len(train)):
		x = train[i].split()
		output.append(x[0])
		i = i + 1
	return output

def pos_list(train):
	output = []
	i = 0
	while(i < len(train)):
		x = train[i].split()
		output.append(x[1])
		i = i + 1
	return output

def add_one_feat(feat_vec,key_z,key_true):
	if key_z != None:	
		if feat_vec[key_z] != None:
			feat_vec[key_z] -= 1
			#if feat_vec[key_z] <= 0:
			#	feat_vec.pop(key_z)
	if key_true != None:
		if feat_vec[key_true] == None:
			feat_vec[key_true] = 1
		else:
			feat_vec[key_true] += 1
	return

def strip(feat_vec):
	items_to_pop = []

	for i in feat_vec:
		if feat_vec[i] <= 0:
			items_to_pop.append(i)
	
	for i in range(0,len(items_to_pop)):
		feat_vec.pop(items_to_pop[i])

#Every Feat function uses the feature that ranges from feat_00 to feat_22
def feat_00(feat_vec,word_list,pos_list,tag_list,z_list,position):
	if ((position - 2) < 0):
		return

	if(tag_list[position-2] != z_list[position-2]):
		key_z = ("U00:" + word_list[position-2], z_list[position-2])
		key_true = ("U00:" + word_list[position-2], tag_list[position-2])
	
		add_one_feat(feat_vec,key_z,key_true)


def feat_01(feat_vec,word_list,pos_list,tag_list,z_list,position):
	if ((position - 1) < 0):
		return

	if(tag_list[position-1] != z_list[position-1]):
		key_z = ("U01:" + word_list[position-1], z_list[position-1])
		key_true = ("U01:" + word_list[position-1], tag_list[position-1])
	
		add_one_feat(feat_vec,key_z,key_true)

def feat_02(feat_vec,word_list,pos_list,tag_list,z_list,position):
	if(tag_list[position] != z_list[position]):
		key_z = ("U02:" + word_list[position], z_list[position])
		key_true = ("U02:" + word_list[position], tag_list[position])
		
		add_one_feat(feat_vec,key_z,key_true)
	return

def feat_03(feat_vec,word_list,pos_list,tag_list,z_list,position):
	if ((position + 1) > len(z_list) - 1):
		return

	if(tag_list[position+1] != z_list[position+1]):
		key_z = ("U03:" + word_list[position+1], z_list[position+1])
		key_true = ("U03:" + word_list[position+1], tag_list[position+1])
	
		add_one_feat(feat_vec,key_z,key_true)

def feat_04(feat_vec,word_list,pos_list,tag_list,z_list,position):
	if ((position + 2) > len(z_list) - 1):
		return

	if(tag_list[position+2] != z_list[position+2]):
		key_z = ("U04:" + word_list[position+2], z_list[position+2])
		key_true = ("U04:" + word_list[position+2], tag_list[position+2])
	
		add_one_feat(feat_vec,key_z,key_true)

def feat_05(feat_vec,word_list,pos_list,tag_list,z_list,position):

	offset = 1
	if ((position - offset) < 0):
		return

	if(tag_list[position -offset] == tag_list[position]):
		if(z_list[position -offset] == z_list[position]):
			if(z_list[position] != tag_list[position]):
				key_z = ("U05:" + word_list[position-1] + "/" + word_list[position], z_list[position])
				key_true = ("U05:" + word_list[position-1] + "/" + word_list[position], tag_list[position])
				add_one_feat(feat_vec,key_z,key_true)
		else:	
			key_z1 = ("U05:" + word_list[position-1] + "/" + word_list[position], z_list[position-1])
			key_z2 = ("U05:" + word_list[position-1] + "/" + word_list[position], z_list[position])		
			key_true = ("U05:" + word_list[position-1] + "/" + word_list[position], tag_list[position])
			add_one_feat(feat_vec,key_z1,key_true)
			add_one_feat(feat_vec,key_z2,key_true)
			add_one_feat(feat_vec,None,key_true)

def feat_06(feat_vec,word_list,pos_list,tag_list,z_list,position):

	if ((position + 1) > len(z_list) - 1):
		return

	if(tag_list[position +1] == tag_list[position]):
		if(z_list[position +1] == z_list[position]):
			if(z_list[position] != tag_list[position]):
				key_z = ("U06:" + word_list[position] + "/" + word_list[position+1], z_list[position])
				key_true = ("U06:" + word_list[position] + "/" + word_list[position+1], tag_list[position])
				add_one_feat(feat_vec,key_z,key_true)
		else:			
			key_z1 = ("U06:" + word_list[position] + "/" + word_list[position+1], z_list[position])
			key_z2 = ("U06:" + word_list[position] + "/" + word_list[position+1], z_list[position+1])
			key_true = ("U06:" + word_list[position] + "/" + word_list[position+1], tag_list[position])
			add_one_feat(feat_vec,key_z1,key_true)
			add_one_feat(feat_vec,key_z2,key_true)
			add_one_feat(feat_vec,None,key_true)



def feat_10(feat_vec,word_list,pos_list,tag_list,z_list,position):
	if((position -2) < 0):
		return

	if(tag_list[position-2] != z_list[position-2]):
		key_z = ("U10:" + pos_list[position-2], z_list[position-2])
		key_true = ("U10:" + pos_list[position-2], tag_list[position-2])
		add_one_feat(feat_vec,key_z,key_true)



def feat_11(feat_vec,word_list,pos_list,tag_list,z_list,position):
	if((position -1) < 0):
		return

	if(tag_list[position-1] != z_list[position-1]):
		key_z = ("U11:" + pos_list[position-1], z_list[position-1])
		key_true = ("U11:" + pos_list[position-1], tag_list[position-1])
		add_one_feat(feat_vec,key_z,key_true)



def feat_12(feat_vec,word_list,pos_list,tag_list,z_list,position):

	if(tag_list[position] != z_list[position]):
		key_z = ("U12:" + pos_list[position] + "q", z_list[position])
		key_true = ("U12:" + pos_list[position] + "q", tag_list[position])
		add_one_feat(feat_vec,key_z,key_true)


def feat_13(feat_vec,word_list,pos_list,tag_list,z_list,position):
	if((position +1) > len(z_list) - 1):
		return

	if(tag_list[position+1] != z_list[position+1]):
		key_z = ("U13:" + pos_list[position+1], z_list[position+1])
		key_true = ("U13:" + pos_list[position+1], tag_list[position+1])
		add_one_feat(feat_vec,key_z,key_true)

def feat_14(feat_vec,word_list,pos_list,tag_list,z_list,position):
	if((position +2) > len(z_list) - 1):
		return

	if(tag_list[position+2] != z_list[position+2]):
		key_z = ("U14:" + pos_list[position+2], z_list[position+2])
		key_true = ("U14:" + pos_list[position+2], tag_list[position+2])
		add_one_feat(feat_vec,key_z,key_true)

def feat_15(feat_vec,word_list,pos_list,tag_list,z_list,position):

	if ((position - 2) < 0):
		return

	if(tag_list[position -2] == tag_list[position-1]):
		if(z_list[position -2] == z_list[position-1]):
			if(z_list[position-1] != tag_list[position-1]):
				key_z = ("U15:" + pos_list[position-2] + "/" + pos_list[position-1], z_list[position-1])
				key_true = ("U15:" + pos_list[position-2] + "/" + pos_list[position-1], tag_list[position-1])
				add_one_feat(feat_vec,key_z,key_true)
		else:		
			key_z1 = ("U15:" + pos_list[position-2] + "/" + pos_list[position-1], z_list[position-2])		
			key_z2 = ("U15:" + pos_list[position-2] + "/" + pos_list[position-1], z_list[position-1])	
			key_true = ("U15:" + pos_list[position-2] + "/" + pos_list[position-1], tag_list[position-1])
			add_one_feat(feat_vec,None,key_true)
			add_one_feat(feat_vec,key_z1,None)
			add_one_feat(feat_vec,key_z2,None)


def feat_16(feat_vec,word_list,pos_list,tag_list,z_list,position):

	if ((position - 1) < 0):
		return

	if(tag_list[position -1] == tag_list[position]):
		if(z_list[position -1] == z_list[position]):
			if(z_list[position] != tag_list[position]):
				key_z = ("U16:" + pos_list[position-1] + "/" + pos_list[position], z_list[position])
				key_true = ("U16:" + pos_list[position-1] + "/" + pos_list[position], tag_list[position])
				add_one_feat(feat_vec,key_z,key_true)
		else:		
			key_z1 = ("U16:" + pos_list[position-1] + "/" + pos_list[position], z_list[position-1])	
			key_z2 = ("U16:" + pos_list[position-1] + "/" + pos_list[position], z_list[position])
			key_true = ("U16:" + pos_list[position-1] + "/" + pos_list[position], tag_list[position])
			add_one_feat(feat_vec,None,key_true)
			add_one_feat(feat_vec,key_z1,None)
			add_one_feat(feat_vec,key_z2,None)


def feat_17(feat_vec,word_list,pos_list,tag_list,z_list,position):

	if ((position + 1) > len(z_list) - 1):
		return

	if(tag_list[position] == tag_list[position+1]):
		if(z_list[position] == z_list[position+1]):
			if(z_list[position] != tag_list[position]):
				key_z = ("U17:" + pos_list[position] + "/" + pos_list[position+1], z_list[position])
				key_true = ("U17:" + pos_list[position] + "/" + pos_list[position+1], tag_list[position])
				add_one_feat(feat_vec,key_z,key_true)
		else:
			key_z1 = ("U17:" + pos_list[position] + "/" + pos_list[position+1], z_list[position])
			key_z2 = ("U17:" + pos_list[position] + "/" + pos_list[position+1], z_list[position+1])
			key_true = ("U17:" + pos_list[position] + "/" + pos_list[position+1], tag_list[position])

			add_one_feat(feat_vec,key_z1,None)
			add_one_feat(feat_vec,key_z2,None)			
			add_one_feat(feat_vec,None,key_true)

def feat_18(feat_vec,word_list,pos_list,tag_list,z_list,position):

	if ((position + 2) > len(z_list) - 1):
		return

	if(tag_list[position+1] == tag_list[position+2]):
		if(z_list[position+1] == z_list[position+2]):
			if(z_list[position+1] != tag_list[position+1]):
				key_z = ("U18:" + pos_list[position+1] + "/" + pos_list[position+2], z_list[position+1])
				key_true = ("U18:" + pos_list[position+1] + "/" + pos_list[position+2], tag_list[position+1])
				add_one_feat(feat_vec,key_z,key_true)
		else:			
			key_z1 = ("U18:" + pos_list[position+1] + "/" + pos_list[position+2], z_list[position+1])
			key_z2 = ("U18:" + pos_list[position+1] + "/" + pos_list[position+2], z_list[position+2])

			key_true = ("U18:" + pos_list[position+1] + "/" + pos_list[position+2], tag_list[position+1])
			add_one_feat(feat_vec,key_z1,None)
			add_one_feat(feat_vec,key_z2,None)
			add_one_feat(feat_vec,None,key_true)


def feat_20(feat_vec,word_list,pos_list,tag_list,z_list,position):
	if((position -2 ) < 0):
		return

	if((tag_list[position-2] == tag_list[position-1]) and (tag_list[position-1] == tag_list[position])):
		if((z_list[position-2] == z_list[position-1]) and (z_list[position-1] == z_list[position])):
			if(z_list[position] != tag_list[position]):
				key_z = ("U20:" + pos_list[position-2] + "/" + pos_list[position-1] + "/" + pos_list[position], z_list[position])
				key_true = ("U20:" + pos_list[position-2] + "/" + pos_list[position-1] + "/" + pos_list[position], tag_list[position])
				add_one_feat(feat_vec,key_z,key_true)
		else:
			key_z1 = ("U20:" + pos_list[position-2] + "/" + pos_list[position-1] + "/" + pos_list[position], z_list[position-2])
			key_z2 = ("U20:" + pos_list[position-2] + "/" + pos_list[position-1] + "/" + pos_list[position], z_list[position-1])
			key_z3 = ("U20:" + pos_list[position-2] + "/" + pos_list[position-1] + "/" + pos_list[position], z_list[position])
			key_true = ("U20:" + pos_list[position-2] + "/" + pos_list[position-1] + "/" + pos_list[position], tag_list[position])
			add_one_feat(feat_vec,key_z1,None)
			add_one_feat(feat_vec,key_z2,None)
			add_one_feat(feat_vec,key_z3,None)
			add_one_feat(feat_vec,None,key_true)


def feat_21(feat_vec,word_list,pos_list,tag_list,z_list,position):
	if ((position - 1) < 0):
		return

	if ((position + 1) > len(z_list) - 1):
		return

	if((tag_list[position-1] == tag_list[position]) and (tag_list[position] == tag_list[position+1])):
		if((z_list[position-1] == z_list[position]) and (z_list[position] == z_list[position+1])):
			if(z_list[position] != tag_list[position]):
				key_z = ("U21:" + pos_list[position-1] + "/" + pos_list[position] + "/" + pos_list[position+1], z_list[position])
				key_true = ("U21:" + pos_list[position-1] + "/" + pos_list[position] + "/" + pos_list[position+1], tag_list[position])
				add_one_feat(feat_vec,key_z,key_true)
		else:
			key_z1 = ("U21:" + pos_list[position-1] + "/" + pos_list[position] + "/" + pos_list[position+1], z_list[position-1])
			key_z2 = ("U21:" + pos_list[position-1] + "/" + pos_list[position] + "/" + pos_list[position+1], z_list[position])
			key_z3 = ("U21:" + pos_list[position-1] + "/" + pos_list[position] + "/" + pos_list[position+1], z_list[position+1])
			key_true = ("U21:" + pos_list[position-1] + "/" + pos_list[position] + "/" + pos_list[position+1], tag_list[position])
	
			add_one_feat(feat_vec,key_z1,None)
			add_one_feat(feat_vec,key_z2,None)
			add_one_feat(feat_vec,key_z3,None)
			add_one_feat(feat_vec,None,key_true)

def feat_22(feat_vec,word_list,pos_list,tag_list,z_list,position):
	if((position +2 ) > len(z_list) - 1):
		return

	if((tag_list[position] == tag_list[position+1]) and (tag_list[position+2] == tag_list[position])):
		if((z_list[position] == z_list[position+1]) and (z_list[position+2] == z_list[position])):
			if(z_list[position] != tag_list[position]):
				key_z = ("U22:" + pos_list[position] + "/" + pos_list[position+1] + "/" + pos_list[position+2], z_list[position])
				key_true = ("U22:" + pos_list[position] + "/" + pos_list[position+1] + "/" + pos_list[position+2], tag_list[position])
				add_one_feat(feat_vec,key_z,key_true)
		else:
			key_z1 = ("U22:" + pos_list[position] + "/" + pos_list[position+1] + "/" + pos_list[position+2], z_list[position])
			key_z2 = ("U22:" + pos_list[position] + "/" + pos_list[position+1] + "/" + pos_list[position+2], z_list[position+1])
			key_z3 = ("U22:" + pos_list[position] + "/" + pos_list[position+1] + "/" + pos_list[position+2], z_list[position+2])
			key_true = ("U22:" + pos_list[position] + "/" + pos_list[position+1] + "/" + pos_list[position+2], tag_list[position])

			add_one_feat(feat_vec,key_z1,None)
			add_one_feat(feat_vec,key_z2,None)
			add_one_feat(feat_vec,key_z3,None)
			add_one_feat(feat_vec,None,key_true)

#The check and change function calls all the features that may either add or 
def check_and_change(feat_vec,word_list,pos_list,tag_list,z_list,position):
	feat_00(feat_vec,word_list,pos_list,tag_list,z_list,position)
	feat_01(feat_vec,word_list,pos_list,tag_list,z_list,position)
	feat_02(feat_vec,word_list,pos_list,tag_list,z_list,position)
	feat_03(feat_vec,word_list,pos_list,tag_list,z_list,position)
	feat_04(feat_vec,word_list,pos_list,tag_list,z_list,position)
	feat_05(feat_vec,word_list,pos_list,tag_list,z_list,position)
	feat_06(feat_vec,word_list,pos_list,tag_list,z_list,position)
	feat_10(feat_vec,word_list,pos_list,tag_list,z_list,position)
	feat_11(feat_vec,word_list,pos_list,tag_list,z_list,position)
	feat_12(feat_vec,word_list,pos_list,tag_list,z_list,position)
	feat_13(feat_vec,word_list,pos_list,tag_list,z_list,position)
	feat_14(feat_vec,word_list,pos_list,tag_list,z_list,position)
	feat_15(feat_vec,word_list,pos_list,tag_list,z_list,position)
	feat_16(feat_vec,word_list,pos_list,tag_list,z_list,position)
	feat_17(feat_vec,word_list,pos_list,tag_list,z_list,position)
	feat_18(feat_vec,word_list,pos_list,tag_list,z_list,position)
	feat_20(feat_vec,word_list,pos_list,tag_list,z_list,position)
	feat_21(feat_vec,word_list,pos_list,tag_list,z_list,position)
	feat_22(feat_vec,word_list,pos_list,tag_list,z_list,position)
	strip(feat_vec)
	

#perc train calls the viterbi algorithm then calls the check and change function to manipulate the weights
def perc_train(train_data,tagset,numepochs):
	feat_vec = defaultdict(int)
	tags = {}

	for i in range(0,numepochs):
		for j in range(0,len(train_data)):
			label_list = train_data[j][0]
			feat_list = train_data[j][1]

			z = perc.perc_test(feat_vec,label_list, feat_list,tagset,tagset[0])
				
			for k in range(0,len(z)):
				temp = train_tags(label_list)
				if(z[k] != temp[k]):
					check_and_change(feat_vec,word_list(label_list),pos_list(label_list),train_tags(label_list),z,k)

	return feat_vec



if __name__ == '__main__':
    optparser = optparse.OptionParser()
    optparser.add_option("-t", "--tagsetfile", dest="tagsetfile", default=os.path.join("data", "tagset.txt"), help="tagset that contains all the labels produced in the output, i.e. the y in \phi(x,y)")
    optparser.add_option("-i", "--trainfile", dest="trainfile", default=os.path.join("data", "train.txt.gz"), help="input data, i.e. the x in \phi(x,y)")
    optparser.add_option("-f", "--featfile", dest="featfile", default=os.path.join("data", "train.feats.gz"), help="precomputed features for the input data, i.e. the values of \phi(x,_) without y")
    optparser.add_option("-e", "--numepochs", dest="numepochs", default=int(10), help="number of epochs of training; in each epoch we iterate over over all the training examples")
    optparser.add_option("-m", "--modelfile", dest="modelfile", default=os.path.join("data", "default.model"), help="weights for all features stored on disk")
    (opts, _) = optparser.parse_args()

    # each element in the feat_vec dictionary is:
    # key=feature_id value=weight
    feat_vec = {}
    tagset = []
    train_data = []

    tagset = perc.read_tagset(opts.tagsetfile)
    print >>sys.stderr, "reading data ..."
    train_data = perc.read_labeled_data(opts.trainfile, opts.featfile)
    print >>sys.stderr, "done."
    feat_vec = perc_train(train_data, tagset, int(opts.numepochs))
    perc.perc_write_to_file(feat_vec, opts.modelfile)

