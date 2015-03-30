'''
Created on Sep 4, 2014
This files takes an input an LabelUpdated/AllMTSummary created using combineMTResults.py, removes regular expression in between
summaries and creates summaries in para_data/"+topic+"/cluster/Summaries/InputSummaries.csv
Further execute a java program using stanford parser to create input as sentences using DoctoSent.java to give output as json file 
InputStrings.json.
@author: amita
'''
import os
import FileHandling
import re


#TODO : change remove regular expression
def  createummariesfile(InputFile,summaryFile):
        Allsummary_list= list()
        fieldnames=["text","key"]
        rowdicts=FileHandling.read_csv(InputFile)
        for row in rowdicts:
            if "6646_280" in row["Key"]:
                print "stop"
            
            summary=row["Summaries"]
            summ = re.sub(r'-*\s*D[0-9]*\s*-*\s*', r'', summary)
            summ= " ".join(summ.split())
            #--------------------------- Newsummary=re.split(self.Regex,summary)
            #-------------------------------------------------- print Newsummary
            #summ_text=preprocess_text.preprocess(summ, stem,stop)
            #sent_tokenize_list = sent_tokenize(summ)
            #for sent_str in sent_tokenize_list:
            row_str=dict()
            #sent_str="  ".join(sentc for sentc in sent)
            row_str["text"]=summ
            row_str["key"]=row["Key"]
            Allsummary_list.append(row_str)
        #shuffle(Allsummary_list)
        FileHandling.write_csv(summaryFile, Allsummary_list, fieldnames)
def createstringssummary(summaryFile,StringsFile) :
    FileHandling.convert_json_tocsv(summaryFile, StringsFile)
       
if __name__ == '__main__':
    Regex="[-]*\sD[0-9]*\s[-]*"
    topic="gay-rights-debates"
    InputFile= os.getcwd() +"/CSV/"+ topic +"/MTdata/LabelUpdated/AllMTSummary"#used for summaries not labels
    summaryFile=os.path.dirname(os.getcwd()) + "/paraphrase/para_data/"+topic+"/cluster/Summaries/InputSummaries" 
    StringsFile=os.path.dirname(os.getcwd()) + "/paraphrase/para_data/"+topic+"/cluster/Summaries/InputStrings"
    #createummariesfile(InputFile,summaryFile)#execute once to create summarys as text file
    #In between these functions execute a java program DoctoSent.java that writes these summaries as sentences using stanford parser to a json file JsonStrings"
    
    JsonStrings=os.path.dirname(os.getcwd()) + "/paraphrase/para_data/"+topic+"/cluster/Summaries/InputStrings.json"
    createstringssummary(JsonStrings,StringsFile)
