#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on Nov 23, 2014
 OutputCsv="/Users/amita/git/summary_repo/Summary/src/Similarity_Labels/Similarity_Data/CD_Convince_Forums_taining_gayrights.csv"
 contains gay marraige posts from CD , convince me and from forums those discussions which are not a apart of dialog corpus
@author: amita
'''
from copy import deepcopy
import FileHandling
from file_formatting import csv_wrapper
import NewFormat_text
import unidecode
import unicodedata
fields=["dataset_id"  ,  "discussion_id"  ,  "post_id"  ,  "discussion_url"]


def ascii_only(text):
    """If you really can't use unicode..."""
    
    #nfkd = unicodedata.normalize('NFKD', text)
    chars = list()
    for ch in text:
        #TODO: Handle punctuation and other things which this can miss
        if 9 <= ord(ch) <= 126:
            chars.append(ch)
    ascii_str = ''.join(chars)
    return ascii_str

def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

def disAvoid(discussiondialogcorpus):
    rows1=FileHandling.read_csv(discussiondialogcorpus)
    disavoid=[]
    for row in rows1:
        disavoid.append(row["discussion_id"])
    setdiscavoid=set(disavoid)    
    return  setdiscavoid
def AddTopicDataset(InputCsv,AppendCsv,Output,dataset, discussionsAvoid,topic_id,OutputText):
    rows1=FileHandling.read_csv(InputCsv)
    rows2=FileHandling.read_csv(AppendCsv)
    Allrows=list()
    Lines=list()
    count=0
    for row in rows1:
        NewRow=dict()
        for field in fields :
            NewRow[field]=row[field]
        text=ascii_only(row["text"]) 
        text=text.replace("\n", " ") 
        text=text.replace('"', "") 
           
        NewRow["text"]= text 
        NewRow["topic_id"]=topic_id  
        Allrows.append(NewRow)
        Lines.append(text+"\n")
    for row in rows2:
        if row["discussion_id"]==str("788"):
            print "stop"
        if row["dataset_id"]==str("1") and  row["discussion_id"] in discussionsAvoid:
            count=count+1
            print count
        else:
            if row["dataset_id"]== str(1) and  row["discussion_id"]==str(9391) and row["post_id"]==str(402):
                print row
                
                continue                                      
                                                   
            NewRow=dict()
            for field in fields :
                NewRow[field]=row[field]
            text=ascii_only(row["text"]) 
            text=text.replace("\n", " ") 
            text=text.replace('"', "")    
            NewRow["text"]= text 
            NewRow["topic_id"]=topic_id 
            Allrows.append(NewRow)
            Lines.append(text+"\n")
            
    fieldnames= ["dataset_id"  ,  "discussion_id"  ,  "post_id"  ,  "discussion_url", "topic_id","text"]  
    csv_wrapper.write_csv(Output, Allrows) 
    FileHandling.WriteTextFile(OutputText, Lines)

if __name__ == '__main__':
    AppendCsv="/Users/amita/git/Argument_Extraction_Rep/Argument_Extraction/src/Data_pkg/Data/SQLResult/Forums/Forums_gay-rights-debates"
    InputCsv="/Users/amita/git/summary_repo/Summary/src/Similarity_Labels/Similarity_Data/CD_Convince_gayrights"
    discussiondialogcorpus="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/MTdata/AllMTdata/MT123"
    OutputCsv="/Users/amita/git/summary_repo/Summary/src/Similarity_Labels/Similarity_Data/CD_Convince_Forums_taining_gayrights.csv"
    OutputText="/Users/amita/git/summary_repo/Summary/src/Similarity_Labels/Similarity_Data/CD_Convince_Forums_taining_gayrightsText"
    discussionsAvoid=disAvoid(discussiondialogcorpus)
    dataset=1 # add forums
    topic_id=str("8")
    AddTopicDataset(InputCsv,AppendCsv,OutputCsv,dataset, discussionsAvoid,topic_id,OutputText)
    