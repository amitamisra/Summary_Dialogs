from nltk.corpus import wordnet 
from textblob import Word
'''
Created on Oct 31, 2014

@author: amita
'''
def createoffsetdict():
    syns = list(wordnet.all_synsets())  # @UndefinedVariable
    offsets_list = [(s._offset, s) for s in syns]
    best_synset = wordnet.synsets('drinks')[0]  # @UndefinedVariable
    offsets_dict = dict(offsets_list)
  #  print offsets_dict["08420278"]
   # print offsets_dict[13384557]
    print ""

def WSD(wordlist,pos,string):
    if string=="":
        for word in wordlist:
            best_synset = wordnet.synsets('drinks')  # @UndefinedVariable
            print best_synset
        
if __name__ == '__main__':
    word = Word("plant")
   # word.
    best_synset = wordnet.synsets('drinks')  # @UndefinedVariable
    offset=best_synset[0].offset()
    createoffsetdict()
   
                                    
    print best_synset
