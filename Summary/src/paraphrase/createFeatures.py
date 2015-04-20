import os
from data_pkg import FileHandling
from nlp.text_obj import TextObj
from requests import get
import preprocess_text
import math
from collections import Counter

'''
Created on Aug 12, 2014
NOt used in naacl
@author: amita

'''




class Features:
    def __init__(self, feature_list,InpDir,feature_file,Allrows):
        self.feature_list=feature_list
        self.Feature_file=feature_file
        self.InpDir=InpDir
        self.Allrows=Allrows
    
    #----------------- def sss(self,row, type_sim='relation', corpus='webbase'):
        #---------- sss_url = "http://swoogle.umbc.edu/SimService/GetSimilarity"
        #------------------------------------------------------------------ try:
            #---------------------------------------------------- s1=row["SCU1"]
            #---------------------------------------------------- s2=row["SCU2"]
            # response = get(sss_url, params={'operation':'api','phrase1':s1,'phrase2':s2,'type':type,'corpus':corpus})
            #------------------------------- return float(response.text.strip())
        #--------------------------------------------------------------- except:
            #------------------------------------------------ print response.raw
            #--------------------------------------------- print response.reason
            # print 'Error in getting similarity for %s: %s' % ((s1,s2), response)
            # print "filename_ "+ row["filename"]+ "id1_ " + row["id1"] + "id12_ " + row["id2"] +"\n"
            #-------------------------------------------------------- return 0.0
        
    def UMBCSIM(self,rowdict,row): 
        #print type(s1)
        #s1=removeS(s1)
        #s2=removeS(s2)
        type_sim='relation'
        corpus='webbase'
        sim= self.sss(row,type_sim,corpus)
        rowdict["UMBC"]=sim

def buildVector(iterable1, iterable2):
    counter1 = Counter(iterable1)
    counter2= Counter(iterable2)
    all_items = set(counter1.keys()).union( set(counter2.keys()) )
    vector1 = [counter1[k] for k in all_items]
    vector2 = [counter2[k] for k in all_items]
    return (vector1 , vector2)

def cosim(v1, v2):
    dot_product = sum(n1 * n2 for n1,n2 in zip(v1, v2) )
    magnitude1 = math.sqrt (sum(n ** 2 for n in v1))
    magnitude2 = math.sqrt (sum(n ** 2 for n in v2))
    if (magnitude1==0 or magnitude2==0):
        return 0
    return dot_product / (magnitude1 * magnitude2)

def processPOS(s1,s2,stem):
    
    processed_s1=preprocess_text.preprocess(s1, stem)
    processed_s2=preprocess_text.preprocess(s2, stem)
    s1_text_obj = TextObj(processed_s1.decode('utf-8', 'replace'))
    s1_tokens= s1_text_obj.tokens
    
    s2_text_obj = TextObj(processed_s2.decode('utf-8', 'replace'))
    s2_tokens=s2_text_obj.tokens
    vecs=buildVector(s1_tokens,s2_tokens)
    return (cosim(vecs[0], vecs[1]))

def Calc_cosine(row,rowdict,choice):
    #stem=True
    s1=row["SCU1"]
    s2=row["SCU2"]
    stem=True 
    for ch in choice:
        if ch=="N_V_A_Cos" :
            s1_NVA= row["SCU1_verb_Extended"] + row["SCU1_noun_Extended"] +row["SCU1_adj_Extended"]
            s2_NVA= row["SCU2_verb_Extended"]+row["SCU2_noun_Extended"] + row["SCU2_adj_Extended"]
            NVAcosine= processPOS(s1_NVA,s2_NVA,stem)
            rowdict["N_V_A_Cos"]=NVAcosine
        if ch=="N_V_Cos":
            s1_NV= row["SCU1_verb_Extended"] + row["SCU1_noun_Extended"] 
            s2_NV= row["SCU2_verb_Extended"]+row["SCU2_noun_Extended"] 
            NVcosine= processPOS(s1_NV,s2_NV,stem)
            rowdict["N_V_Cos"]=NVcosine
        if ch== "A_Cos":
            s1_A=row["SCU1_adj_Extended"]
            s2_A=row["SCU2_adj_Extended"]
            Acosine= processPOS(s1_A,s2_A,stem)
            rowdict["A_Cos"]=Acosine
        if ch=="A_N_Cos":
            s1_A_N=row["SCU1_adj_Extended"]+row["SCU1_noun_Extended"]
            s2_A_N=row["SCU2_adj_Extended"]+row["SCU2_noun_Extended"]
            A_Ncosine= processPOS(s1_A_N,s2_A_N,stem)
            rowdict["A_N_Cos"]=A_Ncosine
          
    cos=processPOS(s1,s2,stem) 
    rowdict["Cosine"]=cos         
    
    
if __name__ == '__main__':
    topic="gay-rights-debates" 
    Feature_List=["Cosine","UMBC"]
    Feature_File=os.getcwd() + "/data_pkg/"+ topic+ "/Features"
    InpDir=os.getcwd()+ "/data_pkg/"+ topic +"/BalPairExtended/BalPairExtended_Csv"
    Allrows=list()
    choice=list()
    choice.append("N_V_A_Cos")
    choice.append("N_V_Cos")
    choice.append("A_Cos")
    choice.append("A_N_Cos")
    fieldnames=["label","filename","id1","id2"] + choice
    
    Feature_obj=Features(Feature_List,InpDir,Feature_File,Allrows)
    FileList=os.listdir( Feature_obj.InpDir)
    for Infile in FileList:
        if Infile == "1-8171_3_2__4_5_7_11_1_user6.csv" :
            print "stop"
        if Infile.startswith("."):
            continue
        rows=FileHandling.read_csv( Feature_obj.InpDir+"/"+ Infile[:-4])
        for row in rows:
            rowdict=dict()
            for feature in Feature_List:
                if feature == "UMBC":
                    Feature_obj.UMBCSIM(rowdict,row)
                    if "UMBC" not in fieldnames:
                        fieldnames.append("UMBC")
                    
                if feature == "Cosine":
                    #------------ if (row["id1"]=="6_1" and row["id2"]=="6_4") :
                        #------------------------------------------ print "stop"
                    
                    
                    Calc_cosine(row,rowdict,choice)
                    
                    if "Cosine" not in fieldnames:
                        fieldnames.append("Cosine")
                    
            rowdict["label"]=row["label"]  
            rowdict["filename"]=Feature_obj.InpDir+"/"+ Infile[:-4]
            rowdict["id1"]=row["id1"]
            rowdict["id2"]=row["id2"] 
            Feature_obj.Allrows.append(rowdict)
                     
    
 
    FileHandling.write_csv(Feature_obj.Feature_file, Allrows, fieldnames)
                
