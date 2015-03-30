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
import sys
from random import shuffle

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
        try:
            restval=""
            extrasaction="ignore"
            dialect="excel"
            outputfile = codecs.open(outputcsv + ".csv",'w')
            csv_writer = csv.DictWriter(outputfile, fieldnames, restval, extrasaction, dialect, quoting=csv.QUOTE_NONNUMERIC)
            csv_writer.writeheader()
            csv_writer.writerows(rowdicts) 
            outputfile.close()
        except csv.Error :
                print "csverror" + outputcsv +" in function FileHandling.write_csv"
                sys.exit(1)  
                
def read_csv(inputcsv):   
    try:
        inputfile = codecs.open(inputcsv+ ".csv",'r') 
        result = list(csv.DictReader(inputfile))
        return result              
    except csv.Error:
                print "inputcsverror" + inputcsv + " in function FileHandling.read_csv"
                sys.exit(1)   
                
                
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
    try:
        f = open(Filename+".txt", "w")
        try:
                f.writelines(Lines)
        finally:
                f.close()
    except IOError:
        print Filename +" Error, not found or directory does not exist  , in function FileHandling.WriteTextFile"     
        sys.exit(1)      
def ReadTextFile(Filename): 
    try:
        f = open(Filename, "r")
        try:
                Text=f.readlines()
                return Text
        finally:
                f.close()
    except IOError:
        print Filename +" Error, not found  in function FileHandling.ReadTextFile"       
        sys.exit(1) 
        
#convert json as list of hashed items ( written from DISCO) to csv        
def  convert_json_tocsv( InputFileJsontxt,OutputCSv):
    try:
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
                    newrow[key]=NewFormat_text.ascii_only(newrow[key])
                newrowdicts.append(newrow)        
                
            write_csv(OutputCSv, newrowdicts, fieldnames)
    except Exception as e:
        s = str(e)
        print "error in file" + InputFileJsontxt + "in function FileHandling.convert_json_tocsv"
        print s
        sys.exit(1)



def  convert_json_tocsv_posts( InputFileJsontxt,OutputCSv):
    try:
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
    except Exception as e:
        s = str(e)
        print "error in file" + InputFileJsontxt + "in function FileHandling.convert_json_tocsv"
        print s
        sys.exit(1)


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
if __name__ == '__main__':
#     Inputjson="/Users/amita/git/summary_repo/Summary/src/Similarity_Labels/Similarity_Data/CD_Convince_gayrights_Sent.json"
#     OutputCsv="/Users/amita/git/summary_repo/Summary/src/Similarity_Labels/Similarity_Data/CD_Convince_gayrights_Sent"
    
    Inputjson="/Users/amita/git/summary_repo/Summary/src/Similarity_Labels/Similarity_Data/CHKCD_Convince_Forums_taining_gayrights_.json"
    OutputCsv="/Users/amita/git/summary_repo/Summary/src/Similarity_Labels/Similarity_Data/CCHKCD_Convince_Forums_taining_gayrights_"
    
    
    convert_json_tocsv_posts(Inputjson,OutputCsv)