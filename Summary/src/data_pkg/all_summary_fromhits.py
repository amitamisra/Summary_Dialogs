#!/usr/bin/env python
#coding: utf8 
'''
Created on Jun 14, 2014
This file creates a summary file for pyramid with regular expression 
@author: amita
'''
import os
import FileHandling
import sys
import operator
import itertools
from collections import defaultdict
import NewFormat_text

# creates a batch file from individual hits, mapping file contains record nos from csv files used in Mechanical Turk for input
def CreateBatchFile(outbatchFile,directoryin,inputhitcsvdir,mappingfile,noofitems,BatchNo):
   
    filelist=os.listdir(inputhitcsvdir)
    rowlist=list()
    for inputhitcsv in filelist:
        first=True
        if not inputhitcsv.startswith('.'):
            rowdicts=FileHandling.read_csv(inputhitcsvdir +"/"+inputhitcsv[:-4])
            mappingrows=FileHandling.read_csv(mappingfile)
            for row in rowdicts:
                if first:
                    Hitid=row["HitId"]
                    rowmappingfile= next((item for item in mappingrows if item["HitId"] == Hitid), None) 
                    if rowmappingfile==None:
                        print "hit not found "+ str(Hitid)
                        sys.exit(1)
                        
                    record_No=rowmappingfile["record_no"]
                    filename=rowmappingfile["filename"]
                    inputrows=FileHandling.read_csv(directoryin+filename[:-4])
                    record=inputrows[int(record_No)]
                    first=False
                for count in range(1,noofitems+1):
                    row["Input.key"+str(count)]=record["key"+str(count)]
                    row["Input.Dialogtext"+str(count)]=record["Dialogtext"+str(count)]
                rowlist.append(row)
                   
    fieldnames=sorted(row.keys())        
    FileHandling.write_csv(outbatchFile, rowlist, fieldnames)    
        
def allSummary(inputBatchfile,combineddir): 
    dict_key=defaultdict(str)
    counter_key=defaultdict(int)
    rowdicts=FileHandling.read_csv(inputBatchfile)
    rowdicts.sort(key=operator.itemgetter("HitId"))
    for key, items in itertools.groupby(rowdicts, operator.itemgetter('HitId')):
        Hitids=list(items)
        for row in Hitids:
            
            if row["Status"]=="Approved":
                
                for count in range(1,noofitems+1):
                    key=row["Input.key"+str(count)]
                    Answer=row["Answer " +str(count)]
                    new_text=(NewFormat_text.ascii_only(Answer)) 
                    dict_key[key]=dict_key[key]+"\n"+ str(RegularExp[counter_key[key]]) + "\n" + new_text +"\n\n"
                    counter_key[key]=counter_key[key]+1
                    
    
    for key in dict_key.keys():
        outdir=combineddir
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        Outfile=outdir + "/"+key
        Lines=list()
        Lines.append(dict_key[key])
        FileHandling.WriteTextFile(Outfile, Lines)

    
    
    
   










if __name__ == '__main__':
    TaskNo=2        
    Noofsummaries=5 
    topic="gay-rights-debates"  
    noofitems=5 
    directoryin=os.getcwd()+ "/CSV/"+ topic +"/MTdata/MT"+ str(TaskNo)+"/"
    inputhitdir=directoryin +"MT"+str(TaskNo)+"Results/Mid_Results/HitResults/"       
    mappingfile= directoryin+ "MT"+str(TaskNo)+"Results/MT2_key_Hit_Mapping"   
    RegularExp=["----------\nD"+ str(i) +"\n"+ "----------" for i in range(Noofsummaries)]  
    BatchNo=1
    outbatchFile=directoryin +"MT"+str(TaskNo)+"Results/Mid_Results/BatchResult/ResultBatch"+str(BatchNo)
    #summary_no=3
    #allsummaryfile=os.getcwd()+ "/CSV/"+ topic +"/Summaries/summary_All/newsummary_"+str(summary_no)
    Batchinput=outbatchFile
    
    #CreateBatchFile(outbatchFile,directoryin,inputhitdir,mappingfile,noofitems,BatchNo) # call it once to create a batch file
    combineddir=os.getcwd()+ "/CSV/"+ topic +"/MTdata/MT2/MT2Summaries/MT2_midrange"
     
    allSummary(Batchinput,combineddir)