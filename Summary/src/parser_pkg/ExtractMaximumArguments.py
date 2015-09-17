'''
Created on Sep 30, 2014
This program reads arguments from Parsedrelations and extracts all arguments from them, iteratively find non overlapping arg tags and remove them
@author: amita
'''
from data_pkg import FileHandling
from operator import itemgetter
import re
import copy
import itertools
import collections
import os
from collections import defaultdict
from nltk  import word_tokenize

# checklist  global variables
def check_element(checkpair):
        for pair in checklist:
            if  checkpair != pair and (pair["Open_Exp_Index"] in range(checkpair["Open_Exp_Index"],checkpair["Close_Exp_Index"]) or pair["Close_Exp_Index"] in range(checkpair["Open_Exp_Index"],checkpair["Close_Exp_Index"]) ):
                return bool
class ExtractMaxArguments:
    
    def __init__(self,InputFile,OutputFile):
        self.InputFile=InputFile
        self.OutputFile=OutputFile
        self.OldcheckList=[]
        self.Newchecklist=[]
        self.compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
    
    #===========================================================================
    # This function takes a string with Exp tags from parser output and removes all {Exp_d_Arg_i 
    # and corresponding closing tags Exp_dArg_i}  tags within the string
    #===========================================================================
    def  RemoveExptags_String(self,String) :
        #Open_Brk_Exp=re.findall(r'{Exp_\d+_Arg\d+',"",String)
        StringNoopen=re.sub(r'{Exp_\d+_Arg\d+',"",String)
        StringNotags=re.sub(r'Exp_\d+_Arg\d+}',"",StringNoopen)
        return StringNotags
    
    
    
    
    # Remove any remining Exp tags from the args list
    def RemoveExptags_List(self,AllArgs): 
        Removetagarg=list()
        for arg in AllArgs:
            Newarg=self.RemoveExptags_String(arg)
            Removetagarg.append(Newarg)
        return Removetagarg
    
    
    
    
    #===========================================================================
    # This function takes a string with Attrtags and finds if it contains any 
    # {Exp_d_Arg_i tags and finds all {Exp_d_Arg_i 
    # and corresponding closing tags Exp_dArg_i}  and returns them in order based on tag begin index
    #===========================================================================
    def Addopenclosetags(self,AttrString,OpenExpTags,CloseExpTags):
        ExpTags=OpenExpTags+CloseExpTags
        newlist = sorted(ExpTags, key=itemgetter('Tag_Begin_Index')) 
        AddTags=" "
        for exp in newlist:
            AddTags=AddTags+" "+ exp["tag"]
        return AddTags    
        
    
    #===========================================================================
    # This function takes a string with Exp tags from parser output and removes all {Exp_conn_i 
    # and corresponding closing tags Exp_conn_i}  tags within the string
    #===========================================================================
    def Removeconn(self,String,RemString):
        regex=re.compile('{Exp_\d_%s'%RemString)
        Open_Brk_Attr=regex.findall(String)
        for Attr in Open_Brk_Attr:
            #Attr=m.string[m.start():m.end()]
            
            startindex=String.find(Attr)
            EndAttr=Attr[1:] +"}"
            closeAttrindex=String.find(EndAttr)
            lenAttr=len(EndAttr)
            EndIndex=closeAttrindex+lenAttr
            NewString=String[:startindex]+String[EndIndex:]
            String=NewString
            
            
        return String    
    
