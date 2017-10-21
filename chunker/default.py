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
	if feat_vec[key_z] != None:
		feat_vec[key_z] -= 1
		if feat_vec[key_z] <= 0:
			feat_vec.pop(key_z)
	if feat_vec[key_true] == None:
		feat_vec[key_true] = 1
	else:
		feat_vec[key_true] += 1
	return


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

def check_and_change(feat_vec,word_list,pos_list,tag_list,z_list,position):
	feat_01(feat_vec,word_list,pos_list,tag_list,z_list,position)
	feat_02(feat_vec,word_list,pos_list,tag_list,z_list,position)
	



def perc_train(train_data,tagset,numepochs):
	numepochs = 2 #manual change
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

