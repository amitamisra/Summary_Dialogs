'''
Created on Nov 5, 2014

@author: amita
'''
import os
from data_pkg import FileHandling

import operator
def split_UMBC_sampling(Input,outputcsv, items_hit, fields):
    rowdicts=FileHandling.read_csv(Input)
    AllRows=list()
    for row in rowdicts:
        for count in range(1,items_hit+1):
            NewRow=dict()
            for field in fields:
                NewRow[field]=row[field+str(count)]
            AllRows.append(NewRow)
                
    FileHandling.write_csv(outputcsv, AllRows, fields)    
    
def Sort_UMBC(oneitemInput,Output,field_sort):    
    Rows=FileHandling.read_csv(oneitemInput)
    NewRows=sorted(Rows,key=operator.itemgetter(field_sort))
    fieldnames=sorted(Rows[0].keys())
    FileHandling.write_csv(Output, NewRows, fieldnames)
    
    
if __name__ == '__main__':
    fields=["UMBC_","doccounta_","doccountb_","keya_","keyb_","label_cluster_", "stringa_","stringb_"]
    Input=os.path.dirname(os.getcwd()) + "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task3/MT_task3_5items"
    OutputFile=os.path.dirname(os.getcwd()) + "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task3/MT_task3_oneitem"
    sortedUMBC=os.path.dirname(os.getcwd()) + "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task3/MT_task3_oneitem_UMBCSorted"
    items_hit=5
    field_sort="UMBC_"
    split_UMBC_sampling(Input,OutputFile, items_hit, fields)
    Sort_UMBC( OutputFile,sortedUMBC,field_sort)