#  This function removes tags of attr and  and their content,Also calls Addopenclosetags to add if any 
#{Exp_d_Arg_i tags and corresponding closing tags Exp_dArg_i present within attr}  
    def RemoveAttr(self,String,RemString):
        regex = re.compile('{%s_\d'%RemString)
        Open_Brk_Attr=regex.findall(String)
        if Open_Brk_Attr:
            find=True
        else:
            find=False    
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
            Exp_Tags=self.Addopenclosetags(AttrString,OpenExpTags,CloseExpTags)
            NewString=String[:startindex]+Exp_Tags+String[EndIndex:]
            String=NewString
            
            
            
        return (String,find)
    
    
    # This function takes a string with Exp tags from parser output and removes all {Exp_d_Arg_i
    #-------- and corresponding closing tags Exp_dArg_i}  tags within the string
    def FindAllExpopen_closeTags(self, String):
        Open_Brk_Exp_Iter=re.finditer(r'{Exp_\d+_Arg\d+',String)
        Open_Exp_List=[]
        for m in Open_Brk_Exp_Iter:
            Exp_Index=dict()
            Open_Exp=m.string[m.start():m.end()]
            Exp_Index["Open_Exp"]=Open_Exp
            length_Open_Exp= len(Exp_Index["Open_Exp"])
            close_exp=Open_Exp[1:length_Open_Exp] +"}"
            len_close_exp=len(close_exp)
            close_exp_ind=str(String).find(close_exp)+len_close_exp-1
            Exp_Index["Close_Exp_Index"]=close_exp_ind
            Exp_Index["Open_Exp_Index"]=m.start()
            Exp_Index["Close_Exp"]=close_exp
            Open_Exp_List.append(Exp_Index)
        
        
        if Open_Exp_List:
            findexp=True
        else:
            findexp=False 
        Open_Exp_List.sort(key=itemgetter('Open_Exp_Index'))
        return (Open_Exp_List,findexp)
    
    
# This function takes a string with Exp tags from parser output and finds all {Exp_d_Arg_i
    def FindAllExpopenTags(self, String):
        Open_Brk_Exp_Iter=re.finditer(r'{Exp_\d+_Arg\d+',String)
        Open_Exp_List=[]
        for m in Open_Brk_Exp_Iter:
            Exp_Index=defaultdict(lambda:-1)
            #===================================================================
            # Exp_Index["Open_Exp"]=m.string[m.start():m.end()]
            # Exp_Index["Open_Exp_Index"]=m.start()
            #===================================================================
            Exp_Index["Tag_Begin_Index"]=m.start()
            Exp_Index["tag"]=m.string[m.start():m.end()]
            Open_Exp_List.append(Exp_Index)
         
        Open_Exp_List.sort(key=itemgetter('Tag_Begin_Index'))
        return (Open_Exp_List)
    
    #This function takes a string with Exp tags from parser output and finds all Exp_d_Arg_i }   
    def FindAllExpcloseTags(self, String):
        Close_Brk_Exp_Iter=re.finditer(r'Exp_\d+_Arg\d+}',String)
        Close_Exp_List=[]
        for m in Close_Brk_Exp_Iter:
            Exp_Index=defaultdict(lambda:-1)
            #===================================================================
            # Exp_Index["close_Exp"]=m.string[m.start():m.end()]
            # Exp_Index["close_Exp_Index"]=m.start()
            #===================================================================
            Exp_Index["Tag_Begin_Index"]=m.start()
            Exp_Index["tag"]=m.string[m.start():m.end()]
            Close_Exp_List.append(Exp_Index)
         
        Close_Exp_List.sort(key=itemgetter('Tag_Begin_Index'))
        return (Close_Exp_List)     
    
