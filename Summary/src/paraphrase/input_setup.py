from data_pkg import FileHandling
import operator
import itertools
import os
import json
from random import shuffle
'''
Created on Aug 7, 2014
This  creates a csv file for setting up machine learning experiment.Reads in a jsonvfile Allscus( created by running pyramidscores) containing SCUs from all pyramids.
Filter a pyramid based on  key_user field.
creates a outpair file named AllScuPairs
@author: amita
'''
# find all possible combinations of contributors belong to different scus and add it to PairScuList
def calUMBCSIM(AllOutputPairdir):
    Filelist=os.listdir(AllOutputPairdir)
    for filename in Filelist:
        if filename.startswith("."):
            continue
        #rowdicts=FileHandling.read_csv(OutputDir+"/"+filename[:-4])
        #fieldnames=rowdicts[0].keys()

def DifferentPairs(file_key,contrib_id,ListScus,PairScuList,Label=False):
    IdList=contrib_id.keys()
    DiffIdCombinations=list(itertools.combinations(IdList,2))
    for tuple_comb in DiffIdCombinations:
        contrib1=contrib_id[tuple_comb[0]]
        contrib2=contrib_id[tuple_comb[1]]
        len_contrib1=len(contrib1)
        len_contrib2=len(contrib2)
        pairlist=list(itertools.product(range(0,len_contrib1),range(0,len_contrib2)))
        for pair in pairlist:
                rowdict=dict()
                rowdict["SCU1"]= " ".join(contrib1[pair[0]])
                rowdict["SCU2"]=" ".join(contrib2[pair[1]])
                rowdict["id1"]=str(tuple_comb[0])+"_"+str(pair[0])
                rowdict["id2"]=str(tuple_comb[1])+"_"+str(pair[1])
                rowdict["label"]=Label
                rowdict["key_user"]=file_key
                PairScuList.append(rowdict)
        
    
# find all possible combinations of contributors belong to same scus and add it to PairScuList
def SelfPairs(file_key,ListScus,PairScuList,Label):
    contrib_id=dict()
    for row in  ListScus:
        if row["weight"] > 2 :
            #IdList.append(row["id"])
            contrib_id[row["id"]]=row["contrib"]
            weight=row["weight"] 
            SelfCombinations=list(itertools.combinations(range(0,weight),2))
            for tuple_comb in SelfCombinations:
                rowdict=dict()
                rowdict["SCU1"]= " ".join(row["contrib"][tuple_comb[0]])
                rowdict["SCU2"]=" ".join(row["contrib"][tuple_comb[1]])
                rowdict["id1"]=str(row["id"]) + "_"+ str(tuple_comb[0])
                rowdict["id2"]=str(row["id"])+ "_"+ str(tuple_comb[1])
                rowdict["label"]=Label
                rowdict["key_user"]=file_key
                PairScuList.append(rowdict)
                
                
    return contrib_id
#------------------------------------- create the pairlist 'PairScuList' with all pairs
def CreatePairsScus(ListScus,file_key) :
    PairScuList=list()
    contrib_id=SelfPairs(file_key,ListScus,PairScuList,Label=True)
    DifferentPairs(file_key,contrib_id,ListScus,PairScuList,Label=False)
    return PairScuList
 
 #------------------------------------ write all pairs in PairScuList to output csv AllScuPairs
def CreateScuPairFile(inputscufile,OutputPairdir):
    try:
        fieldnames=["key_user","SCU1","SCU2","id1","id2","label"]
        with open(inputscufile, 'rb') as fp:
            rowdicts = json.load(fp)
        #rowdicts=FileHandling.read_csv(inputscufile)
        rowdicts.sort(key=operator.itemgetter("key_user"))
        for key, items in itertools.groupby(rowdicts, operator.itemgetter('key_user')):
            ListScus=list(items)
            PairScuList=CreatePairsScus(ListScus,key)
            outkeyfile=OutputPairdir + "/"+ key[:-4]
            FileHandling.write_csv(outkeyfile, PairScuList, fieldnames)
            
    except IOError :
        print "error in " +  inputscufile      
            
#===============================================================================
# create a balance pair file of true and false labels
# true: contributors of same scu
# false: contributors of different scus
# Balance each pyramid file by randomly selecting false labels , add true labels, randomize again for
#true and false labels 
#===============================================================================
def Balance_Randomize(AllOutputPairdir,BalancedDir):
    
    if not (os.path.exists(BalancedDir)):
        os.makedirs(BalancedDir)
    FileList = os.listdir(AllOutputPairdir)
    for InpFile in FileList:
        rowdicts=FileHandling.read_csv(AllOutputPairdir+ "/"+InpFile[:-4])
        fieldnames= rowdicts[1].keys()
        TrueRows=[row for row in rowdicts if row['label'] == "True"]
        FalseRows=[row for row in rowdicts if row['label'] == "False"]
        Truelen=len(TrueRows)
        #Falselen=len(FalsRows)
        shuffle(FalseRows)
        BalancedFalse=FalseRows[:Truelen]
        BalancedList=TrueRows + BalancedFalse
        shuffle(BalancedList)
        OutputFile= BalancedDir + "/"+ InpFile[:-4]
        FileHandling.write_csv(OutputFile, BalancedList, fieldnames)
        
def AddID_TDM(Id,Scu,IdList,Allrows_TDM):
    if Id not in IdList:
        dict_TDM=dict()
        dict_TDM["id"]=Id
        dict_TDM["SCU"]=Scu
        IdList.append(Id)
        Allrows_TDM.append(dict_TDM)        
        
def BalancedAllDocs_TDM(BalancedDir,TdmDir):
    if not (os.path.exists(TdmDir)):
        os.makedirs(TdmDir)
    FileList = os.listdir(BalancedDir)
    fieldnames=["id","SCU"]
    for InpFile in FileList:
        rowdicts=FileHandling.read_csv(BalancedDir+ "/"+InpFile[:-4])
        Allrows_TDM=list()
        IdList=list()
        for row in rowdicts:
            Id1=row["id1"]
            Scu1=row["SCU1"]  
            Id2=row["id2"]
            Scu2=row["SCU2"]  
            AddID_TDM(Id1,Scu1,IdList,Allrows_TDM)
            AddID_TDM(Id2,Scu2,IdList,Allrows_TDM)
            
        outputfile=TdmDir +"/" +  InpFile[:-4] 
        FileHandling.write_csv(outputfile, Allrows_TDM, fieldnames) 
            
                
                
            
          
     
        
        
                   
    
if __name__ == '__main__':
    topic="gay-rights-debates"     
    InputScuFile=os.path.dirname(os.getcwd()) + "/data_pkg/CSV/"+ topic+"/MTdata/AllScusJson.json"
    AllOutputPairdir=os.getcwd()+ "/data_pkg/"+ topic +"/AllScuPairs"
    BalancedDir=os.path.dirname(AllOutputPairdir) +"/Balanced_Pairs"
    TdmDir=os.path.dirname(AllOutputPairdir) +"/TDM_Dir"
    if not (os.path.exists(AllOutputPairdir)):
        os.makedirs(AllOutputPairdir)
    CreateScuPairFile(InputScuFile,AllOutputPairdir)
    Balance_Randomize(AllOutputPairdir,BalancedDir)
    BalancedAllDocs_TDM(BalancedDir,TdmDir)