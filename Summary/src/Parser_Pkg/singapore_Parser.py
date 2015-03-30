#encoding: utf-8
'''
Created on Sep 14, 2014
this program takes input as input strings/summaries/dialogs from csv files , creates a corresponding file for the singapore parser
.singapore parser reads these files, writes to the output files and creates a corresponding json file for all the strings/summaries/dialogs 
@author: amita
'''
import os
from data_pkg import FileHandling
import subprocess
import sys
class SingaporeParser:
    def __init__(self,Inputfile, InputType,ParserPath,dictfield,TextDir,RelationFile,fieldnames):
        self.Inputfile=Inputfile
        self.Inputtype=InputType
        self.ParserPath=ParserPath
        self.dictfield=dictfield
        self.TextDir=TextDir
        self.RelationFile=RelationFile
        self.fieldnames=fieldnames
    
    
    #===========================================================================
    # This function takes an input as strings from paraphrase/para_data/gay-rights-debates/cluster/Summaries/InputStrings.csv 
    # and writes each string to a file for singapore parser
    #===========================================================================
    def write_strings_File(self):
        count=dict()
        RowStrings=FileHandling.read_csv(self.Inputfile)
        KeyList=list()
        counter=0
        for row in RowStrings:
            Lines=list()
            InputKey=row[self.dictfield["keyfile"]]
            #===================================================================
            # if InputKey == "1-1281_12_11__15_21_23_25_26_28_6":
            #     counter=counter+1
            #     print counter
            #===================================================================
            RowString=row[self.dictfield["stringkey"]]
            if not os.path.exists(self.TextDir):
                os.mkdir(self.TextDir)
            if not os.path.exists(self.TextDir+InputKey):
                os.mkdir(self.TextDir+InputKey)
            
            if not self.TextDir+InputKey in KeyList:
                KeyList.append(self.TextDir+InputKey)
                count[self.TextDir+InputKey]=1
            OutStringFileParser = self.TextDir +InputKey+"/"+"sent_" +str(count[self.TextDir+InputKey])
            Lines.append(RowString)
            FileHandling.WriteTextFile(OutStringFileParser, Lines)
            count[self.TextDir+InputKey]=count[self.TextDir+InputKey]+1
            
            
    
    
    def write_dicourse_stringsFile(self):
        try: 
            AllRows=list()  
            Relation_Lines=list()    
            ListDir=os.listdir(self.TextDir)
            for KeyDirs in ListDir: 
                if str(KeyDirs).startswith("."):
                    continue
                SentFileList=os.listdir(self.TextDir+KeyDirs)
                sent_count=1
                for filename in SentFileList:
                    if str(filename).startswith("."):
                        continue
                    FileWithPath=self.TextDir+ KeyDirs+"/"+filename
                    TextLines=FileHandling.ReadTextFile(FileWithPath)
                    print FileWithPath
                    TextString=" ".join(TextLines)
                    Rowdict=dict()
                    cmd=str(self.ParserPath +" "+ FileWithPath )  
                    #subprocess.call(cmd, shell=True) 
                    #output=subprocess.check_output(cmd,shell=True) 
                    proc=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
                    output, errors=proc.communicate()
                    Rowdict["key"]  = KeyDirs
                    Rowdict["Sent"]  = TextString
                    Rowdict["Parsed_String"]  = output
                    Rowdict["Sent_No"]=sent_count
                    sent_count=sent_count+1;
                    AllRows.append(Rowdict)
                    Relation_Lines.append(output)
                    
            FileHandling.WriteTextFile(self.RelationFile,Relation_Lines)  
            FileHandling.write_csv(self.RelationFile, AllRows, self.fieldnames)                                                                       
        except Exception as e :
            print " Exception " + str(e)  +"in File SingaporeParser in function write_dicourse_stringsFile"  
            sys.exit()  #proc=subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)                              
                #for line in proc.stdout:
                #    print line
                #subprocess.call([self.ParserPath,OutFileDes], shell=True)
                #output, errors = p.communicate()  
                #OutFileDes.close()
                
        
def Execute(SingaporeParserObj):
    SingaporeParserObj.write_strings_File()
    SingaporeParserObj.write_dicourse_stringsFile()
                

if __name__ == '__main__':
    topic="gay-rights-debates"
    parserlocation="/Users/amita/software/singapore_pdtb-parser-master/src/parse.rb"
    
    TypeInputParser="Strings"
    
    
    if    TypeInputParser=="Strings":
            InpFileLocation=os.path.dirname(os.getcwd())+"/paraphrase/para_data/"+ topic+"/cluster/Summaries/InputStrings"
            RelationFile=os.getcwd()+"/Parserdata/" +topic+ "/Summaries/ParsedRelations" # Allrelations in all strings as textfile
            fieldnames=sorted(["key","Sent","Parsed_String","Sent_No"])
            TextDir=os.getcwd()+ "/Parserdata/" +topic+ "/Summaries/StringsDir/"  # contains each string as a file for parser input
            dictfield=dict()
            dictfield["stringkey"]="Sent"
            dictfield["keyfile"]="key"
            dictfield["textallsummary"]="text"
            
    
    
    
    SingaporeParserObj=SingaporeParser(InpFileLocation,TypeInputParser,parserlocation,dictfield,TextDir,RelationFile,fieldnames)
    Execute(SingaporeParserObj)
            
    
    
    
    
    
    