# extract Individual arguments( do not cross) in Non_crossing_pairs and the remaining string in RemString
    def getexpargs(self,ParsedString,Allargs):
        RemString=ParsedString
        Non_crossing_pairs=list()
        global checklist
        while True:
            filtered = itertools.ifilter(check_element,checklist) #returns generator
            Newchecklist = list(filtered) 
            if len(Newchecklist)==len(checklist ): 
                leftpairs=checklist
                break
            else:
                diff=[x for x in checklist if x not in Newchecklist]
                for pair in diff:
                    lenLeftstring=len(RemString)
                    begin=pair["Open_Exp"]
                    close=pair["Close_Exp"]
                    len_exp=len(close)
                    begin_ind=str(RemString).find(begin)
                    end_index=RemString.find(close) + len_exp
                    RemString=RemString[0:begin_ind] + RemString[end_index:lenLeftstring]
                    
                Non_crossing_pairs.extend(diff)
                checklist=copy.deepcopy(Newchecklist) 
        return  (Non_crossing_pairs,leftpairs,RemString)       
            # copychecklist=copy.deepcopy(Newchecklist)                           #exahust iterator to create list
            #----------- _filtered = itertools.ifilter(check_element, checklist)
            #--------------------------------------- checklist = list(_filtered)
    def getargsText(self,AllExpopentags,ParsedString):
        Allargs=list()
        del checklist[:] 
        for dicttags in AllExpopentags:
            checklist_dict=dict()
            checklist_dict["Open_Exp_Index"]=dicttags["Open_Exp_Index"]
            checklist_dict["Close_Exp_Index"]=dicttags["Close_Exp_Index"]
            checklist_dict["Open_Exp"]=dicttags["Open_Exp"]
            checklist_dict["Close_Exp"]=dicttags["Close_Exp"]
            checklist.append( checklist_dict)
        All_crossing_pairs=ExtractMaxArgumentsobj.getexpargs(ParsedString,Allargs)
        Non_crossing_pairs=All_crossing_pairs[0]
        Left_pairs=All_crossing_pairs[1]
        Rem_String=All_crossing_pairs[2]
        for pair_dict in Non_crossing_pairs:
                    len_ParsedStr=len(ParsedString) 
                    start=ParsedString.find(pair_dict["Open_Exp"])
                    end_exp_start=ParsedString.find(pair_dict["Close_Exp"])
                    end_exp_len=len(pair_dict["Close_Exp"])
                    Allargs.append(ParsedString[start:end_exp_start+end_exp_len])
                    ParsedString=ParsedString[0:start] + ParsedString[end_exp_start+end_exp_len:len_ParsedStr]
        return(Allargs,Rem_String)            
    
    

    
    
    def Removeblk_smallargs_list(self,AllArgs,minlen) :
        Newarg=list()
        for arg in AllArgs:
            arg=self.Removeblk_smallarg_string(arg,minlen)  
            if arg.endswith(","):
                arg=arg[:-1]+"."
            if arg:    
                Newarg.append(arg)
        return  Newarg    
    
    def Removeblk_smallarg_string(self,rem_string,minlen):
        rem_string=" ".join(rem_string.split())
        if rem_string[0:4]=="that":
            rem_string=rem_string[4:]
        tokens=word_tokenize(rem_string)
        #=======================================================================
        # if tokens:
        #     if str(tokens[0]).lower()=="that":
        #         rem_string=" ".join(tokens[1:])
        #=======================================================================
        len_rem=len(tokens) 
        if rem_string.endswith(","):
                rem_string=str(rem_string[:-1]+".")
        if rem_string.endswith("."):
            if  len_rem < minlen:
                rem_string=""
        else:
            if  len_rem < minlen-1:
                rem_string=""
                
        return  rem_string 
    
    def DelspacebeforePeriod(self,Arg):
        if Arg[-1] !=".":
            Arg=Arg.rstrip() +"."
        if Arg[-1]=="."  :
            Arg=Arg[:-1]
            Arg=Arg.rstrip() +"."
        return Arg    
            
        
          
                  
                      
    def WriteAllArgsCsv(self,AllRows):
        ParsedRows=list()
        for Row in AllRows:
            ParsedString=Row["Parsed_String"]
            ParsedString_FindAtt=self.RemoveAttr(ParsedString,"Attr")
            ParsedString=ParsedString_FindAtt[0]
            FindAttr=ParsedString_FindAtt[1]
            ParsedString=self.Removeconn(ParsedString ,"conn")
            AllExpopentags_FindExp=self.FindAllExpopen_closeTags(ParsedString)
            AllExpopentags= AllExpopentags_FindExp[0]
            FindExp=AllExpopentags_FindExp[1]
            AllArgs_Remstring=self.getargsText(AllExpopentags,ParsedString)
            AllArgs=AllArgs_Remstring[0]
            rem_string=AllArgs_Remstring[1]
            AllArgs=self.RemoveExptags_List(AllArgs)
            rem_string=self.RemoveExptags_String(rem_string)
            rem_string=self.Removeblk_smallarg_string(rem_string,4)
            AllArgs=self.Removeblk_smallargs_list(AllArgs,3)
            if rem_string:
                AllArgs.append(rem_string)
            #print AllArgs
            Arg_No=0
            for Arg in AllArgs:
                Arg=self.DelspacebeforePeriod(Arg)
                Arg_No=Arg_No+1
                ArgRow=copy.deepcopy(Row)
                ArgRow["Arg_No"]=str(Arg_No)
                ArgRow["Parsed_Argument"]=Arg
                ArgRow["FindAttr"]=FindAttr
                ArgRow["FindExptags"]=FindExp
                ParsedRows.append(ArgRow)
                #print Arg
        
        fieldnames=ParsedRows[0].keys()
        FileHandling.write_csv(self.OutputFile, ParsedRows, fieldnames)        
                

