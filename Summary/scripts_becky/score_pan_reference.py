import glob
import math
import nltk
from numpy import array,dot,zeros,std,mean,median,sort
import xml.etree.ElementTree as ET
from collections import namedtuple
from matplotlib import pyplot
from matplotlib.ticker import NullFormatter
import csv
import itertools

"""
Docstrings will explain the hard-coded values.
Be sure to replace hard-coded values (anything with a docstring explanation)
before you run the script.
"""

# average word count of the model summaries
AVG_WORD_COUNT_REF = 283.6
# average number of SCUs in model summaries
AVG_SCU_COUNT_REF = math.ceil(26.8)
# histogram of the number of SCUs in all model summaries with weights 1-5
PYR_SCU_WEIGHTS = {1: 22, 2: 15, 3: 13, 4: 7, 5: 3}

# the SCU weight distribution for each model summary
references = {'marion': ({1: 0, 2: 4, 3: 10, 4: 5, 5: 3},239,73),'ann': ({1: 11, 2: 13, 3: 13, 4: 7, 5: 3},574,119),
				'heather': ({1: 1, 2: 2, 3: 2, 4: 3, 5: 3},139,38),'mary': ({1: 9, 2: 4, 3: 5, 4: 6, 5: 3},194,71),
				'ruthie': ({1: 1, 2: 7, 3: 9, 4: 7, 5: 3},272,85)}

def max_scu_sum(number_of_scus):
	NUM_POSS_WEIGHTS = len(references['marion'][0].keys())
	count = zeros(NUM_POSS_WEIGHTS)
	weights = array(range(NUM_POSS_WEIGHTS+1)[1:])
	i = number_of_scus
	j = NUM_POSS_WEIGHTS
	while (i-PYR_SCU_WEIGHTS[j]>0):
		i-=PYR_SCU_WEIGHTS[j]
		count[j-1] = PYR_SCU_WEIGHTS[j]
		j -= 1
	count[j-1] = i
	return dot(count,weights)

# compute max score that can be generated from the avg number of scus in the reference summaries, =90
SCU_WEIGHT_REF = max_scu_sum(AVG_SCU_COUNT_REF)

# Did the summary use words economically?
def score1(scu_weight_sum,scu_count):
	max_possible = max_scu_sum(scu_count)
	return scu_weight_sum/float(max_possible)

# Did the summary communicate an effective amount of the content? To what degree does the target summary
# reflect the content in the pyramid?	
def score2(scu_weight_sum):
	return float(scu_weight_sum)/SCU_WEIGHT_REF

# combined measure of score1 and score2
def score3(score1,score2):
	return 0.5 * (score1+score2)



# compute the amount of information each word should convey, based on reference summaries
def info_per_word(scu_weight_sum,word_count):
	return scu_weight_sum/float(word_count)

total = 0
for writer in references:
	res = info_per_word(references[writer][2],references[writer][1])
	total += res
WORD_NORM_FACTOR = float(total)/len(references.keys())

# Normalize by word count rather than SCU count.
# Use the reference summaries to define the amount of semantic information each word can convey.
def score4(scu_weight_sum,word_count):
	return scu_weight_sum/(word_count * WORD_NORM_FACTOR)

def get_root(filename):
	tree = ET.parse(filename)
	root = tree.getroot()
	return root

def get_word_count(root):
	targ_summ_text = [line for line in root.find('annotation').iter('line')][0].text
	return len(nltk.word_tokenize(targ_summ_text))
	
# returns scu_weight_sum, scu_count 
def get_scu_info(root):
	scus = []
	for peerscu in root.find('annotation').iter('peerscu'):
		if len([p for p in peerscu.iter('part')])>0:
			try:
				weight = int(peerscu.get('label')[1])
				scu_id = int(peerscu.get('uid'))
				scus.append((weight,scu_id))
			except ValueError as e:
				print e, peerscu.get('label')
	return scus
	
if __name__ == '__main__':
    # replace with path to the directory where your .pan files are
    pans = glob.glob('/Users/EmilyChen/Dropbox/pyramids/data/target/summaries/scored/*.pan')
    targets = dict.fromkeys([pan[-13:-4] for pan in pans])
    for pan in pans:
	    id = pan[-13:-4]
	    root = get_root(pan)
	    word_count = get_word_count(root)
	    scu_weight_sum, scu_count = get_scu_info(root)
	    scu_info = namedtuple('SCU_info','weight_sum count')
	    target_attributes = scu_info(scu_weight_sum,scu_count)
	    s1 = score1(scu_weight_sum,scu_count)
	    s2 = score2(scu_weight_sum)
	    s3 = score3(s1,s2)
	    s4 = score4(scu_weight_sum,word_count)
	    results = namedtuple('Results','score1 score2 score3 score4')
	    target_score = results(s1,s2,s3,s4)
	    targets[id] = (target_attributes,target_score)

    for item in targets.items():
	    print 'ID '+item[0]+':\n{}'.format(item[1][0])
	    print 'Score 1: {0:.3f}\nScore 2: {1:.3f}\nScore 3: {2:.3f}\nScore 4: {3:.3f}\n'.format(item[1][1][0],item[1][1][1],item[1][1][2],item[1][1][3])

    # visualize score distributions
    fig = pyplot.figure()
    rankings = {1:[],2:[],3:[],4:[]}
    for i in xrange(4):
	    s = [scores[i] for attr,scores in targets.values()]
	    sorted_desc = sort(s)[::-1]
	    r = []
	    for mark in sorted_desc:
		    id = [k for k, v in targets.iteritems() if v[1][i] == mark]
		    r.append(id)
	    rankings[i+1] = r
	    std_dev = std(s)
	    mn = mean(s)
	    med = median(s)
	    ax = fig.add_subplot(2,2,i+1,autoscale_on=False,xlim=[0,1.5],ylim=[0,10])
	    ax.hist(array(s),bins=(0,0.125,0.25,0.375,0.5,0.625,0.75,0.825,1.0,1.125,1.25,1.375,1.5))
	    ax.set_xlabel('Score'+str(i+1)+'\nStd Dev: {0:.3}, Mean: {1:.3}, Median: {2:.3}'.format(std_dev,mn,med))
	    ax.set_ylabel('Count')
    pyplot.subplots_adjust(wspace=0.8,hspace=0.4)
    pyplot.suptitle('Distributions of Four Metrics Applied to Target Summaries',fontsize=16)
    pyplot.show()

    with open('ranking_report','wb') as f:
	    mywriter = csv.writer(f,delimiter='\t')
	    mywriter.writerow(['Score1','Score2','Score3','Score4'])
	    for rank in itertools.izip(rankings[1],rankings[2],rankings[3],rankings[4]):
		    mywriter.writerow(rank)
