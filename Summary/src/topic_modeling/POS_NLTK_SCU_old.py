import nltk
import data_pkg.FileHandling
import itertools
import operator
from nltk  import word_tokenize
from nltk.corpus import stopwords
import os
'''
Created on Aug 5, 2014

@author: amita
'''
def AddPOStag(InputScuFile,PosScuFile):
    stops = set(stopwords.words('english'))
    rowdicts= data_pkg.FileHandling.read_csv(InputScuFile)
    posrowdicts=list()
    fieldnames=rowdicts[0].keys()
    fieldnames.append("noun_verb")
    rowdicts.sort(key= operator.itemgetter("key_user"))
    for key, items in itertools.groupby(rowdicts, operator.itemgetter('key_user')):
        allcontribs=list(items)
        for key2, items2 in itertools.groupby(allcontribs, operator.itemgetter('weight')):
            weightcontribs=list(items2)
            for row in weightcontribs:
                if row["weight"]>str(2) :
                    scu=row["topic_contrib_str"]
                    text = word_tokenize(scu)
                    pos_scu=nltk.pos_tag(text)
                    noun_verb_list=list()
                    for tuple_scu in pos_scu:
                        if tuple_scu[1].startswith("NN") or tuple_scu[1].startswith("VB"):
                            if tuple_scu[0].lower() not in stops:
                                noun_verb_list.append(tuple_scu[0])
                    row["noun_verb"]=" ".join(noun_verb_list) 
                    posrowdicts.append(row) 
                else:
                    print " we less than 3"     
                        
                
    data_pkg.FileHandling.write_csv(PosScuFile, posrowdicts, fieldnames)        
            
    
if __name__ == '__main__':
    
    topic="gay-rights-debates"    
    directoryin=os.getcwd()
    InputScuFile=directoryin +"/topic_data/" + topic + "/modeling_input/Scus_weights"
    PosScuFile=directoryin +"/topic_data/" + topic + "/modeling_input/Pos_Scus"
    AddPOStag(InputScuFile,PosScuFile)
    