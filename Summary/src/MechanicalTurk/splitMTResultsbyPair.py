'''
Created on Nov 12, 2014
This program takes MT results from MT2 and creates a separate entry for each pair
This program takes MT results from MT3 and creates a separate entry for each pair
This program takes MT results from MT4 and creates a separate entry for each pair

@author: amita
'''
import operator
import itertools
import os
from data_pkg import FileHandling
from collections import defaultdict
from file_formatting import csv_wrapper
fields=["UMBC_","doccounta_","doccountb_","keya_","keyb_","label_cluster_", "stringa_","stringb_"]

def ReadRows(InputCsv):
    rows=FileHandling.read_csv(InputCsv)
    return rows
    
def splitRowPairwise(rowdicts,noofitemsHit):
    AllRows=list()
    rowdicts.sort(key=operator.itemgetter("HITId"))
    for key, items in itertools.groupby(rowdicts, operator.itemgetter('HITId')):
        Hitids=list(items)
        for count in range(1,noofitemsHit+1):
            NewDict=defaultdict()
            for row in Hitids:
                    NewDict["Id_"+ row["WorkerId"]]=row["Answer.response"+ str(count)]
            for field in fields:
                NewDict[field ]=row["Input."+field+ str(count)]        
            NewDict["HITId"]=row["HITId"]
            NewDict["HITTypeId"]=row["HITTypeId"] 
            AllRows.append(NewDict) 
            
    return AllRows        
                
                    
                    
def Execute(Input,Output,noofitemsHit): 
    rowdicts= ReadRows(Input)
    NewRows=splitRowPairwise(rowdicts,noofitemsHit)
    csv_wrapper.write_csv(Output, NewRows)
    
       
        
        
if __name__ == '__main__':
    topic="gay-rights-debates"
    Input=os.getcwd()+ "/"+ topic +"/MTdata_cluster/Labels_Updated/MT_task3/Results/Results_MT_Task3"
    Output= os.getcwd()+ "/"+ topic+"/MTdata_cluster/Labels_Updated/MT_task3/Results/MT_Task3_split_worker.csv"
    
    Input2=os.getcwd()+ "/"+ topic +"/MTdata_cluster/Labels_Updated/MT_task5/Results/Results_MT_Task5"
    Output2= os.getcwd()+ "/"+ topic+"/MTdata_cluster/Labels_Updated/MT_task5/Results/MT_Task5_split_worker.csv"
    
    
    
    #Input=os.getcwd()+ "/"+ topic +"/MTdata_cluster/Labels_Updated/MT_task4/Results/Results_MT_Task4"
    #Output= os.getcwd()+ "/"+ topic+"/MTdata_cluster/Labels_Updated/MT_task4/Results/MT_Task4_split_worker.csv"
    
    
    #Input=os.getcwd()+ "/"+ topic +"/MTdata_cluster/Labels_Updated/MT_task2/ResultsV3/MT2_web_interface"
    #Output=os.getcwd()+ "/"+ topic +"/MTdata_cluster/Labels_Updated/MT_task2/ResultsV3/MT2_web_interface_split_worker.csv"
    noofitemsHit=5
    Execute(Input,Output,noofitemsHit)
    Execute(Input2,Output2,noofitemsHit)