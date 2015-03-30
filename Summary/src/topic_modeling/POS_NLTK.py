import nltk
import data_pkg.FileHandling
import itertools
import operator
from nltk  import word_tokenize
import os
'''
Created on Aug 5, 2014

@author: amita
'''
def AddPOStag(InputScuFile):
    rowdicts= data_pkg.FileHandling.read_csv(InputScuFile)
    rowdicts.sort(key= operator.itemgetter("key_user"))
    for key, items in itertools.groupby(rowdicts, operator.itemgetter('key_user')):
        allcontribs=list(items)
        for key2, items2 in itertools.groupby(allcontribs, operator.itemgetter('weight')):
            weightcontribs=list(items2)
            for row in weightcontribs:
                if row["weight"]<3:
                    break
                else:
                    scu=row["topic_contrib_str"]
                    text = word_tokenize(scu)
                    pos_scu=nltk.pos_tag(text)
                    print pos_scu
                
            
            
    
if __name__ == '__main__':
    
    topic="gay-rights-debates"    
    directoryin=os.getcwd()
    InputScuFile=directoryin
    AddPOStag(InputScuFile)
    