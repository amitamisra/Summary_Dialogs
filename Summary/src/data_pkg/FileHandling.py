#!/usr/bin/env python
#coding: utf8 
'''
Created on Apr 27, 2014

@author: amita
'''
import os
import csv  
import sys
import codecs
from collections import defaultdict
import MySQLdb as mdb
import unicodecsv
import json
import NewFormat_text
#from nlp.text_obj import TextObj
from operator import itemgetter
from copy import deepcopy

import sys
from random import shuffle

def AddUniqueRowNo(AllRows):
    count=0
    AllNewRows=[]
    for row in AllRows:
        Newrow=deepcopy(row)
        Newrow["_"+"uniqueRowNo"]=count # gives each row a unique number for Mechanical turk
        count=count+1
        AllNewRows.append(Newrow)
    return AllNewRows    
    
        
def splitcsv(inputcsv,outfolder,numtosplit):
    rows=read_csv(inputcsv)
    start=0
    fieldnames=rows[0].keys()
    sizefile=len(rows)/numtosplit
    rem=len(rows) % numtosplit
    for count in range(0,numtosplit):
        rowbegin=start
        if count == numtosplit:
            rowend=sizefile + start
        else:
            rowend=sizefile + + start+ rem +1 
        rowswrite=rows[rowbegin:rowend]
        out=outfolder+"/"+inputcsv+ "_"+ str(count)
        write_csv(out,rowswrite,fieldnames)
        start=rowend
        
def csvtojson(inputfile):
    Allrows= read_csv(inputfile)
    writejson(Allrows,inputfile)
# write a list of dictionaries to a json file
def  writejson(list_dict,filename):
    
    with open(filename+".json", 'w') as f:
        json.dump(list_dict, f)

#takes an input json file created during DISCO  gives the rowdicts       
def jsontorowdicts(listofdictfile): 
    with open(listofdictfile, 'rb') as fp:
        rowdicts = json.load(fp) 
    return  rowdicts     
def writeHtml(outputfile,all_lines):
    f = open(outputfile +".html",'w')
    #-------------------------------------------------------- for line in lines:
        #--------------------------------------------- all_lines=" ".join(lines)
    all_lines= """<html><head></head><body>""" + all_lines +"""</body> </html>"""  
    f.write(all_lines)    
    f.close()
 
def write_csv(outputcsv, rowdicts, fieldnames):
            restval=""
            extrasaction="ignore"
            dialect="excel"
            outputfile = codecs.open(outputcsv + ".csv",'w')
            csv_writer = csv.DictWriter(outputfile, fieldnames, restval, extrasaction, dialect, quoting=csv.QUOTE_NONNUMERIC)
            csv_writer.writeheader()
            csv_writer.writerows(rowdicts) 
            outputfile.close()
                
def read_csv(inputcsv):   
        inputfile = codecs.open(inputcsv+ ".csv",'r') 
        result = list(csv.DictReader(inputfile))
        return result              
                
def KeepColumns_Csv(InputCsvStr,OutputCsvStr, fields):
    fields=sorted(fields)
    infile= open(InputCsvStr+".csv","r")
    outfile= open(OutputCsvStr +".csv", "w")
    r = csv.DictReader(infile)
    w = csv.DictWriter(outfile, fields, extrasaction="ignore")
    w.writeheader()
    for row in r:
        w.writerow(row)   
        
def getcolumnnames(db1,tablename):
    Setcolnames=set()
    cursor = db1.cursor(mdb.cursors.DictCursor) 
    sql="select * from "+ tablename
    cursor.execute(sql )
    rowdict = cursor.fetchone()
    col_names = [keyrow for keyrow in rowdict.keys()]
    for colname in col_names:
        Setcolnames.add(colname)
        
    return Setcolnames                                            
def WriteTextFile(Filename,Lines): 
        f = open(Filename+".txt", "w")
        f.writelines(Lines)
        f.close()
def ReadTextFile(Filename): 
        f = open(Filename, "r")
        Text=f.readlines()
        f.close()
        return Text
#convert json as list of hashed items ( written from DISCO) to csv        
def  convert_json_tocsv( InputFileJsontxt,OutputCSv):
    
            rowdicts=jsontorowdicts(InputFileJsontxt)
            fieldnames= sorted(rowdicts[0].keys())
            newrowdicts=list()
            for row in rowdicts:
                newrow=dict()
                for key in fieldnames:
                    newrow[key]=row[key]
                    #text_obj = TextObj(row[key])
                    #text=text_obj.text
                    #print type(text)
                    #new_text=text.encode('ascii', 'ignore')
                    if type(newrow[key]) is str :
                        newrow[key]=NewFormat_text.ascii_only(newrow[key])
                    else:
                         print " type not string"   
                newrowdicts.append(newrow)        
                
            write_csv(OutputCSv, newrowdicts, fieldnames)
    


def  convert_json_tocsv_posts( InputFileJsontxt,OutputCSv):
            rowdicts=jsontorowdicts(InputFileJsontxt)
            fieldnames= sorted(rowdicts[0].keys())
            newrowdicts=list()
            for row in rowdicts:
                newrow=dict()
                for key in fieldnames:
                    newrow[key]=row[key]
                    newrow[key]=NewFormat_text.ascii_only_posts(newrow[key])
                newrowdicts.append(newrow)        
                
            write_csv(OutputCSv, newrowdicts, fieldnames)


def Randomize(inputfile,output):
    rows= read_csv(inputfile)
    shuffle(rows)
    fieldnames=rows[0].keys()
    write_csv(output,rows,fieldnames)


#remove duplicates from a csv file    
def RemoveDup(Input,Output):  
    AllRows=read_csv(Input) 
    rowdictsNodup = []
    for i in range(0, len(AllRows)):
        if AllRows[i] not in rowdictsNodup:
            rowdictsNodup.append(AllRows[i])
            
    fieldnames=sorted(rowdictsNodup[0].keys())
    write_csv(Output, rowdictsNodup, fieldnames)   

def SortRows(AllRows,fieldname):
    sortedrows=sorted(AllRows,key = itemgetter(fieldname), reverse =True)
    return sortedrows
                                                                   
if __name__ == '__main__':
#     Inputjson="/Users/amita/git/summary_repo/Summary/src/Similarity_Labels/Similarity_Data/CD_Convince_gayrights_Sent.json"
#     OutputCsv="/Users/amita/git/summary_repo/Summary/src/Similarity_Labels/Similarity_Data/CD_Convince_gayrights_Sent"
    
    Inputjson="/Users/amita/git/summary_repo/Summary/src/Similarity_Labels/Similarity_Data/CHKCD_Convince_Forums_taining_gayrights_.json"
    OutputCsv="/Users/amita/git/summary_repo/Summary/src/Similarity_Labels/Similarity_Data/CCHKCD_Convince_Forums_taining_gayrights_"
    
    
    convert_json_tocsv_posts(Inputjson,OutputCsv)