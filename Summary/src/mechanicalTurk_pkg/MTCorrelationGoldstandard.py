''' Not needed now
Created on Oct 14, 2014
This files pairs up Annotators with gold standard labels for finding the correlation.
takes input as batch file .For labels input is MT1_Mt2 contains all labels from hits ,batch task1 and task2
@author: amita
'''
from data_pkg import FileHandling
import itertools 
import operator
import os
from collections import defaultdict
class PairsMT:
    def __init__(self,Input,Output,Overlapping4,corr_4Annotator,AllA2_019,OverlapingA2_019,noofitems_inhit):
        self.input=Input
        self.output=Output
        self.noofitems_inhit=noofitems_inhit
        self.Overlapping4=Overlapping4
        self.corr_4Annotator=corr_4Annotator
        self.AllA2_019=AllA2_019
        self.OverlapingA2_019=OverlapingA2_019
    def ReadMTHitpairs(self):
        InputRows=FileHandling.read_csv(self.input)
        return InputRows
    
      
                

    def ProcessRowsWorkers(self,Rowdicts):
            correlation4fieldnames=sorted(["A2TNNKHFNY5WQ4_GoldstandardAnswer.response_","A3TQD8CNO16IZKAnswer.response_",\
            "AC3VLHA8082IAAnswer.response_","ADUJUZANFOWKWAnswer.response_","HITId","Input.UMBC_","Input.stringa_","Input.stringb_"])
            correlation_A2019=sorted(["A2TMWYLZY40I9Answer.response_","A2TNNKHFNY5WQ4_GoldstandardAnswer.response_","HITId","Input.UMBC_","Input.stringa_","Input.stringb_"])
            
            worker_list=[row["WorkerId"] for row in Rowdicts ] # get all workers ids
            AllHitsAllWorker=list()
            unique_worker=set(worker_list)  # get all unique workers ids
            AllRows=list()
            workerhits=list()
            for worker in unique_worker:
                AllHitsAllWorker.append([row for row in Rowdicts if row["WorkerId"]==worker]) # construct list of lists, each list consists of hits by a worker, each row contains one hit by a worker
            Gold_Standard=[worker_row for worker_row in   AllHitsAllWorker if worker_row[0]["WorkerId"]==  "A2TNNKHFNY5WQ4"][0]
            for row in Gold_Standard:
                worker_alsoin_gold=list()
                for allhits_worker in AllHitsAllWorker:# get the hit corresponding to gold standard hit for a worker, allhits_worker is all hits by a worker
                    for worker_hit in allhits_worker:
                        if worker_hit["HITId"]==row["HITId"]:
                            workerhits.append(worker_hit) 
                            worker_alsoin_gold.append(worker_hit["WorkerId"])
                for count in range(1,self.noofitems_inhit+1):
                    dict_key=defaultdict(lambda:-1)
                    dict_key["HITId"]=row["HITId"]
                    dict_key["Input.UMBC_"]=row["Input.UMBC_"+ str(count)]
                    dict_key["Input.stringa_"]=row["Input.stringa_"+str(count)]
                    dict_key["Input.stringb_"]=row["Input.stringb_"+str(count)]
                    dict_key["A2TNNKHFNY5WQ4_Goldstandard"+"Answer.response_"]=row["Answer.response"+str(count)]
                    for worker_gold_hit in workerhits:#hit for a worker corresponding to gold standard hit
                        dict_key[worker_gold_hit["WorkerId"]+"Answer.response_"]=worker_gold_hit["Answer.response"+str(count)]
                    for workerid in unique_worker:
                        if workerid not in worker_alsoin_gold:
                            dict_key[workerid+"Answer.response_"]=-1
                            
                    AllRows.append(dict_key)
            
            fieldnames=sorted(AllRows[0].keys())
            FileHandling.write_csv(self.output, AllRows, fieldnames)
            
            FileHandling.write_csv(self.corr_4Annotator, AllRows, correlation4fieldnames)
            FileHandling.write_csv(self.AllA2_019,AllRows,correlation_A2019)
            
            
            
            return AllRows              
def KeepOverlappingRows(inputfile,overlapping4File) :
        AllRows=FileHandling.read_csv(inputfile)
        NewRows=list()
        for row in AllRows:
            append=True
            keys=row.keys()
            for key in keys:
                blankfield=str(row[key]).strip()
                if row[key]==str(-1) or blankfield=="":
                    append=False
                    break
            if append:       
                NewRows.append(row)
        fieldnames=sorted(NewRows[0].keys())
        FileHandling.write_csv(overlapping4File, NewRows, fieldnames)          
                
