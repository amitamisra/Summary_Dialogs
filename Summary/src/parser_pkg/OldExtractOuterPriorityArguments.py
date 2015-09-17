'''
Created on Sep 15, 2014
This file reads the arguments written by Singapore Parser_Pkg from file parser/Parserdata/" +topic+ "/StringInput/StringsDir/Relations" 
@author: amita.This looks for outermost arguments not embedded inside any argtags.and extracts that as a single argument.
'''
import re
import os
from data_pkg import FileHandling
import sys
import operator
class ExtractArguments:
    def __init__(self,InputFile,OutputFile):
        self.InputFile=InputFile
        self.OutputFile=OutputFile
    
    #===========================================================================
    # This function takes a string with Exp tags from parser output and removes all {Exp_conn_Arg_i 
    # and corresponding closing tags Exp_conn_Arg_i  tags within the string
    #===========================================================================
    def  RemoveAllExptags(self,String) :
        #Open_Brk_Exp=re.findall(r'{Exp_\d+_Arg\d+',"",String)
        StringNoopen=re.sub(r'{Exp_\d+_Arg\d+',"",String)
        StringNotags=re.sub(r'Exp_\d+_Arg\d+}',"",StringNoopen)
        return StringNotags
    
    
    
#  This function removes tags of attr and Connective and their content depending on the valiue of RemString from String
    def RemoveAttr(self,String,RemString):
        if RemString=="Attr":
            regex = re.compile('{%s_\d'%RemString)
        else:
            if RemString=="conn":
                regex=re.compile('{Exp_\d_%s'%RemString)
        
        
        Open_Brk_Attr=regex.findall(String)
        for Attr in Open_Brk_Attr:
            #Attr=m.string[m.start():m.end()]
            
            startindex=String.find(Attr)
            EndAttr=Attr[1:] +"}"
            closeAttrindex=String.find(EndAttr)
            lenAttr=len(EndAttr)
            EndIndex=closeAttrindex+lenAttr
            AttrString=String[startindex:EndIndex]
            OpenExpTags=self.FindAllExpopenTags(AttrString)
            CloseExpTags=self.FindAllExpcloseTags(AttrString)
            NewString=String[:startindex]+String[EndIndex:]
            String=NewString
            
            
        return String
    
    def FindAllExpopenTags(self, String):
        Open_Brk_Exp_Iter=re.finditer(r'{Exp_\d+_Arg\d+',String)
        Open_Exp_List=[]
        for m in Open_Brk_Exp_Iter:
            Exp_Index=dict()
            Exp_Index["Open_Exp"]=m.string[m.start():m.end()]
            Exp_Index["Open_Exp_Index"]=m.start()
            Exp_Index["Tag_Begin_Index"]=m.start()
            Open_Exp_List.append(Exp_Index)
         
        Open_Exp_List.sort(key=operator.itemgetter('Open_Exp_Index'))
        return (Open_Exp_List)
    
        
    def FindAllExpcloseTags(self, String):
        Close_Brk_Exp_Iter=re.finditer(r'Exp_\d+_Arg\d+}',String)
        Close_Exp_List=[]
        for m in Close_Brk_Exp_Iter:
            Exp_Index=dict()
            Exp_Index["close_Exp"]=m.string[m.start():m.end()]
            Exp_Index["close_Exp_Index"]=m.start()
            Exp_Index["Tag_Begin_Index"]=m.start()
            Close_Exp_List.append(Exp_Index)
         
        Close_Exp_List.sort(key=operator.itemgetter('Open_Exp_Index'))
        return (Close_Exp_List)    
    
    
    
    
    
    #===========================================================================
    # This function takes two inputs , one is from singapore parser output string with EXP tags 
    # and other is a list containing all Exp_conn_Arg_i opening tags. Takes the first index of  an opening tag
    # from the import list deletes that tag and corresponding closing tag from the string and then calls function
    #  RemoveAllExptags which removes all nested tags within this EXP tag.
    # It repeats till the list of tags is empty      
    #===========================================================================
    
    def Removetags(self,RowStringwithArgs,ListOpenExp):
        AllStrings=list()
        NewString=RowStringwithArgs
        NewList=ListOpenExp
        if NewList:
            while NewList:
                len_Newstring=len(NewString)
                First_BrkArg=NewList[0]["Open_Exp"]
                First_BrkIndexArg=NewString.find(First_BrkArg)
                Len_BrkIndexArg= len(First_BrkArg)
                StartingPoint= First_BrkIndexArg+Len_BrkIndexArg
                conn_ind=First_BrkArg.index("{Exp_")+5 # no of chars in EXP_
                conn_no=First_BrkArg[conn_ind]
                Argno_ind=First_BrkArg.index("Arg")+3 # no of chars in Arg
                Argno=First_BrkArg[Argno_ind]
                closingExp="Exp_"+str(conn_no)+"_Arg"+str(Argno)+"}"
                closingExp_First=NewString.index(closingExp)
                closingExp_len=len(closingExp)
                start_Newstring=closingExp_First+closingExp_len
                Reduced_String=NewString[: closingExp_First]
                Reduced_String=self.RemoveAllExptags(Reduced_String)
                Reduced_String=self.RemoveAttr(Reduced_String,"Attr")
                Reduced_String=self.RemoveAttr(Reduced_String,"conn")
                AllStrings.append(Reduced_String)
                
                NewString=NewString[start_Newstring:len_Newstring]
                NewList=self.FindAllExpopenTags(NewString)
        else:
            Reduced_String=self.RemoveAttr(NewString,"Attr")
            Reduced_String=self.RemoveAttr(Reduced_String,"conn")
            AllStrings.append(Reduced_String)      
            
        return AllStrings    
