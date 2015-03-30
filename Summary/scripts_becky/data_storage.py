import pymongo
from pymongo import Connection
from bson.binary import Binary
import pickle
import glob
import nltk
from train_on_conll2000 import *
import xml.etree.ElementTree as ET

def all_lower(list_of_tokens):
	return [t.lower() for t in list_of_tokens]
	
def get_sents(raw):
# returns a list of word-tokenized sents
	untok = nltk.tokenize.sent_tokenize(raw)
	word_tok_sents = []
	punct = ['.',',','?',';',"'",'-',':','...','!','(',')','[',']']
	for s in untok:
		word_tok_sents.append(all_lower([i for i in nltk.tokenize.word_tokenize(s) if i not in punct]))
	print word_tok_sents
	return word_tok_sents
		
def shallow_parse(sent_list):
	# currently returns a list of Tree objects
	# if subtree = Tree('NP', [('energy', 'NN')])
	# subtree[0] returns ('energy', 'NN')	
	chunks = []
	with open('conll2000_trigram_uni_backoff','rb') as f:
		chunker = pickle.load(f)
	for sent in sent_list:
		tree = chunker.parse(sent)
		for sub in tree.subtrees():
			if sub.node != 'S':
				chunks.append(sub)
	print chunks
	return chunks

def words(sent):
	punct = ['.',',','?',';',"'",'-',':','...','!','(',')','[',']']
	return [w for w in sent if w not in punct]

def get_scus(filename):
	tree = ET.parse(filename)
	root = tree.getroot()
	return [Scu(element) for element in root.iter('scu')]
		
class Summary(object):
	def __init__(self,raw):
		self.sents = get_sents(raw)
		self.pos = nltk.tag.batch_pos_tag(self.sents)
		# create another field to store stemmed, spellchecked sents with punct removed
		# import the parser that had the best performance on your sample
		self.chunks = shallow_parse(self.pos)

class Pyramid(object):
	def __init__(self,filename):
		self.scus = get_scus(filename)

class Scu(object):
	def __init__(self,element):
		self.id = int(element.get('uid'))
		self.label = words(all_lower(nltk.tokenize.word_tokenize(element.get('label'))))
		self.contrib = [words(all_lower(nltk.tokenize.word_tokenize(c.get('label')))) for c in element.iter('contributor')]
		self.weight = len(self.contrib)
			
def main():
	# create mongo connection
	conn = Connection()
	db = conn.tc_storage
	coll = db.writingsamples
	coll.remove()
	print "coll.count()"
	print coll.count()
	for path in glob.glob('/Users/EmilyChen/Dropbox/pyramids/data/target/summaries/[0-9]*.txt'):
		id = path[-13:-4]
		with open(path,'r') as f:
			raw = f.read()
		s = Summary(raw)
		coll.save({'id':id,'summary':Binary(pickle.dumps(s),subtype=128)})
	
	pyr_coll = db.pyramid
	pyr_coll.remove()
	matter_pyr = Pyramid('../pyr/12_10_09_MATTER.pyr')
	for scu in matter_pyr.scus:
		doc = {'id':scu.id,'weight':scu.weight,'label':scu.label,'contrib':scu.contrib}
		pyr_coll.save(doc)
	print "pyrcoll.count()"
	print pyr_coll.count()
	
if __name__ == '__main__':
	main()