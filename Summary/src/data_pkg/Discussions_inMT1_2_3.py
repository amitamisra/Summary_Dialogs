''' NOT USED NOW , USE AllDialogFile.py
Created on Nov 22, 2014
This file contains all the discussions for dialogs in MT1,MT2,MT3
@author: amita
'''
import FileHandling
import re
from file_formatting import csv_wrapper

def Add(rows,AllRows,keys):
    for row in rows:
        for key in keys:
            NewRow=dict()
            keyfield=row[key] 
            dis_post_list=re.split('_|-',keyfield)
            NewRow["dataset"]=dis_post_list[0]
            NewRow["discussion_id"]=dis_post_list[1]
            lastindex=len(dis_post_list)
            NewRow["posts_dialogNo"]="_".join(dis_post_list[2:lastindex])
            AllRows.append(NewRow)     
    
def AddDiscussions(MT1,MT2_mid,MT2_more750,MT3_mid,MT3_more750,AllMT):
    
    rows1=FileHandling.read_csv(MT1)
    rows2=FileHandling.read_csv(MT2_mid)
    rows3=FileHandling.read_csv(MT2_more750)
    rows4=FileHandling.read_csv(MT3_mid)
    rows5=FileHandling.read_csv(MT3_more750)
    
    keys1=["key1","key2","key3"]
    keys2=["key1","key2","key3","key4","key5"]
    AllRows=list()
    Add(rows1,AllRows,keys1)
    Add(rows2,AllRows,keys2)
    Add(rows3,AllRows,keys2)
    Add(rows4,AllRows,keys2)
    Add(rows5,AllRows,keys1)
    csv_wrapper.write_csv(AllMT,AllRows)
            
    

if __name__ == '__main__':
    MT1="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/MTdata/MT1/MT_task1"
    MT2_mid="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/MTdata/MT2/MT2_midrange"
    MT2_more750="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/MTdata/MT2/MT2_more750"
    MT3_mid="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/MTdata/MT3/MT3_midrange"
    MT3_more750="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/MTdata/MT3/MT3_more750"
    AllMTdata="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/MTdata/AllMTdata/MT123.csv"
    
    ALLMTdataNoDup="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/MTdata/AllMTdata/MT123_NoDup"
    AllMTdataDup="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/MTdata/AllMTdata/MT123"
    
    #AddDiscussions(MT1,MT2_mid,MT2_more750,MT3_mid,MT3_more750,AllMTdata)
    FileHandling.RemoveDup(AllMTdataDup,ALLMTdataNoDup)
    
    