def Execute(ExtractArgumentsobj):
    AllRows= FileHandling.read_csv(ExtractArgumentsobj.InputFile)
    AllArgRows=list()
    AllArgRowsText=list()
    sent_no=0
    for Row in AllRows:
        ParsedString=Row["Parsed_string"]
        AllExpopentags=ExtractArgumentsobj.FindAllExpopenTags(ParsedString)
        AllArgs=ExtractArgumentsobj.Removetags(ParsedString,AllExpopentags)
        NoofArg=len(AllArgs)
        count=0
        sent_no=sent_no+1
        AllArgRowsText.append("\n\n\n Original Text:\n"+ str(sent_no)+":  "+ Row["Sent"])
        AllArgRowsText.append("\nParsed Text:\n"+Row["Parsed_string"])
        AllArgRowsText.append("\nArguments without connective and Attributions\n")
        for singleArg in AllArgs:
            count=count+1
            ArgRow=dict()
            AllArgRowsText.append("\n NEW ARGUMENT:" +singleArg )
            ArgRow["Args"]=singleArg
            ArgRow["Parsed_string"]=Row["Parsed_string"]
            ArgRow["Sent"]=Row["Sent"]
            ArgRow["key"]=Row["key"]
            ArgRow["CountArg"]=NoofArg
            ArgRow["ArgNo"]=count
            ArgRow["sent_No"]=sent_no
            AllArgRows.append(ArgRow)
    fieldnames=ArgRow.keys()        
    FileHandling.WriteTextFile(ExtractArgumentsobj.OutputFile, AllArgRowsText)
    FileHandling.writejson(AllArgRows, ExtractArgumentsobj.OutputFile)  
    FileHandling.write_csv(ExtractArgumentsobj.OutputFile, AllArgRows, fieldnames) 
        
        
if __name__ == '__main__':
    topic="gay-rights-debates"
    InputFile=os.getcwd()+"/Parserdata/" +topic+ "/StringInput/ParsedRelations"
    OutputFile=os.getcwd()+"/Parserdata/" +topic+ "/StringInput/ParsedArguments"
    ExtractArgumentsobj=ExtractArguments(InputFile,OutputFile)
    Execute(ExtractArgumentsobj)
   
    
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 #==============================================================================
 # Open_Exp_List=list()
 #        Close_Exp_List=list()
 #        Open_Brk_Exp_Iter=re.finditer(r'{Exp_\d+_Arg\d+',String)
 #        Close_Brk_Exp_Iter=re.finditer(r'Exp_\d+_Arg\d+}',String)
 #        for m in Open_Brk_Exp_Iter:
 #            Exp_Index=dict()
 #            Exp_Index["Open_Exp"]=m.string[m.start():m.end()]
 #            Exp_Index["Open_Exp_Index"]=m.start
 #            Open_Exp_List.append(Exp_Index)
 #        for m in Close_Brk_Exp_Iter:
 #            Exp_Index=dict()
 #            Exp_Index["Close_Exp"]=m.string[m.start():m.end()]
 #            Exp_Index["Close_Exp_Index"]=m.start
 #            Close_Exp_List.append(Exp_Index)
 #            
 #            
 #        Open_Exp_List.sort(key=operator.itemgetter('Open_Exp_Index'))
 #        Close_Exp_List.sort(key=operator.itemgetter('name'))    
 #        return (Open_Exp_List,Close_Exp_List)  
 
 #ParsedString=""" {Attr_0 {Exp_0_Arg2 {Exp_0_Arg1 S1 {Exp_0_conn_Asynchronous then Exp_0_conn} states Attr_0} that {Exp_1_Arg1 in many anglo countries , it is not for a heterosexual contract , Exp_1_Arg1} {Exp_1_conn_Conjunction and Exp_1_conn} {Exp_1_Arg2 in marriage with couples who can not have children , it 's not for a family unit either Exp_1_Arg2} . Exp_0_Arg1} Exp_0_Arg2} """
    #ParsedString=""" {Exp_0_Arg1 S1 responds angrily and with homosexual slurs , Exp_0_Arg1} {Exp_0_conn_Conjunction and Exp_0_conn} {Exp_0_Arg2 requests that S2 take his comments up with Obama . Exp_0_Arg2}"""
    #ParsedString="""{Exp_0_Arg2 {Exp_0_Arg1 This person {Exp_0_conn_Conjunction also Exp_0_conn} uses the parallel of treatment of blacks and women , {Attr_0 but argues Attr_0} that morality was an excuse to hide the prejudice . Exp_0_Arg1} Exp_0_Arg2}"""
    #ParsedString="""{Exp_0_Arg1 S1 believes it is completely unfair that gay marriage be dismissed or disliked Exp_0_Arg1} {Exp_0_conn_Conjunction and Exp_0_conn} {Attr_0 {Exp_0_Arg2 S2 argues Attr_0} that no matter what S1 believes is right or wrong , the majority of people control what is normal in our society . Exp_0_Arg2}"""
 
 #==============================================================================