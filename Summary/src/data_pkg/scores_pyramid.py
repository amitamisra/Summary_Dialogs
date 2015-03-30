#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on May 22, 2014
This file calculates pyramid scores of each of the annotators
3 classes , SCU,pyramid and User

@author: amita
'''
from __future__ import division
import xml.etree.ElementTree as ET
import os
import FileHandling
from collections import Counter,defaultdict
from operator import itemgetter
import re
import sys
import json



#creates an Scu object
def get_scus(filename):
    #parser = XMLParser(encoding="utf-8")
    tree = ET.parse(filename)
    root = tree.getroot()
    lines=[element for element in root.iter('line')]
    return ([Scu(element) for element in root.iter('scu')],lines)

#map weights to tiers and create a counter of tiers
def AddTiers(Scu_objects):
    Tiers= defaultdict() # keys are weights, values are tiers
    All_scus_wts = sorted([Scu_object.weight for Scu_object in Scu_objects],reverse =True)
    counter_scu_wts=Counter(All_scus_wts)
    counter_tiers=Counter()
    set_scus_wts=sorted(set(All_scus_wts),reverse=True)
    top_tier=len(set_scus_wts)
    counter=0
    total_scu_count=len(All_scus_wts )
    
    while counter < total_scu_count:
        if counter==0:
            Tiers[All_scus_wts[counter]]=top_tier
            top_tier=top_tier-1
            counter=counter+1
        else:
            if  All_scus_wts[counter] == All_scus_wts[counter-1] :
                    counter=counter+1
                    
            else:
                    Tiers[All_scus_wts[counter]]=top_tier
                    top_tier=top_tier-1  
                    counter=counter+1  
    for scu in  Scu_objects:
        scu.tier=Tiers[scu.weight]
#---------------------------- create a counter of tiers using counter of weights
    for key,value in Tiers.iteritems():
        counter_tiers[value]=counter_scu_wts[key]
         
    return counter_tiers    
        
          
class Scu(object):
    def __init__(self,element):
        self.contrib=list()
        self.id = int(element.get('uid'))
        self.label = element.get('label')
        for contributor in element.iter('contributor'): 
            label_start=[ (c.get('label'),c.get('start') )for c in contributor.iter('part')]
            #===================================================================
            # if len(label_start) >1:
            #     print "stop here"
            #===================================================================
            sorted_list=sorted(label_start,key = lambda x: x[1])
            label_list, start_list = zip(*sorted_list)
            self.contrib.append(label_list)
        self.weight = len(self.contrib)
        self.tier=0
        
class Pyramid(object):
    def __init__(self,filename):
        
        scus,text = get_scus(filename)#scus is a list of scu objects
        self.countertiers=AddTiers(scus)
        self.scus=scus
        self.text=text
class user():
    def __init__(self): 
        self.user_scu=dict()
        self.user_scuweight=dict()
        self.user_scutier=dict()
        self.id=""
        self.index=""    
        self.scucount=0 
        self.contrib=""
        self.SecondSummand_count=0
        self.Tier=list()
        self.SecondSummand=0
        self.pyramid_score=0.0
def firstj(counter_tiers,NumScu):
    sum_j=0
    for (key, value) in counter_tiers:
        sum_j=sum_j+value
        if sum_j >= NumScu:
            tierno=key
            break        
    return tierno

def Addtextuser(pyramid,regex):
    lines=pyramid.text
    text_list=[c.text for c in lines if c.text is not None]
    textstring=" ".join(text_list)
    Usertext=filter(None,re.split(regex,textstring))
    return Usertext
def topic_model(outputfilescu,Allrows_scu, fieldnames_scu):
    fieldnames_scu_topic=list(fieldnames_scu)
    fieldnames_scu_topic.append("topic_contrib_str")
    fieldnames_scu_topic.append("id_topic_contrib")
    topic_row=list()
    
    for row in Allrows_scu:
        count_id=1
        topic_contrib=row["contrib"] 
        for topiccontriblist in topic_contrib:
            newrow=dict(row)
            #print topiccontriblist
            topic_contrib_str =" ".join(topiccontriblist)
            newrow["topic_contrib_str"]= topic_contrib_str
            newrow["id_topic_contrib"]=row["key_user"]+ "_"+ str(row["id"]) +"_" + str(count_id)
            topic_row.append(newrow)          
            count_id=count_id+1
    FileHandling.write_csv(outputfiletopic_model,topic_row, fieldnames_scu_topic)
        
def Users_Details(Users_Text,matter_pyr,regex,filename):
    FinalRows=dict()
    Users_Text=Addtextuser(matter_pyr,regex)
    User_count=len(Users_Text)
    if not User_count == no_of_summaries:
        print "Error in counting users"
        sys.exit(1)
    Users=[user() for i in range(User_count)]
    MaxTier_scuweight=0
    for scu in matter_pyr.scus:
        scuid=scu.id
        count_units=0
        Index_added_User=list()
        for allcontri_label in scu.contrib:
            userindex=list()
            for i, string in enumerate (Users_Text) :
                if all (x in string for x in allcontri_label):
                    userindex.append((i,allcontri_label))
            for tup in userindex:
                index=tup[0]
                if index not in Index_added_User:
                    Index_added_User.append(index)
                    contrib=tup[1]
                    Users[index].contrib=Users[index].contrib + " ".join(contrib)
                    Users[index].user_scu["scuid:"+str(scuid)]=1
                    Users[index].user_scuweight["weight_scuid:"+str(scuid)]=scu.weight
                    Users[index].user_scutier["tier_scuid:"+str(scuid)]=scu.tier
                    
                    count_units=count_units+1
                    #Users[index].user_id_wt_tuple["id-wt"]=(scuid,scu.weight )
                    if MaxTier_scuweight < scu.weight:
                        MaxTier_scuweight = scu.weight
        if count_units <> scu.weight:
                    print filename
                    print "error in scuuid: " + str(scu.id)
                    print "error in counting scu_units"   
                    sys.exit(1)                    
    useri=1
    sortedcountertiers= sorted(matter_pyr.countertiers.items(), key=itemgetter(0), reverse=True)
    for userobj in Users:
        
        userobj.scucount=sum(v for v in userobj.user_scu.values() )  
        userobj.dscore=sum(v for v in userobj.user_scutier.values() )  
        if userobj.dscore==0:
            print "Error in dscore, dscore=0"
            sys.exit(1)
        userobj.firstj=firstj(sortedcountertiers,userobj.scucount)
        userobj.Tier=[(key,count) for (key,count) in sortedcountertiers if key >= userobj.firstj+1]
        userobj.FirstSummand=sum([key*count for (key,count) in userobj.Tier])
        userobj.SecondSummand_count=sum([count for (key,count) in userobj.Tier if key >= userobj.firstj+1 ])
        userobj.SecondSummand=userobj.firstj*(userobj.scucount- userobj.SecondSummand_count)
        userobj.Maximum=userobj.FirstSummand+userobj.SecondSummand
        userobj.pyramid_score= userobj.dscore/userobj.Maximum
        file_id=os.path.basename(filename)
        FinalRows["score_:"+ str(useri) ]=userobj.pyramid_score
        
        FinalRows["filename"]=file_id
        useri=useri+1
            
    All_annotator.append(FinalRows)   
        
        
        
if __name__ == '__main__':        
          
    topic="gay-rights-debates"     
    Users_Text=list()
    Regex="[-]*\sD[0-9]*\s[-]*"
    test=0# check annotator scores
    #test=0#normal execution
    if test==1:
        outputfile=os.path.dirname(os.getcwd())+ "/data_pkg/CSV/"+ topic+"/MTdata/MT2/MT2Pyramid/Test_Scores/Test_AllAnnotator_Scores"
        outputfilescu=os.path.dirname(os.getcwd())+ "/data_pkg/CSV/"+ topic+"/MTdata/MT2/MT2Pyramid/Test_Scores/Test_AllScus"
        file_scu_more2=os.path.dirname(os.getcwd())  + "/data_pkg/CSV/"+ topic+"/MTdata/MT2/MT2Pyramid/Test_Scores/Test_more2_Scus"
        Jsonfilescu=os.path.dirname(os.getcwd())+   "/data_pkg/CSV/"+ topic+"/MTdata/MT2/MT2Pyramid/Test_Scores/Test_AllScusJson"
        outputfiletopic_model=os.path.dirname(os.getcwd()) + "/data_pkg/CSV/" +topic+"/MTdata/MT2/MT2Pyramid/Test_Scores/Test_Scus_weights"
        directory= os.path.dirname(os.getcwd())+   "/data_pkg/CSV/"+ topic +"/MTdata/MT2/MT2Pyramid/Test_Scores/Test_annotator_pyramid/"
    else:
        #-------------------------------------------------------- done for phse1
        # outputfile=os.path.dirname(os.getcwd())+"data_pkg/CSV/"+ topic+"/MTdata/LabelUpdated/AllAnnotator_Scores"
        # outputfilescu=os.getcwd() + "/data_pkg/CSV/"+ topic+"/MTdata/LabelUpdated/AllScus"
        # file_scu_more2=os.getcwd() + "/data_pkg/CSV/"+ topic+"/MTdata/LabelUpdated/more2_Scus"
        # Jsonfilescu=os.getcwd() + "/data_pkg/CSV/"+ topic+"/MTdata/LabelUpdated/AllScusJson"
        # outputfiletopic_model=os.path.dirname(os.getcwd()) +"/topic_modeling/topic_data/" + topic + "/modeling_input/LabelUpdated/Scus_weights"
        # directory= os.path.dirname(os.getcwd()) + "/data_pkg/CSV/"+ topic +"/MTdata/LabelUpdated/Allpyramids_v1_labels_updated/"
#------------------------------------------------------------------------------ 
       
       
        outdirectory= os.path.dirname(os.getcwd() ) + "/data_pkg/CSV/"+ topic+"/MTdata/MTPhase2"
        outputfile=outdirectory+"/AllAnnotator_Scores"
        outputfilescu=outdirectory+"/AllScus"
        file_scu_more2=outdirectory+"/more2_Scus"
        Jsonfilescu=outdirectory+"/AllScusJson"
        directory= outdirectory+"/AllPyramids/"
    
    
    fieldnames=["score_:1","score_:2","score_:3","score_:4","score_:5","filename"]
    fieldnames_scu=["weight","label","contrib","key_user","id"]
    no_of_summaries=5
    
    All_annotator=list()
    Allrows_scu=list()
    rows_scu_more2=list()
    
    first =True
    for fileid in os.listdir(directory):
        if "Icon" in str(fileid)  or "Store" in str(fileid): continue
        if not fileid.startswith('.'):
            #print directory+fileid
            matter_pyr = Pyramid(directory+fileid)
            #print directory+fileid
            
            for scu in matter_pyr.scus:
                rowscu=dict()
                rowscu["weight"]=scu.weight
                rowscu["label"]=scu.label
                rowscu["contrib"]=scu.contrib
                rowscu["key_user"]=fileid
                rowscu["id"]=scu.id
                Allrows_scu.append(rowscu)
                if scu.weight > 2 :
                    rows_scu_more2.append(rowscu)
                    
                
            Users_Details(Users_Text,matter_pyr,Regex,directory+fileid)
                
     
    sortedAll_annotator=sorted(All_annotator, key=lambda k: k['filename'].lower())
    FileHandling.write_csv(outputfile,sortedAll_annotator, fieldnames)
    FileHandling.write_csv(outputfilescu,Allrows_scu, fieldnames_scu)
    FileHandling.write_csv(file_scu_more2,rows_scu_more2, fieldnames_scu)
    FileHandling.writejson(Allrows_scu,Jsonfilescu)
    #topic_model(outputfilescu,Allrows_scu, fieldnames_scu)( done for phase 1)
    
