'''
Created on Sep 21, 2014
This program takes the input as strings from Parser package file 
/Parser_Pkg/Parserdata/" +topic+ "/StringInput/StringsDir/"
and  parses using ims to extract the probabilities for each sense.
@author: amita
'''
import nltk
from bs4 import BeautifulSoup
import os
import sys
from operator import itemgetter
from collections import OrderedDict
import subprocess
from data_pkg import FileHandling


    


class ParseWSDResults:
    def __init__(self,InputDir,OutputDir,WSDPath):
        self.InputDir=InputDir
        self.OutputDir=OutputDir
        self.WSDPath=WSDPath
     
    #----- Call IMS for WSD , input in FileWithPath and write results to outfile
    def GenerateWSDResultsFile(self,FileWithPath,KeyDirs):
        #TextLines=FileHandling.ReadTextFile(FileWithPath)
        #TextString=" ".join(TextLines)
        WSD_Lines=list()
        outdir=self.OutputDir + KeyDirs
        if not os.path.exists(outdir):
                os.mkdir(outdir)
        outfile=outdir + "/"+os.path.basename(FileWithPath)
        cmd=str(self.WSDPath +" "+ FileWithPath+" "+ outfile[:-3]+".xml" +" " +"/Users/amita/software/IMS/ims/lib/dict/index.sense 0 0 0 0")  
        proc=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        output, errors=proc.communicate()
        WSD_Lines.append(output)  


#==========================================================================
# Input is a dir of dir from parser package, reads strings file 
# and call function GenerateWSDResultsFile with individual file containing the string to perform WSD
#==========================================================================
    def GenerateWSDResultsDir(self,DirPath):
        ListDir=os.listdir(DirPath)
        for KeyDirs in ListDir: 
            SentFileList=os.listdir(DirPath+KeyDirs)
            for filename in SentFileList:
                FileWithPath=DirPath+ KeyDirs+"/"+filename
                if str(FileWithPath).startswith("."):
                            continue
                self.GenerateWSDResultsFile(FileWithPath, KeyDirs)    
              
    
    #===========================================================================
    # Read a list of files containing WSD in xml format, parse it to get sense keys with 
    # probilities for each  word in the input file   
    #===========================================================================
    def Generate_sorted_list_SenseKeysDir(self): 
        
        ListDir=os.listdir(self.OutputDir)
        rowdicts=list()
        for KeyDirs in ListDir: 
            if str(KeyDirs).startswith("."):
                            continue
            SentFileList=os.listdir(self.OutputDir+KeyDirs)
            for filename in SentFileList:
                FileWithPath=self.OutputDir+ KeyDirs+"/"+filename
                if str(FileWithPath).startswith("."):
                            continue
                sorted_list_SenseKeys=self.Generate_sorted_list_SenseKeysFile(FileWithPath)
                row=dict()
                row["key"]=FileWithPath
                row["list_SenseKeys"]=sorted_list_SenseKeys
                rowdicts.append(row)   
        return rowdicts    
            
           
    def Generate_sorted_list_SenseKeysFile(self, FullPath):
        
        soup=BeautifulSoup(open(FullPath)) 
        soup.prettify()
        probs_key_list=list() 
        listx= soup.find_all("x") 
        for word in listx:
            dictprob =dict()   
            first=True
            Prob_sense_keys= str(word.attrs['length']).split()
            for probs_key_pair in Prob_sense_keys:
                
                if first:
                    first=False
                    if not probs_key_pair == "1" :
                        print " first argument not 1 in sense id keys for " + probs_key_pair + " in  file "  +FullPath
                        sys.exit(0)
                else: 
                    
                    prob_key_list = probs_key_pair.split("|")
                    print prob_key_list
                    dictprob[prob_key_list[0]]=prob_key_list[1]
                    
                    
            sorted_probs_key=OrderedDict(sorted( dictprob.items(), key=lambda t: t[1],reverse=True)) 
            probs_key_list.append(sorted_probs_key)
                
                     
        return    probs_key_list         
                    
               
def Execute(ParseWSDResultsObj):
    #ParseWSDResultsObj.GenerateWSDResultsDir(ParseWSDResultsObj.InputDir)
    ParseWSDResultsObj.Generate_sorted_list_SenseKeysDir()

if __name__ == '__main__':
    topic="gay-rights-debates"
    InputDir=os.path.dirname(os.getcwd()) +  "/Parser_Pkg/Parserdata/" +topic+ "/StringInput/StringsDir/"
    OutputDir=os.getcwd()+"/WSD_data/"+topic+ "/StringInput/XMLStrings/" 
    WSDPath="""/Users/amita/software/IMS/ims/testPlain.bash /Users/amita/software/IMS/ims/models """ 
    ParseWSDResultsObj=ParseWSDResults(InputDir,OutputDir,WSDPath)
    Execute(ParseWSDResultsObj)    
    
    