def Execute(ExtractMaxArgumentsobj):
    global checklist
    AllRows= FileHandling.read_csv(ExtractMaxArgumentsobj.InputFile)
    ExtractMaxArgumentsobj.WriteAllArgsCsv(AllRows)
    
        






if __name__ == '__main__':
    #ParsedString=""" {Attr_0 {Exp_0_Arg2 {Exp_0_Arg1 S1 {Exp_0_conn_Asynchronous then Exp_0_conn} states Attr_0} that {Exp_1_Arg1 in many anglo countries , it is not for a heterosexual contract , Exp_1_Arg1} {Exp_1_conn_Conjunction and Exp_1_conn} {Exp_1_Arg2 in marriage with couples who can not have children , it 's not for a family unit either Exp_1_Arg2} . Exp_0_Arg1} Exp_0_Arg2} """
    #ParsedString=""" {Exp_0_Arg1 S1 responds angrily and with homosexual slurs , Exp_0_Arg1} {Exp_0_conn_Conjunction and Exp_0_conn} {Exp_0_Arg2 requests that S2 take his comments up with Obama . Exp_0_Arg2}"""
    #ParsedString="""{Exp_0_Arg2 {Exp_0_Arg1 This person {Exp_0_conn_Conjunction also Exp_0_conn} uses the parallel of treatment of blacks and women , {Attr_0 but argues Attr_0} that morality was an excuse to hide the prejudice . Exp_0_Arg1} Exp_0_Arg2}"""
    #ParsedString="""{Exp_0_Arg1 S1 believes it is completely unfair that gay marriage be dismissed or disliked Exp_0_Arg1} {Exp_0_conn_Conjunction and Exp_0_conn} {Attr_0 {Exp_0_Arg2 S2 argues Attr_0} that no matter what S1 believes is right or wrong , the majority of people control what is normal in our society . Exp_0_Arg2}"""
    #ParsedString="{Attr_0 {Exp_0_Arg1 He says Attr_0} there are many married heterosexual couples who either choose not to have children or ca n't Exp_0_Arg1} , {Exp_0_conn_Cause so Exp_0_conn} {Exp_0_Arg2 marriage is not simply about having a family Exp_0_Arg2} ."
    #ParsedString="{Attr_0 S1 feels Attr_0} marriage is classified by a heterosexual contract and {Exp_0_Arg1 is not legal or natural Exp_0_Arg1} {Exp_0_conn_Condition if Exp_0_conn} {Exp_0_Arg2 it involves couples of the same sex Exp_0_Arg2} ."
    global checklist
    checklist=[]
    if __name__ == '__main__':
        topic="gay-rights-debates"
        InputFile=os.getcwd()+"/Parserdata/" +topic+ "/Summaries/ParsedRelations"
        OutputFile=os.getcwd()+"/Parserdata/" +topic+ "/Summaries/ParsedArguments"
        ExtractMaxArgumentsobj=ExtractMaxArguments(InputFile,OutputFile)
        Execute(ExtractMaxArgumentsobj)
   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#===============================================================================
# def RemovePair():
#     Checklist=[(2,72), (20,73),(22,70), (25,30)]
#     sortedlist=sorted(Checklist,key=itemgetter(0))
#     i=0
#     NewList=list()
#     len_sortedlist=len(sortedlist)
#     while i< len_sortedlist:
#         condition=True
#         checkpair =sortedlist[i]
#         removelist=copy.deepcopy(sortedlist)
#         del removelist[i]
#         for pair in removelist:# check for every pair if it is within checked pair list
#             if pair[0] in range(checkpair[0],checkpair[1]) or pair[1] in range(checkpair[0],checkpair[1]) :
#                 condition=False
#                 i=i+1
#                 break    
#         if condition==True:
#             NewList.append(checkpair)
#             sortedlist.remove(checkpair)
#             sortedlist=sorted(sortedlist,key=itemgetter(1))
#             i=0
#             len_sortedlist=len(sortedlist)
#     
#===============================================================================