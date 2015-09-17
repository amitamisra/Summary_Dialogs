'''
Created on Nov 22, 2014

@author: amita
'''
from __future__ import division
from file_formatting import csv_wrapper
from data_pkg import FileHandling
import os



global fieldnames
fieldnames=["HITId","HITTypeId","UMBC_" ,"doccounta_", "doccountb_","keya_", "keyb_", "label_cluster_", "stringa_", "stringb_"]

def RegressionLabel(MTInput,MTCorr,MTNoHits, MT_RegressionLabel)  :
    MTRows=FileHandling.read_csv(MTInput) 
    MTCorrRows=FileHandling.read_csv(MTCorr) 
    MTNoHitRows=FileHandling.read_csv(MTNoHits) 
    GoodCorrWorker=list() 
    sufficienthit=list()
    AllRows=list()
    GoldRorwCorr=[rowcorr for rowcorr in MTCorrRows if rowcorr["Workers"]=="Id_A2TNNKHFNY5WQ4"]
    for key in GoldRorwCorr[0].keys():
        try:
            if float(GoldRorwCorr[0][key]) > 0.6:
                GoodCorrWorker.append(key)
        except ValueError:
            print "No value for " +  GoldRorwCorr[0][key]  + " : "+ key 
            print "stop" 
    
    
    for workerhitno in MTNoHitRows:
        if int(workerhitno["X.1..38"]) > 19:
            sufficienthit.append(workerhitno ["Workers"])
            
    finalWorker= set(sufficienthit) & set( GoodCorrWorker)
    
    for row in MTRows:
        NewRow=dict()
        for fieldname  in fieldnames:
            NewRow[fieldname]=row[fieldname]
        keys=row.keys()
        Label=0
        CountLabel=0
        
        for key in keys:
            if key in finalWorker:
                try:
                    NewRow[key]=row[key]
                    Label=Label+float(row[key])
                    CountLabel=CountLabel+1
                except ValueError:
                    print
                       
        if CountLabel < 4:
            print row            
        ActLabel=Label/CountLabel
        NewRow["SimLabel"]=ActLabel
        AllRows.append(NewRow)
    csv_wrapper.write_csv(MT_RegressionLabel, AllRows)
        
        
if __name__ == '__main__':
    MTInput=os.path.dirname(os.getcwd()) + "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/AllMT_task/Results/MT_2_4_3_5_split_worker"
    MTCorr=os.path.dirname(os.getcwd()) + "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/AllMT_task/Results/MT_2_4_3_5_split_worker_Corr"
    MTNoHits=os.path.dirname(os.getcwd()) + "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/AllMT_task/Results/MT_2_4_3_5_split_worker_Hits"
    MT_Regression=os.path.dirname(os.getcwd()) + "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/AllMT_task/Results/MT_2_4_3_5_worker_Reg.csv"
    
    
    RegressionLabel(MTInput,MTCorr,MTNoHits, MT_Regression)