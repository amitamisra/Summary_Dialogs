'''
Created on Nov 16, 2014

@author: amita
'''
import os
import copy
from data_pkg import FileHandling
from file_formatting import csv_wrapper
import sys
clusterin2notin1=['30', '53', '44', '9', '25', '30', '28', '9', '4', '30', '20', '20', '45', '24', '45', '31', '31', '57', '20', '53', '4', '9', '56', '28', '30', '20', '4', '28', '4', '4', '45', '9', '25', '25', '53', '45', '9', '9', '30', '24', '56', '10', '28', '9', '45', '56', '53', '25', '10', '53', '4', '28', '30', '45', '52', '27', '28', '54', '9', '4', '64', '4', '58', '23', '4', '25', '30', '30', '30', '4', '28', '30', '30', '53', '25', '20', '20', '20', '25', '9', '25', '30', '25', '20', '25']
clusterin1notin2=['6', '6', '61', '37', '42', '42', '42', '42', '42', '0', '0', '0', '0', '0', '6', '6', '6', '6', '16', '16', '16', '16', '0', '0', '0', '0', '0', '42', '42', '42', '42', '42', '0', '0', '0', '0', '0', '66', '67', '16', '16']

def readCSV(InputCSV):
    rows=FileHandling.read_csv(InputCSV)
    return rows
def AddRows(InputCSV1,InputCSV2,Output):
    Allrows=[]
    Allclusters1=[]
    Allclusters2=[]
    rows1=readCSV(InputCSV1)
    rows2=readCSV(InputCSV2)
    for row in rows1:
        NewRow=dict()
        NewRow=copy.deepcopy(row)
        Allrows.append(NewRow)
        Allclusters1.append(row["label_cluster_"])
    for row in rows2:
        NewRow=dict()
        NewRow=copy.deepcopy(row)
        if  any(d['stringa_'] == row['stringa_'] and d['stringb_'] == row['stringb_'] for d in Allrows):
            print("row same")
            sys.exit()
        Allrows.append(NewRow) 
        Allclusters2.append(row["label_cluster_"]) 
    clusters= [obj for obj in Allclusters1 if obj not in Allclusters2]  
    print   clusters
    print
       
    csv_wrapper.write_csv(Output,Allrows)    
if __name__ == '__main__':
    topic="gay-rights-debates"
    # InputCSV1=os.getcwd()+ "/"+ topic+"/MTdata_cluster/Labels_Updated/MT_task2/ResultsV3/MT2_web_interface_split_worker"
    # InputCSV2=os.getcwd()+ "/"+ topic+"/MTdata_cluster/Labels_Updated/MT_task3/Results/MT_Task3_split_worker"
    # Output=os.getcwd()+ "/"+ topic+"/MTdata_cluster/Labels_Updated/AllMT_task/Results/MT_Task2_3split_worker.csv"
    
    
    InputCSV2=os.getcwd()+ "/"+ topic+"/MTdata_cluster/Labels_Updated/AllMT_task/Results/MT4_MT2_Gold_split_worker"
    InputCSV1=os.getcwd()+ "/"+ topic+"/MTdata_cluster/Labels_Updated/AllMT_task/Results/MT5_MT3_Gold_split_worker"
    Output=os.getcwd()+ "/"+ topic+"/MTdata_cluster/Labels_Updated/AllMT_task/Results/MT_2_4_3_5_split_worker.csv"
    
    
    AddRows(InputCSV1,InputCSV2,Output)