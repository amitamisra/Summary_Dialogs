#!/usr/bin/env python
# -*- coding: utf-8 
from nlp.text_obj import TextObj
import sys
'''
Created on Aug 18, 2014
NOt used in naacl
@author: amita
'''
# This program takes an input a json Dir created using DISCO Toolkit in java and writes a corresponding csv file for file craeteFeatures.py
from data_pkg import FileHandling
from data_pkg import NewFormat_text
import os
from random import shuffle
def createinputML(OutputDir,Outfile_All):
    AllrowsAllfiles=list()
    Filelist=os.listdir(OutputDir)
    try:
        for filename in Filelist:
            if filename.startswith("."):
                continue
            rowdicts=FileHandling.read_csv(OutputDir+"/"+filename[:-4])
            fieldnames=rowdicts[0].keys()
            AllrowsAllfiles.extend(rowdicts)
         
        shuffle(AllrowsAllfiles)
        shuffle(AllrowsAllfiles)
        FileHandling.write_csv(Outfile_All, AllrowsAllfiles, fieldnames)  
         
    except Exception as e :
        print str(e)
         
def  convert_json_tocsv( InputDir,OutputDir):
    Filelist=os.listdir(InputDir)
    try:
        for filename in Filelist:
            if filename.startswith("."):
                continue
            Inputjson=InputDir+"/"+ filename
            rowdicts=FileHandling.jsontorowdicts(Inputjson)
            fieldnames= sorted(rowdicts[0].keys())
            OutputFile=OutputDir+"/"+filename[:-4]
            newrowdicts=list()
            for row in rowdicts:
                newrow=dict()
                for key in fieldnames:
                    #newrow[key]=row[key]
                    text_obj = TextObj(row[key])
                    text=text_obj.text
                    #print type(text)
                    new_text=text.encode('ascii', 'ignore')
                    newrow[key]=NewFormat_text.ascii_only(new_text)
                    
                    
                    
                newrowdicts.append(newrow)        
                
            FileHandling.write_csv(OutputFile, newrowdicts, fieldnames)
    except Exception as e:
        s = str(e)
        print "error in file" + filename
        print s
        print newrow
        sys.exit(1)
            
        


if __name__ == '__main__':
    topic="gay-rights-debates"     
    InputDirDir=os.getcwd()+ "/data_pkg/"+ topic +"/BalPairExtended_3/BalPairExtendJson_3"
    OutputDir=os.getcwd()+ "/data_pkg/"+ topic +"/BalPairExtended_3/BalPairExtended_3_Csv"
    Outfile_All=os.getcwd()+ "/data_pkg/"+ topic +"/Input_Features_3"
    convert_json_tocsv( InputDirDir,OutputDir)
    createinputML(OutputDir,Outfile_All)