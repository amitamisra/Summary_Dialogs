#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on Jul 11, 2014
This module takes data_pkg from MT output file AllMTSummary.csv and changes it to input 
for topic modeling at sentence as a document for each "pyramid/dialog/set_of_5_summaries"
@author: amita
'''
from data_pkg import FileHandling
import re
import os
import sys
from data_pkg import NewFormat_text
from nlp.text_obj import TextObj
import nltk.data
import nltk
import os


# This function takes an input as all MT data_pkg from file /MTdata/AllMTSummary and creates a directory
# for each dialog. Each file in the directory corresponds to a sentence in the summary.
def createtopic_modeling_dir(inputcsv,outputdir,regex):
    #sent_detector = nltk.data_pkg.load('tokenizers/punkt/english.pickle')
    rowdicts=FileHandling.read_csv(inputcsv)
    for row in rowdicts:
        key=row["Key"]
        dialogkeydir=outputdir +"/"+key+"/"
        if not os.path.exists(dialogkeydir):
            os.makedirs(dialogkeydir)
        else:
            print str(key) +"directory already exists"
            sys.exit(1)    
        summaries=row["Summaries"]
        splitter=re.compile(regex)
        sentenceList=splitter.split(summaries)
        if len(sentenceList)!= noofsummaries+1:
            print "Error in spiltting regular expresson in file with key " + str(key)
            sys.exit(1)
        for counter in range(0,len(sentenceList)):
            summmary_sent=sentenceList[counter]
            if summmary_sent:
                summmary_sent=summmary_sent.strip()
                summary_sentnew=summmary_sent.replace("S1"," ")
                summary_sentnew=summary_sentnew.replace("S2"," ")
                summmary_sentnew=NewFormat_text.ascii_only(summary_sentnew)
                text_obj = TextObj(summmary_sentnew) 
                sentences=text_obj.sentences
                noofsentences=len(sentences)
                for count in range(0,noofsentences):
                    Lines=list()
                    Lines.append(" ".join(sentences[count]))
                    textfile=dialogkeydir + "summ_"+ str(counter) +"sent_" + str(count)
                    FileHandling.WriteTextFile(textfile, Lines)
                    
            #print('\n-----\n'.join(sent_detector.tokenize(summmarycount.strip())))
            
             
            
                
            
        
        
        
        
        
        
        
    
    





if __name__ == '__main__':
    regex="\s*[-]+\\s*D[0-9]*\\s+[-]+"
    topic="gay-rights-debates"
    noofsummaries=5
    inputcsv=os.path.dirname(os.getcwd()) + "/data_pkg/CSV/"+ topic + "/MTdata/AllMTSummary"
    outputdir=os.getcwd() + "/topic_data/"+ topic 
    createtopic_modeling_dir(inputcsv,outputdir,regex)