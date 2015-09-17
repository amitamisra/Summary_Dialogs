'''
Created on Oct 18, 2014

@author: amita
'''
import sys
from collections import defaultdict
from data_pkg import FileHandling
from file_formatting import csv_wrapper

def RemaininHits(Hitcsv,combinedcsv,allhit_batch):
    HitnotinBatch=[{"hitid":"3ICOHX7ENCBA5WA1R6IDZACZMORE0Y","tup": ("Broadened marriage is a side effect of legal gay marriage","Opponents of gay marriage are not protecting traditional marriage, but are discriminating against homosexuals.")},
                   {"hitid":"3ZUE82NE0A1KTZF0HLFYA73HHNI8FX","tup":("marriage is defined as a family unit based on natural heterosexual contact","heterosexual nature of the relationship that is important, not how the children are conceived within the relationship")},
                   {"hitid":"3VMV5CHJZ8F95J3JV3WBJOZGWF3GTT","tup":("discussion of " +'"{}"'.format("morality")  +" is a safe ground because morality is relative and subjective","when people claim religion in doing prejudice they are actually abandoning their morals" )},
                   {"hitid":"3BS6ERDL9370R1IGX0NA2T45ZFBD64","tup":("Statistics regarding AIDs in Africa show that is is not a homosexual disease.","spread of AIDS was caused by unprotected sex")},
                   {"hitid":"309D674SHZLWSLTXTV97T38FSGBBCO","tup":("gay marriage is unlikely to be recognized in future","allows marriage officers the right not to perform a same-sex marriage if it conflicts with their conscience, religion, or beliefs")},
                   {"hitid":"3MIVREZQVHY1FP7A4QNVCBGMJPKKQL","tup":("No reason for discrimination against homosexual marriage","in the next 20 years the wave of gay marriage legalization will be over")},
                   {"hitid":"3ZVPAMTJWN3WP4QRRERGJ9YY8U6GRG","tup":("little financial impact on support for homosexual marriage","opponents of homosexual marriage tend to argue that a change to marriage law would make it too open ended") },
                   {"hitid":"3FHTJGYT8N0BDRACEMNREEYJ7CIGPO","tup":("Gay couples are unable to get any benefits that married people do.","referring to namecalling and violence from the original post that was opposing gay rights")}]
   
    InputhitCSVMT2="/Users/amita/git/summary_repo/Summary/src/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task2/MT_task2"

    Hitdicts=FileHandling.read_csv(Hitcsv)
    rowdicts=FileHandling.read_csv(InputhitCSVMT2)
    combineddicts=FileHandling.read_csv(combinedcsv)
    
    Newlist=list()
    Responses=["Answer.response1",  "Answer.response2", "Answer.response3",   "Answer.response4", "Answer.response5"] 
    CopyBatchkeys=["Title","Description","Keywords","Reward","CreationTime","MaxAssignments","RequesterAnnotation",\
             "AssignmentDurationInSeconds","AutoApprovalDelayInSeconds", "Expiration", "NumberOfSimilarHITs","LifetimeInSeconds"]
    for combineddict in combineddicts:
        Newlist.append(combineddict)
        combineddictkeys=combineddict.keys()
        
    for listcount in range(0,8):
        for count in range(1,6):
            row1=[row for row in rowdicts if row["stringa_"+str(count)]== HitnotinBatch[listcount]["tup"][0] and row["stringb_"+str(count)]==HitnotinBatch[listcount]["tup"][1]]
            if row1:
                break
        if len(row1)>1:
                print"error"
        else:
                
                HitRecs=[hitrec for hitrec in Hitdicts if hitrec["hitid"]==HitnotinBatch[listcount]["hitid"] ]
                for  hitrec in HitRecs:
                    NewDict=defaultdict()
                    NewDict["HITId"]=HitnotinBatch[listcount]["hitid"]
                    NewDict["WorkerId"]=hitrec["workerid"]
                    NewDict["AssignmentId"]=hitrec["assignmentid"]
                    NewDict["HITTypeId"]=hitrec["hittypeid"]
                    
                    for (key,items)in row1[0].iteritems():
                        NewDict["Input."+key]=items
                    for reskey in Responses:
                        NewDict[reskey]=hitrec[reskey]
                    for copykey in  CopyBatchkeys:
                        NewDict[copykey]= combineddicts[0][copykey]
                            
                    Newlist.append(NewDict) 
                    newdictkeys=NewDict.keys() 
                    if newdictkeys ==  combineddictkeys:
                        print "keys equal" 
                    else:
                        print " not equal"    
                    
    fieldnames=sorted(newdictkeys)                   
    FileHandling.write_csv(allhit_batch,Newlist, fieldnames)          
            

