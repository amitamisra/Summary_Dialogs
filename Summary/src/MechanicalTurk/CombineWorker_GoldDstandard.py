'''
Created on Nov 22, 2014

@author: amita
'''
from data_pkg import FileHandling
import sys
from copy import deepcopy
from file_formatting import csv_wrapper
def CombineGoldstandardHitwithOthers(MTHitGoldDsplit,MTHitWorkersplit,Combine):
    keys=["UMBC_","doccounta_", "doccountb_","keya_", "keyb_", "label_cluster_","stringa_", \
             "stringb_"]
    MT1gold= FileHandling.read_csv(MTHitGoldDsplit)
    
    MT2Other= FileHandling.read_csv(MTHitWorkersplit)
    NewRows=list()
    for row in MT2Other:
        Newdict={}
        Newdict=deepcopy(row)
        Samerow=[rowGold for rowGold in MT1gold if rowGold["stringa_"]== row["stringa_"] \
                 and rowGold["stringb_"]== row["stringb_"]]#gold standard
        
        if Samerow:
            if len(Samerow) > 1:
                print "rows not same"
                sys.exit()
            
            for field in keys:
                    if row[field] != Samerow[0][field]:
                        print "rows not same"
                        sys.exit()
                        
            
                
            Newdict["Id_A2TNNKHFNY5WQ4"]=Samerow[0]["Id_A2TNNKHFNY5WQ4"]
            
            
        NewRows.append(Newdict)    
    csv_wrapper.write_csv(Combine, NewRows)           
    





if __name__ == '__main__':
#     InputWorker="""/Users/amita/git/summary_repo/Summary/src/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task4/Results/MT_Task4_split_worker"""
#     InputGold= """/Users/amita/git/summary_repo/Summary/src/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task2/ResultsV3/MT2_web_interface_split_worker"""
#     Combine="""/Users/amita/git/summary_repo/Summary/src/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/AllMT_task/Results/MT4_MT2_Gold_split_worker.csv"""
#                
    
    
    InputGold="""/Users/amita/git/summary_repo/Summary/src/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task5/Results/MT_Task5_split_worker"""
    InputWorker= """/Users/amita/git/summary_repo/Summary/src/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task3/Results/MT_Task3_split_worker"""
    Combine="""/Users/amita/git/summary_repo/Summary/src/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/AllMT_task/Results/MT5_MT3_Gold_split_worker.csv"""
 
    
    CombineGoldstandardHitwithOthers(InputGold,InputWorker,Combine)
                
                