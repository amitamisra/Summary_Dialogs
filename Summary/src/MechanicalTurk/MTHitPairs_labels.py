'''
Created on Sep 1, 2014

@author: amita
'''
from data_pkg import FileHandling
import os
from random import shuffle
from splitMT3_forUMBCsampling import Sort_UMBC
from splitMT3_forUMBCsampling import split_UMBC_sampling
from splitMT1 import SplitMTHitscv

class MTPairs:
    def __init__(self,Input,Output,No_ofitem,No_ofhits,fields):
        self.Input=Input
        self.Output=Output
        self.No_ofitem=No_ofitem
        self.No_ofhits=No_ofhits
        self.fields=fields
        
    def ReadInput(self):
        Rowdicts=FileHandling.read_csv(self.Input)
        return Rowdicts
        
    def createhitinput(self,rowdicts):
        MTrow=dict()
        #shuffle(rowdicts) 
        Fieldnames=list()
        MTRows=list()
        intc=1
        extc=0
        first=True
        for row in rowdicts:
            if extc < self.No_ofhits:  
                
                if intc<=self.No_ofitem:
                    
                    for field in self.fields:                
                        MTrow[field +str("a")+"_"+str(intc)]=row[field+str(1)]
                        MTrow[field +str("b")+"_"+str(intc)]=row[field+str(2)] 
                         
                    MTrow["label_cluster" +"_"+str(intc)]=row["label_cluster"]
                    MTrow["UMBC" +"_"+str(intc)]=row["UMBC"]
                 
                    if first:
                        Fieldnames.append("label_cluster"+"_"+str(intc))
                        Fieldnames.append("UMBC" +"_"+str(intc))
                        for field in self.fields:   
                            Fieldnames.append(field +str("a")+"_"+str(intc))
                            Fieldnames.append(field +str("b")+"_"+str(intc))
                    intc=intc+1       
                                         
                if intc-1==self.No_ofitem:
                    MTRows.append(MTrow)   
                    extc=extc+1
                    intc=1
                    MTrow=dict()
                    first=False 
                    
            else:
                break
        #shuffle(MTRows) ( done this once to create MTpairsLabels)       
        FileHandling.write_csv(self.Output, MTRows, Fieldnames)            



    def creathittask3(self,rowdicts):
            MTrow=dict()
            Fieldnames=list()
            MTRows=list()
            intc=1
            extc=0
            first=True
            fields=rowdicts[0].keys()
            for row in rowdicts:
                if extc < self.No_ofhits:  
                    
                    if intc<=self.No_ofitem:
                        
                        for field in fields:                
                            MTrow[field +str(intc)]=row[field]
                             
                     
                        if first:
                            for field in fields:   
                                Fieldnames.append(field +str(intc))
                        intc=intc+1       
                                             
                    if intc-1==self.No_ofitem:
                        MTRows.append(MTrow)   
                        extc=extc+1
                        intc=1
                        MTrow=dict()
                        first=False 
                        
                else:
                    break
            #shuffle(MTRows) ( done this once to create MTpairsLabels)       
            FileHandling.write_csv(self.Output, MTRows, Fieldnames)            




def Execute(MTPairsobj):
    RowDicts=MTPairsobj.ReadInput()
    MTPairsobj.createhitinput(RowDicts)
    
def MTRowFilter(MTAllPairs,MT_task1,rowstart,rowend):
    AllRows=FileHandling.read_csv(MTAllPairs)
    fieldnames=sorted(AllRows[0].keys())
    FileHandling.write_csv(MT_task1, AllRows[rowstart:rowend], fieldnames)
    
def  callsplitUMBC(Input,Outputoneitem,sortedUMBC):
    fields=["UMBC_","doccounta_","doccountb_","keya_","keyb_","label_cluster_", "stringa_","stringb_"]
    items_hit=5
    field_sort="UMBC_"
    split_UMBC_sampling(Input,Outputoneitem, items_hit, fields)
    Sort_UMBC( Outputoneitem,sortedUMBC,field_sort)

def RemovelastnumberMT(PairsFile,output2): # removes _1 as last char in each fieldname for CORENLP 
    rows= FileHandling.read_csv(PairsFile)
    AllRows=[]
    for row in rows:
        newrow=dict()
        for key in row.keys():
            newrow[key[:-1]]=row[key]
        AllRows.append(newrow)
    fieldnames=AllRows[0].keys()    
    FileHandling.write_csv(output2, AllRows, fieldnames)    
if __name__ == '__main__':
    topic="gun-control"
    Input="/Users/amita/git/FacetIdentification/src/Paraphrase_Pkg_Data/" + topic + "/cluster/Phase1/TFIdf/Pairs_Cos_Cluster_70_AVG_Noun_Verb_Ad"
    Output="/Users/amita/git/FacetIdentification/src/MechanicalTurk_Pkg_Data/" + topic + "/MTdata/Phase1/MTdata_cluster/MT_PairsLabels"
    Output2="/Users/amita/git/FacetIdentification/src/MechanicalTurk_Pkg_Data/" + topic + "/MTdata/Phase1/MTdata_cluster/MT_Nolastchar_PairsLabels"
    #MT_task1=os.path.dirname(os.getcwd()) + "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task1"
    #rowstart=0 # starting row from MTFile
    #rowend=50 #last row to include in MTfile
    No_ofitem=1 
    No_ofhits=528
    fields=["string","key","doccount"]  
    MTPairsobj=MTPairs(Input,Output,No_ofitem, No_ofhits,fields)
    Execute(MTPairsobj)
    #MTRowFilter(Output,MT_task1,rowstart,rowend)  # select the rows to be put on MT
    RemovelastnumberMT(Output,Output2)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#------------------------------------------------------------------------------ done for NAACL