# This function combines the hits genertaing by generate results and results web interface.
# Before using this download using get results api, use tab as separator, open in google drive, import as spreadsheet
#------------------------------------------------------------------ save as csv.
#-- If assignment id matches, get the dict from batch file append it to new file
#------------------------------------- otherwise  use 4 different types of keys.
# CopyBatchKeysFirst type get values from batch and are same for a hit.Find a matching hit id and  just copy the values of those keys from batchfile to new file
#--------------- batchKeys and HitKeys is 1-1 mapping between batch and hit keys
#----------------- count keys are taken from batch file with same hit id.__call_
#-------------------------------------------- response keys are taken from hitid
def combineBatch_withHits(BatchCSV,HitCSV,CombinedBatchHit):
    CopyBatchkeys=["Title","Description","Keywords","Reward","CreationTime","MaxAssignments","RequesterAnnotation",\
             "AssignmentDurationInSeconds","AutoApprovalDelayInSeconds", "Expiration", "NumberOfSimilarHITs","LifetimeInSeconds"]
    
    BatchKeys=["HITId","HITTypeId","AssignmentId", "WorkerId","AssignmentStatus","AcceptTime", "SubmitTime", "AutoApprovalTime", "ApprovalTime",\
                "RejectionTime", "RequesterFeedback", "WorkTimeInSeconds","LifetimeApprovalRate", "Last30DaysApprovalRate", \
                 "Last7DaysApprovalRate", "Answer.comments","Approve","Reject"]
    Hitkeys=["hitid",   "hittypeid","assignmentid",  "workerid", "assignmentstatus", "assignmentaccepttime","assignmentsubmittime", \
             "autoapprovaltime", "assignmentapprovaltime", "assignmentrejecttime", "feedback",   "assignmentduration",\
             "numcomplete","numpending","hitlifetime","Answer.comments","hitstatus","reject"]
    Responses=["Answer.response1",  "Answer.response2", "Answer.response3",   "Answer.response4", "Answer.response5"] 
    countkeys=["Input.UMBC_","Input.doccounta_", "Input.doccountb_","Input.keya_", "Input.keyb_", "Input.label_cluster_","Input.stringa_","Input.stringb_"]              

    BatchRows=FileHandling.read_csv(BatchCSV)
    HitRows= FileHandling.read_csv(HitCSV)
    NewRows=list()
    lenBatchkeys=len(BatchKeys)
    for row in HitRows:
        keyass="assignmentid"
        BatchFound=[DictBatch for DictBatch in BatchRows if row[keyass] == DictBatch["AssignmentId"] ]
        if BatchFound:
            keyhitid="hitid"
            if row[keyhitid]== BatchFound[0]["HITId"]:
                keyworker="workerid"
                if row[keyworker]== BatchFound[0]["WorkerId"] : 
                    if len(BatchFound)==1:
                        NewRows.append(BatchFound[0])
                    else:
                        print"error in assignment" +str(row[keyass])         
                else:
                    print"error in assignment" +str(row[keyass])   
                     
            else:
                print"error in assignment" +str(row[keyass])   
        else:
            NewDict=defaultdict()
            keyhitid="hitid"
            HitDict=[DictBatch for DictBatch in BatchRows if row[keyhitid]== DictBatch["HITId"] ]
            if len(HitDict)==0:
                print " hitid not found" +str(row[keyhitid])
            else:    
                for keysfromBatch in CopyBatchkeys:
                    NewDict[keysfromBatch]=HitDict[0][keysfromBatch]
                for countkey in countkeys:
                    for counter in range(1,6):    
                        NewDict[countkey+str(counter)]=HitDict[0][countkey+str(counter)]
                for key_no in range(0,lenBatchkeys) :
                    key_nohit=Hitkeys[key_no]
                    NewDict[BatchKeys[key_no]] = row[key_nohit]   
                for response in  Responses:
                    hitresponse=response
                    NewDict[response]=row[hitresponse]
                
                NewRows.append(NewDict)
    fieldnames=sorted(NewRows[0].keys()) 
    FileHandling.write_csv(CombinedBatchHit,NewRows, fieldnames)       

        


