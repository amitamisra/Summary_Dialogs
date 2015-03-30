#!/usr/bin/env python
# -*- coding: utf-8 -*-
#===============================================================================
# This file  creates a summary text file compiling summaries from different files and adding the 
# regular expression for pyramid
#===============================================================================

import os
from collections import defaultdict
import FileHandling
import NewFormat_text
#from ftfy import fix_text
import unicodedata
'''
Created on May 29, 2014

@author: amita
'''
class summary:
    def __init__(self,inputdir):
        self.inputdir= inputdir
        self.filelist_summary=defaultdict(list)
        self.filelist_user_tuple=[]
        
    
    #------------------------- parsed the filename based on key_userid construct
    def parsefilenames(self):
        filelist=os.listdir(self.inputdir)
        for filename in filelist:
            if not filename.startswith('.'):
                if os.path.isfile(os.path.join(self.inputdir, filename)):
                    index= filename.index("user")
                    self.filelist_user_tuple.append((filename[:index-1],filename))
    def createsummarylist(self):
        result= defaultdict(list)
        for k,v in self.filelist_user_tuple:
            result[k].append(v)
        self.filelist_summary= result
    
    #===========================================================================
    # write the summary files in the folder newsummary_taskno    
    #===========================================================================
    def writefoldersummary(self,combinedir):
        Textlines=[]
        count=0 
        for key,values in self.filelist_summary.items():
            filenames=values
            for filename in filenames: 
                inputfile= self.inputdir+ filename
                Text=FileHandling.ReadTextFile(inputfile)
                new_text=" ".join(Text)
                #new_text=new_text.decode('utf-8', 'ignore')
                #print type(new_text)
                print inputfile
                new_text=(NewFormat_text.ascii_only(new_text))   
                print type(new_text)
                Textlines.append("\n"+ str(RegularExp[count])) 
                Textlines.append("\n"+ new_text+"\n")
                count= count+1
             
            
            if not os.path.exists(combinedir):
                os.makedirs(combinedir)
            Filename=combinedir+key
            FileHandling.WriteTextFile(Filename, Textlines)
            Textlines=[] 
            count=0     
                  
TaskNo=1        
Noofsummaries=5 
topic="gay-rights-debates"           
Inpdirectory=os.getcwd()+ "/CSV/"+ topic +"/MTdata/MT2/MT2Summaries/MT2_more750/TextFiles/TextFiles_"+str(TaskNo)+"/"
combinedir=os.getcwd()+ "/CSV/"+ topic +"/MTdata/MT2/MT2Summaries/MT2_more750/combined_Summary/"
RegularExp=["----------\nD"+ str(i) +"\n"+ "----------" for i in range(Noofsummaries)]    

summaryobj = summary(Inpdirectory)  
summaryobj.parsefilenames()
summaryobj.createsummarylist()
summaryobj.writefoldersummary(combinedir)  
               
if __name__ == '__main__':
    pass
