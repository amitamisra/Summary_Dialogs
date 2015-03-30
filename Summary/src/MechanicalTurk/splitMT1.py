'''
Created on Sep 25, 2014
THIS PROGRAM takes the hit constructed in MT1 and splits it into 2 hits 2 with 5 pairs each, i.e split each row of MT1 into 2 rows
chnanging field names from stringa_5 to strina_10

Take an input hit with 10 items in File "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task3/MT_task3_10items" and split it 
into 2 hits with 5 pairs each for MTtask3. The input contains row beginning 51 to last from MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_PairsLabels
    

@author: amita
'''
import os
from data_pkg import FileHandling
def SplitMTHitscv(InputHitMT1,Output):
    AllRows=list()
    rows=FileHandling.read_csv(InputHitMT1)
    #key_not_6_10=["stringa_6","stringa_7","stringa_8","stringa_9","stringa_10","stringb_6","stringb_7","stringb_8","stringb_9","stringb_10"]
    #list_not_1_5=["stringa_1","stringa_2","stringa_3","stringa_4","stringa_5","stringb_1","stringb_2","stringb_3","stringb_4","stringb_5"]
    list1_5=["1","2","3","4","5"]
    list6_10=["6","7","8","9","0"]
    for row in rows:
        dict1to5=dict()
        dict6to10=dict()
        for key in row.keys():
            key6_10=""
            if key[-1]  in list1_5:
                dict1to5[key]=row[key]
                continue
            if key[-1]  in list6_10: 
                if key[-1]=="6":
                    key6_10=key[:-1]+"1"
                else:
                    if key[-1]=="7":
                        key6_10=key[:-1]+"2"
                    else:
                        if key[-1]=="8":
                            key6_10=key[:-1]+"3"
                        else:
                            if key[-1]=="9":
                                key6_10=key[:-1]+"4"
                            else:
                                if key[-1]=="0":
                                    key6_10=key[:-2]+"5"   
            dict6to10[key6_10]=row[key]    
                
        AllRows.append(dict1to5)            
        AllRows.append(dict6to10)    
                
    fieldnames=sorted(AllRows[0].keys())
    FileHandling.write_csv(Output, AllRows, fieldnames)                              
                
        
if __name__ == '__main__':
    topic="gay-rights-debates"
    
    # done for Task2
    #------------------------------------------------------------- Inputtaskno=1
    #------------------------------------------------------------ OutputtaskNo=2
    #-------- InputDir=os.getcwd()+  "/"+topic+"/MTdata_cluster/Labels_Updated/"
    # InputFile=InputDir+"MT_task"+ str(Inputtaskno)+"/" +"MT_task"+str(Inputtaskno)
    # OutFile=InputDir + "MT_task"+ str(OutputtaskNo) +"/MT_task"+ str(OutputtaskNo)
    #------------------------------------------ SplitMTHitscv(InputFile,OutFile)
    
    #Now for task3
    InputFile=os.path.dirname(os.getcwd()) + "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task3/MT_task3_10items"
    OutputFile=os.path.dirname(os.getcwd()) + "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task3/MT_task3_5items"
    SplitMTHitscv(InputFile,OutputFile)
    