def FindHitwithSameString(MT1CSV,MT2CSV,M1_MT2):
    MT1keys=["Title","Description","Keywords","Reward","CreationTime","MaxAssignments","RequesterAnnotation","AssignmentDurationInSeconds", \
             "AutoApprovalDelayInSeconds", "Expiration", "NumberOfSimilarHITs","LifetimeInSeconds","AssignmentId", "WorkerId","AssignmentStatus",\
            "AcceptTime", "SubmitTime", "AutoApprovalTime", "ApprovalTime", "RejectionTime", "RequesterFeedback", "WorkTimeInSeconds", "WorkerId",\
            "LifetimeApprovalRate", "Last30DaysApprovalRate",  "Last7DaysApprovalRate", "Answer.comments","Approve","Reject"]
    MT2countkeys=["Input.UMBC_","Input.doccounta_", "Input.doccountb_","Input.keya_", "Input.keyb_", "Input.label_cluster_","Input.stringa_", \
             "Input.stringb_"]
    MT1Rows= FileHandling.read_csv(MT1CSV)
    MT2Rows= FileHandling.read_csv(MT2CSV)
    NewRows=list()
    for rowMT1 in MT1Rows:
        if rowMT1["WorkerId"]=="AC3VLHA8082IA": # only take this worker as other may be duplicate for MT2
        
            Newdict1=dict()
            Newdict2=dict()
            for count in range(1,6):
                stringaMT1=rowMT1["Input.stringa_"+ str(count)]
                stringbMT1=rowMT1["Input.stringb_"+ str(count)]
                
                AllworkersHit = [d for d in MT2Rows if d["Input.stringa_"+ str(count)] == stringaMT1 and d["Input.stringb_"+ str(count)] == stringbMT1]
                if len(AllworkersHit)==0:
                    print" keys not present for  assignment of MT1" + rowMT1["AssignmentId"]
                    #sys.exit()
                    break
                
                if  AllworkersHit:
                    
                    for key_count in  MT2countkeys: 
                        if rowMT1[key_count+ str(count)] != AllworkersHit[0][key_count+ str(count)]:
                            print" keys not same for assignment in MT1" + rowMT1["AssignmentId"]
                            sys.exit()
                        else:    
                            Newdict1[key_count+ str(count)] = AllworkersHit[0][key_count+ str(count)] 
                            Newdict1["Answer.response"+ str(count)]=rowMT1["Answer.response"+ str(count)]
            for keys_1 in MT1keys:
                Newdict1[keys_1]=rowMT1[keys_1]
            if  AllworkersHit:   
                Newdict1["HITId"]=AllworkersHit[0]["HITId"]
                Newdict1["HITTypeId"]=AllworkersHit[0]["HITTypeId"] 
                for workerHit in AllworkersHit:
                        NewRows.append(workerHit)
                NewRows.append(Newdict1)        
                       
            for count in range(6,11):
                stringaMT1=rowMT1["Input.stringa_"+ str(count)]
                stringbMT1=rowMT1["Input.stringb_"+ str(count)]
                
                AllworkersHit = [d for d in MT2Rows if d["Input.stringa_"+ str(count-5)] == stringaMT1 and d["Input.stringb_"+ str(count-5)] == stringbMT1]
                if  AllworkersHit:
                #===================================================================
                # if len(AllworkersHit)==0:
                #     print" keys not present for  assignment in MT1" + rowMT1["AssignmentId"]
                #     sys.exit()
                #===================================================================
                    for key_count in  MT2countkeys: 
                        if rowMT1[key_count+ str(count)] != AllworkersHit[0][key_count+ str(count-5)]:
                            print" keys not same for assignment in MT1" + rowMT1["AssignmentId"]
                            sys.exit()
                        else:    
                            Newdict2[key_count+ str(count-5)] = AllworkersHit[0][key_count+ str(count-5)] 
                            Newdict2["Answer.response"+ str(count-5)]=rowMT1["Answer.response"+ str(count)]
                else:
                    print" keys not present for  assignment of MT1" + rowMT1["AssignmentId"]
                    #sys.exit()
                    break
                    
            
            
            for keys_1 in MT1keys:
                Newdict2[keys_1]=rowMT1[keys_1]
            if  AllworkersHit:    
                Newdict2["HITId"]=AllworkersHit[0]["HITId"]
                Newdict2["HITTypeId"]=AllworkersHit[0]["HITTypeId"] 
                for workerHit in AllworkersHit:
                        NewRows.append(workerHit)
                NewRows.append(Newdict2)                 
     
    fieldnames=NewRows[0].keys()        
    FileHandling.write_csv(M1_MT2, NewRows, fieldnames)           
    






















if __name__ == '__main__':
 
    InputBatch="/Users/amita/git/summary_repo/Summary/src/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task2/ResultsV2/MT2_Batch"
    InputHit="/Users/amita/git/summary_repo/Summary/src/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task2/ResultsV2/Corected_MT2_Hit_Results"
    CombinedBatchHit="/Users/amita/git/summary_repo/Summary/src/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task2/ResultsV2/MT2_Results_hits_Batch"
    allhit_batch="/Users/amita/git/summary_repo/Summary/src/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task2/ResultsV2/MT2_AllResults_hits_Batch"
    
    MT1_MT2="/Users/amita/git/summary_repo/Summary/src/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task2/ResultsV2/MT1_MT2"
    InputCsv1="/Users/amita/git/summary_repo/Summary/src/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task1/MT1_Results/MT1_Results"
    InputCsv2=allhit_batch
    
    combineBatch_withHits(InputBatch,InputHit,CombinedBatchHit)
    RemaininHits(InputHit,CombinedBatchHit,allhit_batch)
    FindHitwithSameString(InputCsv1,InputCsv2,MT1_MT2)