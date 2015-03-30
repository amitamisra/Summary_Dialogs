from itertools import product
import WSD
import pywsd
from pywsd.lesk import  adapted_lesk, simple_lesk
from nltk import wsd
from nltk.corpus.reader.wordnet import Synset
import sys
from  pywsd.baseline import first_sense

'''
Created on Oct 30, 2014

@author: amita
'''

def replacepos(Sub_Obj):
    NewSubObj=list()
    for tuples in Sub_Obj:
        if str(tuples[1]).startswith("NN" ):
            NewSubObj.append((tuples[0],"n"))
        if str(tuples[1]).startswith("RB"):
            NewSubObj.append((tuples[0],"r"))
        if str(tuples[1]).startswith("VB"):
            NewSubObj.append((tuples[0],"v"))
        if str(tuples[1]).startswith("JJ"):
            NewSubObj.append((tuples[0],"a")) 
        return   NewSubObj          

def GetSynset(Dep,String,Word_Dict_Arg,Relation,relname,indexList):
    
    Synsetlist=list()
    
    for rel in Dep:
            try:
                if rel["Relation"] in Relation:
                    Word_Dict_index=[Word_Dict for Word_Dict  in Word_Dict_Arg if Word_Dict["index"]==rel[relname+"_Index"]]
                    if Word_Dict_index:
                        if not Word_Dict_index[0]["index"] in indexList: 
                            indexList.append(Word_Dict_index[0]["index"]) 
                            if  (Word_Dict_index[0]["word"]) =="Whenever":
                                    print "stop" 
                            Sub_Obj=[(rel[relname],Word_Dict_index[0]["pos"] )]
                            NewSubObj=replacepos(Sub_Obj)
                            for ambigous in NewSubObj:
                                
                                syn=wsd.lesk(String,ambigous[0], pos = ambigous[1] )
                                boolvar=isinstance(syn, Synset)
                                
                                if not boolvar:
                                    print "error in synset   " + String+ "word   " + ambigous[0]+  "pos = "+ ambigous[1]
                                    syn=adapted_lesk(String,ambigous[0])
                                Synsetlist.append(syn)
            except (NameError, IndexError):
                print IndexError
                print """local variable 'signature' referenced before assignment for""" + ambigous[0]
                try:
                    syn=first_sense(ambigous[0]) 
                    Synsetlist.append(syn) 
                    boolvar=isinstance(syn, Synset)
                    if not boolvar:
                        print "error in synset   " + String+ "word   " + ambigous[0]+  "   pos =   "+ ambigous[1]
                except (NameError, IndexError):
                    print IndexError
                    print """local variable 'signature' referenced before assignment for""" + ambigous[0]    
                            
                    
                              
    return (Synsetlist)
       # if ambigous[0]=="Whenever" or ambigous[0]=="heterophobe" or ambigous[0]=="Archie" or ambigous[0]=="""'s"""  \
        #                 or ambigous[0]=="anyone"  or ambigous==["everyone"] or ambigous[0]=="freedom":
   

            
        
def GetCorrPair(DepA,StringA,Word_DictA,DepB,StringB,Word_DictB):
    Relation=["nsubj","nsubjpass","dobj", "iobj","pobj"]
    indexA=list()
    indexB=list()
    SynsetlistANoun=GetSynset(DepA,StringA,Word_DictA,Relation,"Dep",indexA)
    SynsetlistBNoun=GetSynset(DepB,StringB,Word_DictB,Relation,"Dep",indexB)
   
    Relation=["nsubj"]
    FirstVerblistA=GetSynset(DepA,StringA,Word_DictA,Relation,"Gov",indexA)
    FirstVerblistB=GetSynset(DepB,StringB,Word_DictB,Relation,"Gov",indexB)
    
    # TODO as stanford Parser does not return root as vertex
    Relation="root"
    SecVerblistA=GetSynset(DepA,StringA,Word_DictA,Relation,"Dep",indexA)
    SecVerblistB=GetSynset(DepB,StringB,Word_DictB,Relation,"Dep",indexB)
    if FirstVerblistB is  None:
        FirstVerblistB=[]
    if SecVerblistB is  None:
        SecVerblistB=[]   
    
    
    if FirstVerblistA is  None:
        FirstVerblistA=[]
    if SecVerblistA is  None:
        SecVerblistA=[]       
    
    
    VerblistA=FirstVerblistA + SecVerblistA
    VerblistB=FirstVerblistB + SecVerblistB
    
    
    
    Relation="nn"
   # NNA=GetSynset(DepA,StringA,Word_DictA,Relation,"Dep",indexA)
   # NNB=GetSynset(DepB,StringB,Word_DictB,Relation,"Dep",indexB)
    
    SubObjPairs=[]
    if SynsetlistANoun is not None:
        if  SynsetlistBNoun is not None:
                SubObjPairs= product(SynsetlistANoun,SynsetlistBNoun)
                
                
    VerbPairs=[]            
    if  VerblistA is not None:
        if VerblistB is not None:  
            VerbPairs=product(VerblistA,VerblistB)
    NNpairs=[]
    NNA=[]
    NNB=[]
    if NNA is not None: 
        if NNB is not None:
            print StringA +"\n"
            print StringB +"\n"
            print str(NNA) +"\n"
            print str(NNB) +"\n"
            NNpairs=product(NNA,NNB)
            
    StringA_Count_V_A_N_RB=sum(1 for Word_Dict in Word_DictA if str(Word_Dict["pos"]).startswith(("NN","RB","VB","JJ")))
    StringB_Count_V_A_N_RB=sum(1 for Word_Dict in Word_DictB if str(Word_Dict["pos"]).startswith(("NN" , "RB", "VB","JJ")))
        
    return(SubObjPairs,VerbPairs,NNpairs,StringA_Count_V_A_N_RB,StringB_Count_V_A_N_RB)
    
 
    

#dobj,
#nsubj, nsubjpass
if __name__ == '__main__':
    pass