'''
Created on Aug 19, 2014
This file read dialogs from alldialogs put on MT finds the most similar sentence to the contributors of the dialog
It reads all contributors from jsonfile created in program scores_pyramid
@author: amita
NOt used in naacl
'''
import operator
import itertools
import os
import json
import sys
from data_pkg import FileHandling
from nlp.text_obj import TextObj
import createFeatures
from operator import itemgetter

def computesim(sentences,all_contrib):
    stem=True
    allsim=list()
    for sentoken in sentences:
        simdict=dict()
        sen= " ".join(sentoken)
        cos=createFeatures.processPOS(sen,all_contrib,stem) 
        simdict["sen"]=sen
        simdict["cos"]=cos
        allsim.append(simdict)
        
    sorted_allsim = sorted(allsim, key=itemgetter('cos'),reverse=True) 
    return  sorted_allsim    


def FindSim(DialogRow,ListScus,AllrowSim):
    for row in  ListScus:
        if row["weight"] > 2 :
            #IdList.append(row["id"])
            
            weight=row["weight"] 
            all_contrib=""
            rowdict=dict()
            for contributor in row["contrib"]:
                all_contrib=all_contrib +  ", ".join(contributor) +" "
            text_obj = TextObj(DialogRow.decode('utf-8', 'replace')) 
            sentences=text_obj.sentences
            Allsim=computesim(sentences,all_contrib)
            rowdict["AllSim"]=Allsim 
            rowdict["label"]=row["label"] 
            rowdict["weight"]=weight
            rowdict["id"]=row["id"] 
            rowdict["key_user"]=row["key_user"] 
            rowdict["contrib"]= row["contrib"]
            AllrowSim.append(rowdict)
    
def Dialog_contributor(DialogFile, Contris_json):
    AllrowSim=list()
    AllDialogs=FileHandling.read_csv(DialogFile)
    with open(Contris_json, 'rb') as fp:
            rowdicts = json.load(fp)
    rowdicts.sort(key=operator.itemgetter("key_user"))
    for key, items in itertools.groupby(rowdicts, operator.itemgetter('key_user')):
            DialogRow=[row for row in AllDialogs if row["key"] in key]
            if len(DialogRow) > 1:
                print "Error in filtering dialogs from alldialogs file" + key
                sys.exit(1)
            ListScus=list(items)
            FindSim(DialogRow[0]["Dialog"],ListScus,AllrowSim)
    return  AllrowSim       
if __name__ == '__main__':
    fieldnames=["AllSim","label","weight","id","key_user","contrib"]
    topic="gay-rights-debates"   
    DialogFile=os.path.dirname(os.getcwd()) + "/data_pkg/CSV/"+ topic+"/MTdata/AllDialogs_on_MT"
    Contris_json=os.path.dirname(os.getcwd()) + "/data_pkg/CSV/"+ topic+"/MTdata/AllScusJson.json"
    outcsv=os.path.dirname(os.getcwd()) + "/data_pkg/CSV/"+ topic+"/MTdata/contrib_MTDialog_Sim"
    AllRowSim=Dialog_contributor(DialogFile, Contris_json)
    FileHandling.write_csv(outcsv, AllRowSim, fieldnames)