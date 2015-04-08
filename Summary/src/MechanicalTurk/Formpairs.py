'''
Created on Sep 1, 2014
This file takes all clusters from cluster file created in paraphrase  program Input_clustering, forms pairs of labels in same cluster
 and creates a pair file for Mechanical similarity  task
@author: amita
'''
import operator
import itertools
from data_pkg import FileHandling
import os
from paraphrase import similarity

def CombinationStrings(RowStrings,ErrorLines,Label,fields):
    type_sim='relation'
    corpus='webbase'
    PairListCluster=list()
    Combinations=list(itertools.combinations(RowStrings,2))
    for tuple_comb in Combinations:
                rowdict=dict()
                for field in fields:
                    rowdict[str(field)+ str(1)]= (tuple_comb[0])[field]
                    rowdict[str(field)+ str(2)]= (tuple_comb[1])[field]
                    if "string" in str(field):
                        S1=(tuple_comb[0])[field]
                        S2=(tuple_comb[1])[field]
                        sim=similarity.sss(S1, S2, type_sim, corpus)
                        if sim==-1:
                            ErrorLines.append("\n\n Error in these sim pairs\n")
                            ErrorLines.append("1)"+S1 +"\n")
                            ErrorLines.append("2)"+S2+"\n")
                        rowdict["UMBC"]=sim
                         
                rowdict["label_cluster"]=Label
                PairListCluster.append(rowdict)
    return PairListCluster            

def createpairs(RowDicts,ErrorLines,Label,fields):
    AllPairs=list()
    RowDicts.sort(key=operator.itemgetter(Label))
    for key, items in itertools.groupby(RowDicts, operator.itemgetter(Label)):
        ListRows=list(items)
        PairListCluster=CombinationStrings(ListRows,ErrorLines,key,fields)
        AllPairs.extend(PairListCluster)
    
    return AllPairs

def ReadInput(FilenameCsv):
    
    RowDicts=FileHandling.read_csv(FilenameCsv)
    return RowDicts
    
def Execution(InputCsv,OutputCsv, Error_UMBC,Label,fields):
    fieldnames=[str(field)+ str(1) for field in fields]
    fieldnames.append(Label)
    fieldnames.append("UMBC")
    fieldnames=fieldnames +[str(field)+ str(2) for field in fields]
    ErrorLines=list()
    RowDicts=ReadInput(InputCsv)
    AllPairs=createpairs(RowDicts,ErrorLines,Label,fields)
    FileHandling.write_csv(OutputCsv, AllPairs, fieldnames)
    FileHandling.WriteTextFile(Error_UMBC, ErrorLines)
  
if __name__ == '__main__':
    #begin------------------------------------------------------------------------- #done for naacl
    #------------------------------------------------ topic="gay-rights-debates"
    # ClusterLabelInp=os.path.dirname(os.getcwd()) + "/paraphrase/para_data/gay-rights-debates/cluster/LabelUpdated/TFIdf/Cos_Cluster_70_AVG_Noun_Verb_Ad"
    # ClusterLabelPairs=os.path.dirname(os.getcwd()) + "/paraphrase/para_data/gay-rights-debates/cluster/LabelUpdated/TFIdf/Pairs_Cos_Cluster_70_AVG_Noun_Verb_Ad"
    # Error_UMBC=os.path.dirname(os.getcwd()) + "/paraphrase/para_data/gay-rights-debates/cluster/LabelUpdated/TFIdf/ErrorPairsUMBC_Cos_Cluster_70_AVG_Noun_Verb_Ad"
    #----------------------------------- Label="label_cluster" # field for pairs
    #---------------------------------------- fields=["string","key","doccount"]
    #----- Execution(ClusterLabelInp,ClusterLabelPairs, Error_UMBC,Label,fields)
#------------------------------------------------------------------------------ 
#end------------------------------------------------------------------------------ 
    
    topic="gun-control"
    inputdir="/Users/amita/git/FacetIdentification/src"
    ClusterLabelInp=inputdir + "/Paraphrase_Pkg_data/" + topic+"/cluster/Phase1/TFIdf/Cos_Cluster_70_AVG_Noun_Verb_Ad"
    ClusterLabelPairs=inputdir + "/Paraphrase_Pkg_data/" + topic+"/cluster/Phase1/TFIdf/Pairs_Cos_Cluster_70_AVG_Noun_Verb_Ad"
    Error_UMBC=inputdir+ "/Paraphrase_Pkg_data/" + topic +"/cluster/Phase1/TFIdf/ErrorPairsUMBC_Cos_Cluster_70_AVG_Noun_Verb_Ad"
    Label="label_cluster" # field for pairs
    fields=["string","key","doccount"]
    Execution(ClusterLabelInp,ClusterLabelPairs, Error_UMBC,Label,fields)
    
    
    
    
    