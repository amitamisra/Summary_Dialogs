#!/usr/bin/env python
'''
Created on Sep 16, 2014

@author: amita
'''
import os
from data_pkg import FileHandling
import subprocess
class RST_Parser:
    def __init__(self,inputSingaporeRelations,InputRSTDir,OutputRSTDir,TypeInputParser,ParserPath):
        self.inputSingaporeRelations=inputSingaporeRelations # take inout as singapore csv relations for easier mapping
        self.OutputRSTDir= OutputRSTDir
        self.InputRSTDir=InputRSTDir
        self.TypeInputParser=TypeInputParser
        self.ParserPath=ParserPath
    
        
    def CreateTextDirforRSTInput(self):
        rowdicts=FileHandling.read_csv(self.inputSingaporeRelations)
        count=0
        for row in rowdicts:
            Lines=list()
            if self.TypeInputParser =="Strings":
                Sent=row["Sent"] + "<s>"  # <s> required by RST parser
            Sent_No=count
            count=count+1
            Lines.append(Sent)
            outfile=self.InputRSTDir+"/sent_"+ str(count)
            FileHandling.WriteTextFile(outfile, Lines)
    def RunRST(self):
        FileList=os.listdir(self.InputRSTDir)
        for filename in FileList:
            FileWithPath=self.InputRSTDir+filename
            if str(filename).startswith("."):
                continue
            cmd=str(self.ParserPath +" "+ FileWithPath )  
            proc=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            output, errors=proc.communicate()
            print errors
            
            
    def CheckRST(self):
        
            cmd=str(self.ParserPath + " "+ "/Users/amita/software/gCRF_dist/texts/wsj_0607.txt")  
            proc=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            output, errors=proc.communicate()
            print errors         
          
def Execute(RST_Parserobj):
    #RST_Parserobj.CreateTextDirforRSTInput()   
    RST_Parserobj.CheckRST()    
if __name__ == '__main__':
    
    topic="gay-rights-debates"
    parserlocation="/Users/amita/software/gCRF_dist/src/parse.py"
    
    TypeInputParser="Strings"
    if  TypeInputParser=="Strings":
        InpFileLocation=os.getcwd()+"/Parserdata/" +topic+ "/StringInput/ParsedRelations"
        InpRSTDir=os.getcwd()+"/Parserdata/" +topic+ "/StringInput/RST_Dir/RSTStrings/"
        RelationFile=os.getcwd()+"/Parserdata/" +topic+ "/StringInput/RST_Dir/ParsedRelations" 
        
            # InpFileLocation=os.getcwd()+"/Parserdata/" +topic+ "/StringInput/ParsedRelations"
            # InpRSTDir=os.getcwd()+"/Parserdata/" +topic+ "/StringInput/RST_Dir/RSTStrings/"
            # RelationFile=os.getcwd()+"/Parserdata/" +topic+ "/StringInput/RST_Dir/ParsedRelations" # Allrelations in all strings as textfile
            
    RST_Parserobj=RST_Parser(InpFileLocation,InpRSTDir,RelationFile,TypeInputParser,parserlocation)
    Execute(RST_Parserobj)