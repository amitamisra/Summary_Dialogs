#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Jun 26, 2014
This file combines all the input dialogs put on mechanical turk and corresponding summaries in text file for which pyramid annotations exist
in Allpyramid directory for Allpyramids_v1 ,shuffles the rows and puts them  into one csvfile
@author: amita
'''
import os
import FileHandling
import NewFormat_text
import itertools
from operator import itemgetter
from bs4 import BeautifulSoup
import re
from random import shuffle

# create an allsummaries and all dialogs file for which pyramid has been constructed
def combineMTVBatch(InputDir,InputdirSummary,InputFile,Allrows,noofitems,task,AllPyramid):
            keys=os.listdir(AllPyramid)
            #summarydir= InputDir +"MT"+str(task) + "Summaries/" + InputFile+"/"
            rowdicts=FileHandling.read_csv(InputDir+InputFile)
            for row in rowdicts:
                for count in range(1,noofitems+1):
                        found = any( row["key"+str(count)] in x for x in keys)
                        if task == str("3") and topic=="gay-rights-debates" and "1-5811_33_29__35_38_40_41_43_2"  in row["key"+str(count)]:
                            continue 
                        if found:
                            Allrowdict=dict()
                            Allrowdict["Key"]=row["key"+str(count)]
                            Dialog_text_tags=row["Dialogtext"+str(count)]
                            soup = BeautifulSoup(Dialog_text_tags)
                            Allrowdict["Dialog"]=soup.get_text()
                            textfile=InputdirSummary + row["key"+str(count)] +".txt"
                            lines=FileHandling.ReadTextFile(textfile)
                            textlines=" ".join(lines)
                            
                            print textfile
                            textlines=NewFormat_text.ascii_only(textlines)
                            print type(textlines)
                            Allrowdict["Summaries"]=textlines
                            Allrows.append(Allrowdict)
                        else:
                            print row["key"+ str(count)] +" not in keys"
                            
                                
                        
                    
            
            
        
    

if __name__ == '__main__':
    topic="gay-rights-debates"
    TotalTasks=2
    allrows=list()
    fieldnames=["Key","Dialog","Summaries"]
    outfile=os.getcwd() +"/CSV/"+ topic +"/MTdata/LabelUpdated/AllMTSummary"
    AllPyramid=os.getcwd() +"/CSV/"+ topic +"/MTdata/LabelUpdated/Allpyramids_v1_labels_updated"
    for task in range(2,TotalTasks+2):
        if task == 2 :
            InputdirDialog=os.getcwd()+"/CSV/"+ topic+"/MTdata/MT"+ str(task)+"/"
            Inputfile="MT2_more750" # inputcsv  file to read the dialogs,/gay-rights-debates/MTdata/MT2/MT2_more750.csv
            noofitems=5             # no of items in one hit
            InputdirSummary=os.getcwd()+"/CSV/"+ topic+"/MTdata/MT"+ str(task)+"/MT2Summaries/MT2_more750/combined_Summary/"
            combineMTVBatch(InputdirDialog,InputdirSummary,Inputfile,allrows,noofitems,task,AllPyramid)
            
            Inputfile="MT2_midrange"  #input csv file to read the dialogs
            InputdirSummary=os.getcwd()+"/CSV/"+ topic+"/MTdata/MT"+ str(task)+"/MT2Summaries/MT2_midrange/"
            combineMTVBatch(InputdirDialog,InputdirSummary,Inputfile,allrows,noofitems,task,AllPyramid)
        if task==3:
            noofitems=5
            InputdirDialog=os.getcwd()+"/CSV/"+ topic+"/MTdata/MT"+ str(task)+"/"
            InputdirSummary=os.getcwd()+"/CSV/"+ topic+"/MTdata/MT"+ str(task)+"/MT3Summaries/MT3_midRange_Summary/"
            Inputfile="MT3_midrange"  #input csv file to read the dialogs
            combineMTVBatch(InputdirDialog,InputdirSummary,Inputfile,allrows,noofitems,task,AllPyramid)
            #------------------------------------------------------- noofitems=3
            #--- Inputdir=os.getcwd()+"/CSV/"+ topic+"/MTdata/MT"+ str(task)+"/"
            #------------------------------------------- Inputfile="MT3_more750"
            # combineMTVBatch(Inputdir,Inputfile,allrows,noofitems,task,AllPyramid)
    shuffle(allrows) 
    shuffle(allrows)        
    FileHandling.write_csv(outfile, allrows, fieldnames)           