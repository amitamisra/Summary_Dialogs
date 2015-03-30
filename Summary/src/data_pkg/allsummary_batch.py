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

def allSummary(inputBatchfile,dirout): 
    dict_key=defaultdict(str)
    counter_key=defaultdict(int)
    rowdicts=FileHandling.read_csv(inputBatchfile)
    rowdicts.sort(key=operator.itemgetter("HITId"))
    for key, items in itertools.groupby(rowdicts, operator.itemgetter('HITId')):
        Hitids=list(items)
        for row in Hitids:
            
            if row["AssignmentStatus"]=="Approved":
                for count in range(1,noofitems_inhit+1):
                    key=row["Input.key"+str(count)]
                    Answer=row["Answer.Dialog"+str(count)+"_Summary"]
                    new_text=(NewFormat_text.ascii_only(Answer)) 
                    print type(new_text)
                    dict_key[key]=dict_key[key]+"\n"+ str(RegularExp[counter_key[key]]) + "\n" + new_text +"\n\n"
                    counter_key[key]=counter_key[key]+1
                    
    
    for key in dict_key.keys():
        
        Outfile=dirout + key
        Lines=list()
        Lines.append(dict_key[key])
        FileHandling.WriteTextFile(Outfile, Lines)

if __name__ == '__main__':
    #was done for Gay rights
    #--------------------------------------- TaskNo=3      # Mechanical Hit task
    #----------------------------------------------------------- Noofsummaries=5
    #---------------------------- topic="gay-rights-debates"  #used only for MT3
    #--------------------------------------------------------- noofitems_inhit=3
    
    
    
    
    TaskNo=1      # Mechanical Hit task
    Noofsummaries=5
    topic="gun-control"  
    noofitems_inhit=3
    
    directoryin=os.getcwd()+ "/CSV/"+ topic +"/MTdata/MT"+ str(TaskNo)+"/"+"MT"+ str(TaskNo)+"Results/MT"+str(TaskNo)+"_midRange_Results/"
    batchinfile=directoryin+"MT"+ str(TaskNo)+"_midRange_Results"
    dirout=os.getcwd()+ "/CSV/"+ topic+ "/MTdata/MT"+ str(TaskNo)+"/"+"MT"+str(TaskNo)+"Summaries/MT"+str(TaskNo)+"_midRange_Summary/"       
    
    
    
    
    
    
    if not os.path.exists(dirout):
        os.makedirs( dirout)
    RegularExp=["----------\nD"+ str(i) +"\n"+ "----------" for i in range(Noofsummaries)]  
    allSummary(batchinfile,dirout)
    pass