'''
Created on Nov 24, 2014

@author: amita
'''
from collections import Counter
import os
from data_pkg import FileHandling
from file_formatting import csv_wrapper
def split(Input, Training, Test):
    Rows=FileHandling.read_csv(Input)
    #--------------------------------- clusters=[Row["cluster"] for Row in Rows]
    #----------------------------------------- Cluster_Counter=Counter(clusters)
    #------------------------------- sortedcluster=Cluster_Counter.most_common()
    #------------------------------------------------------ count_traincluster=0
    #------------------------------------------------------- traincluster=list()
    #-------------------------------------------------------- testcluster=list()
    #--------------------------------------------- for cluster in sortedcluster:
        #------------------------------------------ if count_traincluster < 750:
            #----------------------------------- traincluster.append(cluster[0])
            #---------------- count_traincluster=count_traincluster + cluster[1]
        #------------------------------------------ if count_traincluster > 750:
            #------------------------------------ testcluster.append(cluster[0])
#------------------------------------------------------------------------------ 
            
    TrainingRows=Rows[0:750]
    TestRows=Rows[750:]
    csv_wrapper.write_csv(Training,TrainingRows)
    csv_wrapper.write_csv(Test,TestRows)
    
    
if __name__ == '__main__':
    Input=os.getcwd() + "/Similarity_Data/gay-rights-debates/MTdata_cluster/Labels_Updated/AllMT_task/Results/Rand_FeatureFileAllMT_Reg"
    Training=os.getcwd() + "/Similarity_Data/gay-rights-debates/MTdata_cluster/Labels_Updated/AllMT_task/Results/TrainRand_FeatureFileAllMT_Reg.csv"
    Test=os.getcwd() + "/Similarity_Data/gay-rights-debates/MTdata_cluster/Labels_Updated/AllMT_task/Results/TestRand_FeatureFileAllMT_Reg.csv"
    split(Input, Training, Test)