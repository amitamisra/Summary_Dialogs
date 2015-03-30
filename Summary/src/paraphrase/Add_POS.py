import nltk
from data_pkg import FileHandling 
import itertools
import operator
from nltk  import word_tokenize
from nltk.corpus import stopwords
import os
'''
Created on Aug 5, 2014

@author: amita
'''

def ADDPOS_string(String,list_pos):
    
    text = word_tokenize(String)
    pos_string=nltk.pos_tag(text)
    noun_list=list()
    verb_list=list()
    adj_list=list()
    Allstring =""
    adjs=""
    verbs=""
    nouns=""
    posdict=dict()
    
    
    for tuple_scu in pos_string:
        
            if tuple_scu[1].startswith("NN"):
                noun_list.append(tuple_scu[0])
                nouns=" ".join(noun_list) 
                 
            if  tuple_scu[1].startswith("VB"):
                verb_list.append(tuple_scu[0])
                verbs=" ".join(verb_list) 
                
            if tuple_scu[1].startswith("JJ"):
                adj_list.append(tuple_scu[0])
                adjs=" ".join(adj_list) 
                
    if "Noun" in  list_pos:
        Allstring= Allstring + nouns
    if "Adj" in  list_pos:
        Allstring= Allstring + " " +adjs
    if "Verb" in  list_pos:
        Allstring= Allstring + " "+ verbs  
        
    posdict["AllPOSstring"] =Allstring   
    posdict["Noun"] =nouns 
    posdict["Verb"] =verbs 
    posdict["Adj"] =adjs  
                   
    return posdict
    
def AddPosScu(row,scu,num):
    stops = set(stopwords.words('english'))
    text = word_tokenize(scu)
    pos_scu=nltk.pos_tag(text)
    noun_list=list()
    verb_list=list()
    adj_list=list()
    
    for tuple_scu in pos_scu:
        if tuple_scu[0].lower() not in stops:
            if tuple_scu[1].startswith("NN"):
                noun_list.append(tuple_scu[0])
                row[num +"_noun"]=" ".join(noun_list) 
                 
            if  tuple_scu[1].startswith("VB"):
                verb_list.append(tuple_scu[0])
                row[num +"_verb"]=" ".join(verb_list) 
                
            if tuple_scu[1].startswith("JJ"):
                adj_list.append(tuple_scu[0])
                row[num +"_adj"]=" ".join(adj_list) 
    
def AddPOStag(BalancedPairsDir):
    FileList = os.listdir(BalancedPairsDir)
    OutDir=os.path.dirname(BalancedPairsDir) +"/" +"BalPairPos/"
    if not (os.path.exists(OutDir)):
        os.makedirs(OutDir)
    for InpFile in FileList :
        rowdicts=FileHandling.read_csv(BalancedPairsDir +"/"+InpFile[:-4])
        posrowdicts=list()
        fieldnames=rowdicts[0].keys()
        fieldnames.append("SCU1_noun")
        fieldnames.append("SCU2_noun")
        fieldnames.append("SCU1_verb")
        fieldnames.append("SCU2_verb")
        fieldnames.append("SCU1_adj")
        fieldnames.append("SCU2_adj")
        rowdicts.sort(key= operator.itemgetter("key_user"))
        for row in rowdicts:
            Scu1=row["SCU1"]
            Scu2=row["SCU2"]
            AddPosScu(row,Scu1,"SCU1")
            AddPosScu(row,Scu2,"SCU2")
            posrowdicts.append(row) 
                        
        PosScuFile= OutDir + InpFile[:-4]      
        FileHandling.write_csv(PosScuFile, posrowdicts, fieldnames)        
            
    
if __name__ == '__main__':
    
    topic="gay-rights-debates"    
    topic="gay-rights-debates"     
    BalancedPairsDir=os.getcwd()+ "/data_pkg/"+ topic +"/Balanced_Pairs"
    AddPOStag(BalancedPairsDir)
    
    
    
    