def Execute(pairsMTobj): 
    inputrows=pairsMTobj.ReadMTHitpairs()
    AllRows=pairsMTobj.ProcessRowsWorkers(inputrows) 
   # fieldnames=sorted(AllRows[0].keys())
    #FileHandling.write_csv(pairsMTobj.output, AllRows, fieldnames) 
   
def corrrelaton_Input(pairsMTobj):   
    correlation_4Annottaor=pairsMTobj.corr_4Annotator
    KeepOverlappingRows(correlation_4Annottaor,pairsMTobj.Overlapping4) 
    KeepOverlappingRows(pairsMTobj.AllA2_019,pairsMTobj.OverlapingA2_019)   
          
if __name__ == '__main__':
    inputfile=os.getcwd() + "/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task2/ResultsV2/MT1_MT2"
    outputfile=os.getcwd() + "/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task2/ResultsV2/CorrelationMT1_MT2"
    corr_4Annotator=os.getcwd() + "/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task2/ResultsV2/CorrelationMT1_MT2_4Annotator"
    Overlapping4=os.getcwd() + "/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task2/ResultsV2/OverlappingCorrelation_4_MT1_MT2"
    OverlapingA2_019=os.getcwd() + "/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task2/ResultsV2/OverlappingCorrelation_A2_019MT1_MT2"
    AllA2_019=os.getcwd() + "/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task2/ResultsV2/Correlation_A2_019MT1_MT"
    noofitems_inhit=5
    PairsMTobj=PairsMT(inputfile,outputfile,Overlapping4,corr_4Annotator,AllA2_019,OverlapingA2_019,noofitems_inhit)
    Execute(PairsMTobj)
    corrrelaton_Input(PairsMTobj)
    pass












#===============================================================================
# def ProcessRows(self,rowdicts):
#         rowdicts.sort(key=operator.itemgetter("HITId"))
#         AllRows=list()
#         for key, items in itertools.groupby(rowdicts, operator.itemgetter('HITId')):
#             Hitids=list(items)
#             count=1
#             dict_key=defaultdict(lambda: -1)
#             for row in Hitids: 
#                 
#                 #for count in range(1,self.noofitems_inhit+1):
#                 dict_key["HITId"]=row["HITId"]
#                 dict_key["worker"+ str(count)]=row["WorkerId"]
#                 dict_key["Input.UMBC_1"]=row["Input.UMBC_1"]
#                 dict_key["Input.UMBC_2"]=row["Input.UMBC_2"]
#                 dict_key["Input.UMBC_3"]=row["Input.UMBC_3"]
#                 dict_key["Input.UMBC_4"]=row["Input.UMBC_4"]
#                 dict_key["Input.UMBC_5"]=row["Input.UMBC_5"]
#                 dict_key["Input.stringa_1"]=row["Input.stringa_1"]
#                 dict_key["Input.stringb_1"]=row["Input.stringb_1"]
#                 dict_key["Input.stringa_2"]=row["Input.stringa_2"]
#                 dict_key["Input.stringb_2"]=row["Input.stringb_2"]
#                 dict_key["Input.stringa_3"]=row["Input.stringa_3"]
#                 dict_key["Input.stringb_3"]=row["Input.stringb_3"]
#                 dict_key["Input.stringa_4"]=row["Input.stringa_4"]
#                 dict_key["Input.stringb_4"]=row["Input.stringb_4"]
#                 dict_key["Input.stringa_5"]=row["Input.stringa_5"]
#                 dict_key["Input.stringb_5"]=row["Input.stringb_5"]
#                 dict_key["Worker_"+ str(count)+"Answer.response_1"]=row["Answer.response1"]
#                 dict_key["Worker_"+ str(count)+"Answer.response_2"]=row["Answer.response2"]
#                 dict_key["Worker_"+ str(count)+"Answer.response_3"]=row["Answer.response3"]
#                 dict_key["Worker_"+ str(count)+"Answer.response_4"]=row["Answer.response4"]
#                 dict_key["Worker_"+ str(count)+"Answer.response_5"]=row["Answer.response5"]
#                 count=count+1
#             AllRows.append(dict_key)
#         return AllRows              
#===============================================================================