#------------------------------------------------------------------------------ 
    #------------------------------------------------ topic="gay-rights-debates"
#------------------------------------------------------------------------------ 
    #-------------------------------------------- # did this for task1 and task2
    # #===========================================================================
    # # Input=os.path.dirname(os.getcwd()) + "/paraphrase/para_data/gay-rights-debates/cluster/LabelUpdated/TFIdf/Pairs_Cos_Cluster_70_AVG_Noun_Verb_Ad"
    # # Output=os.path.dirname(os.getcwd()) + "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_PairsLabels"
    # # MT_task1=os.path.dirname(os.getcwd()) + "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task1"
    #----------------------------------- # rowstart=0 # starting row from MTFile
    #-------------------------------- # rowend=50 #last row to include in MTfile
    # # #No_ofitem=10 done for MT1 task, for second task split one hit of 10 pairs into 2 hits of 5 pairs each
    #---------------------------------------------------------- # #No_ofhits=180
    #------------------------------------------------------------- # No_ofitem=5
    #----------------------------------------------------------- # No_ofhits=360
    #-------------------------------------- # fields=["string","key","doccount"]
    #------------ # MTPairsobj=MTPairs(Input,Output,No_ofitem, No_ofhits,fields)
    #----------------------------------------------------- # Execute(MTPairsobj)
    #---------------------------- # MTRowFilter(Output,MT_task1,rowstart,rowend)
    # #===========================================================================
#------------------------------------------------------------------------------ 
    #------------------------------------------------------------ #Now for task3
    # #Muse MT_PairsLabels beginning from row 51 till last, rows 1 to 50 done for task2
    #--------------------------------------------------------------- rowstart=50
    #---------------------------------------------------------------- rowend=115
    # Input =os.path.dirname(os.getcwd()) + "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_PairsLabels"
    # Task3_10items=os.path.dirname(os.getcwd()) + "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task3/MT_task3_10items"
    # Task3_5items=os.path.dirname(os.getcwd()) + "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task3/MT_task3_5items"
#------------------------------------------------------------------------------ 
    # Outputoneitem=os.path.dirname(os.getcwd()) + "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task3/MT_task3_oneitem"
    # sortedUMBC=os.path.dirname(os.getcwd()) + "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task3/MT_task3_oneitem_UMBCSorted"
#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
    # MTRowFilter(Input,Task3_10items,rowstart, rowend) #Already done this, do this once
    #----------------------------------------- # This gives 10 pairs for task 3,
#------------------------------------------------------------------------------ 
    # #execute splitMT1.SplitMTHitscv to get 5 pairs in a hit ,this gives MT_task3_5items.csv
    #--------------------------------- SplitMTHitscv(Task3_10items,Task3_5items)
#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
    #------------------- #however we need to sample to keep top 500 UMBC values.
    #------------------------------------- # so separate them as individual rows
    #------------------- # This gives pairs with one item sorted on UMBC values.
#------------------------------------------------------------------------------ 
    #--------------------- callsplitUMBC( Task3_5items,Outputoneitem,sortedUMBC)
#------------------------------------------------------------------------------ 
    # # For task MTTask3 take top 500 from UMBC sorted File below so start from row Number 531 in UMBCSortedFile
    #------------------------------------------------------------- No_ofhits=100
    #--------------------------------------------------------------- No_ofitem=5
    #---------------------------------------- fields=["string","key","doccount"]
    # UMBCSortedFile=os.path.dirname(os.getcwd()) + "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task3/MT_task3_oneitem_UMBCSorted"
    # UMBCTOP500=os.path.dirname(os.getcwd()) + "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task3/MT_task3_oneitem_UMBCTop500"
    # randomUMBC=os.path.dirname(os.getcwd()) + "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task3/MT_task3_UMBCTop500Random"
#------------------------------------------------------------------------------ 
    # # take only top 500 rows, since UMBCSortedFile is sorted in inc order stary from row 531to last row
    #-------------------------------------------------------------- rowstart=130
    #---------------------------------------------------------------- rowend=632
    #-------------------- MTRowFilter(UMBCSortedFile,UMBCTOP500,rowstart,rowend)
#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
    # MTTask3File=os.path.dirname(os.getcwd()) + "/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task3/FinalMT_task3_TopUMBCRandom"
    #----------------------------- FileHandling.Randomize(UMBCTOP500,randomUMBC)
    #---- MTPairsobj=MTPairs(randomUMBC,MTTask3File,No_ofitem, No_ofhits,fields)
    #------------------------------------------- RowDicts=MTPairsobj.ReadInput()
    #---------------------------------------- MTPairsobj.creathittask3(RowDicts)
#------------------------------------------------------------------------------ 
#------------------------------------------------------------------------------ 
else:
    pass    