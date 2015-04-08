'''
Created on Aug 24, 2014
This program takes input labels from pyramids created by running scores pyramid from data package  and creates  clusters
@author: amita
'''
from sklearn.feature_extraction.text  import CountVectorizer
from sklearn.feature_extraction.text  import TfidfVectorizer
from  sklearn.cluster import AgglomerativeClustering
import preprocess_text
import os
import data_pkg.FileHandling
import Add_POS
from sklearn import metrics
import sys
import operator
import itertools



#--------------------------------------------- Add POS to the input strings file
def createPOSFile(stringsFile,PosStringsFile,clusterField,keyid):
    Allrow_dicts=data_pkg.FileHandling.read_csv(stringsFile)
    Allposrows=list()
    fieldnames=["Text_original","Noun","Verb","Adj","key"]
    POS_List=["Noun","Adj","Verb"]
    for rowdict_str in Allrow_dicts:
        posrow=dict()
        POS_Dict=Add_POS.ADDPOS_string(rowdict_str[clusterField],POS_List)
        posrow["Text_original"] =rowdict_str[clusterField]
        posrow["Noun"]=POS_Dict["Noun"]
        posrow["Verb"]=POS_Dict["Verb"]
        posrow["Adj"]=POS_Dict["Adj"]
        posrow["key"]=rowdict_str[keyid]
        Allposrows.append(posrow)
    data_pkg.FileHandling.write_csv(PosStringsFile, Allposrows, fieldnames)    
        

class Cluster:
    def __init__(self,num_cluster,StringsFile,vec,clustercsv,clusterfield,keyid,clusterfile_stem,POS,affinity): 
        self.StringsFile= StringsFile
        self.OutclusterFile=clusterfile_stem
        self.num_cluster=num_cluster
        self.affinity=affinity
        self.POS=POS
        self.clustercsv=clustercsv
        self.clusterdfield=clusterfield
        self.keyid=keyid
        self.vec=vec
    # creates a Term Doc vector using CountVectorizer, takes input from /MTdata/AllMTSummarycsv file uses reg expression to remove DO,D1  tags added to summaries
    #-- changes to lowercase , removes stop words, if stem is True then it also performs stemming
   
    #creates a string as row for input to clustering and writes individual sentences to file outStringsFile
    #==========================================================================
    # create a tuple of cluster labels with corr documents , doc ids begin with 0   
    #==========================================================================
    def tuple_cluster_doc(self,Res_Labels,Allstrings,Allrow_dicts):
        fieldnames=["label_cluster","doccount","string","key"]
        doccount=0
        cluster_list=list() 
        for label in Res_Labels:
            row_cluster=dict()
            row_cluster["label_cluster"]=label
            row_cluster["doccount"]=doccount
            row_cluster["string"]=Allstrings[doccount]
            row_cluster["key"]=Allrow_dicts[doccount][self.keyid]
            doccount=doccount+1
            cluster_list.append(row_cluster)
        data_pkg.FileHandling.write_csv(self.clustercsv, cluster_list, fieldnames)       
        return cluster_list
    
    def Create_Agg_cluster(self,stem,stop,processing,remS): 
        
        Allrow_dicts=data_pkg.FileHandling.read_csv(self.StringsFile)
        Allstrings=[rowdict_str[self.clusterdfield] for rowdict_str in Allrow_dicts]
        if self.POS=="ALL":
            Allstrings_process=[preprocess_text.preprocess(string_text, stem,stop) for string_text in Allstrings] 
        else:
            POS_Strings=list()
            if self.POS=="Noun_Verb_AdJ" :
                POS_List=["Noun","Adj","Verb"]
            else:    
                if  self.POS=="Noun_AdJ" :
                    POS_List=["Noun","Adj"] 
                else:
                    print "Error in Part of speech in function Create_Agg_cluster"
                    sys.exit(0)
                    
            #ADDPOS_string returns a dictionary with keys as Noun, Verb, Adj, AllPOSstring. 
            # For Naacl Used   AllPOSstring, this includes noun, verb and adj
            #AllPOSstring signifies to take the key    
            for string in Allstrings:
                POS_String=Add_POS.ADDPOS_string(string,POS_List)["AllPOSstring"] 
                POS_Strings.append(POS_String)                  
            Allstrings_process=[preprocess_text.preprocess(string_text, stem,stop) for string_text in POS_Strings]  
        
        if remS:
            Allstrings_process=[preprocess_text.removeS(text) for text in Allstrings_process]            
        if self.vec=="CountVectorizer":
            vectorizer = CountVectorizer()
        else:
            if self.vec=="TFIdfCountVectorizer":
                vectorizer= TfidfVectorizer()      
        term_doc=vectorizer.fit_transform(Allstrings_process)
        #=======================================================================
        # svd = TruncatedSVD(n_components=5, random_state=42)
        # lsa = make_pipeline(svd, Normalizer(copy=False))
        # term_doc = lsa.fit_transform(term_doc)
        # term_doc = svd.fit_transform(term_doc)
        #=======================================================================
        
        #-------------------------- feature_names=vectorizer.get_feature_names()
        #------------------------------------------------ Array=term_doc.toarray
        if self.affinity=='euclidean':
            Agg_cluster=AgglomerativeClustering(n_clusters=self.num_cluster,affinity='euclidean')
        if self.affinity=='cosine':
            Agg_cluster=AgglomerativeClustering(n_clusters=self.num_cluster,linkage='average',affinity=self.affinity)
        if self.affinity=='l1':
            Agg_cluster=AgglomerativeClustering(n_clusters=self.num_cluster,linkage='average',affinity=self.affinity)    
        Res_Labels=Agg_cluster.fit_predict(term_doc.toarray())
        self.cluster_tup_list=self.tuple_cluster_doc(Res_Labels,Allstrings,Allrow_dicts)
        #print type (term_doc)
        self.metric=metrics.silhouette_score(term_doc.toarray(), Res_Labels, metric=self.affinity)
        #print Res_Labels
        #print("n_samples: %d, n_features: %d" % term_doc.shape)
        
    def  write_cluster(self,processing):
        AllList=list()
        self.cluster_tup_list.sort(key= operator.itemgetter("label_cluster"))
        AllList.append("PREPROCESSING :"+ processing)
        AllList.append("Metric"+ str(self.metric))
        count=0
        for key, items in itertools.groupby(self.cluster_tup_list, operator.itemgetter('label_cluster')):
            AllList.append("\n\n NEW CLUSTER  " + str(count)+"\n\n\n")
            OneCluster=list(items) 
            count=count+1
            for contrib in  OneCluster:
                AllList.append("\n" + contrib["string"] + "\n")
                AllList.append("key  "+contrib["key"] + "\n")
        data_pkg.FileHandling.WriteTextFile(self.OutclusterFile,AllList)
            
def stem_cluster(stringsFile,clustercsv,vec,clusterfield,keyid,stem,stop,processing,POS,clusterfile_stem,num_cluster,remS,affinity,):
        
        
        Clusterobj=Cluster(num_cluster,stringsFile,vec,clustercsv,clusterfield,keyid,clusterfile_stem,POS,affinity)
        
        Clusterobj.Create_Agg_cluster(stem,stop,processing,remS)
        Clusterobj.write_cluster(processing)
    
     
if __name__ == '__main__':
    
    #begin===========================================================================done for NAACL
    # topic="gay-rights-debates"
    # clusterfile_cosine=os.getcwd() + "/para_data/"+topic+"/cluster/LabelUpdated/TFIdf/Cos_Cluster_70_AVG_Noun_Verb_Ad"
    # clustercsv=os.getcwd() + "/para_data/"+topic+"/cluster/LabelUpdated/TFIdf/Cos_Cluster_70_AVG_Noun_Verb_Ad"
    #end===========================================================================done for NAACL
    topic="gun-control"
    guncontrolpyramiddir="/Users/amita/git/FacetIdentification/src/Data_Pkg_Data/CSV/gun-control/MTdata/Phase1/Pyramids_Natural"
    clusterfile_cosine="/Users/amita/git/FacetIdentification/src/Paraphrase_Pkg_data/"+topic+"/cluster/Phase1/TFIdf/Cos_Cluster_70_AVG_Noun_Verb_Ad"
    clustercsv="/Users/amita/git/FacetIdentification/src/Paraphrase_Pkg_data/" + topic+"/cluster/Phase1/TFIdf/Cos_Cluster_70_AVG_Noun_Verb_Ad"
    
    
    
    Regex="[-]*\sD[0-9]*\s[-]*"
    #Initialize all values for clustering
    stem=True 
    stop=True  
    remS=True 
    affinity="cosine"
    vect="TFIdfCountVectorizer"
    num_cluster=70
    choice=2 
    # AVG indicates type linkage in cluster class in scikit
    #choice =1 is for summaries, choice =2 is for labels as input
    
    
    if choice ==1:
        #To be done with summaries as input
        print 
        #begin======================================================================= NOT USED FOR NAACL
        # clusterfield="text" #Field in input file for clustering
        # keyid="key"
        # stringsFile=os.getcwd() + "/para_data/"+topic+"/cluster/Summaries/InputStrings" 
        # PosStringsFile=os.getcwd() + "/para_data/"+topic+"/cluster/Summaries/InputStrings_POS"
        # 
        # #create_strings_file(InputFile,stringsFile) #Not executed now, instead execute summary_string form package data  
        # createPOSFile(stringsFile,PosStringsFile,clusterfield,keyid)
        #end=======================================================================NOT USED FOR NAACL
        
    else:
        if choice ==2:
            #begin ---------------------------------- #To be done with labels as input USED FOR NAACL
            #---------- clusterfield="label" #Field in input file for clustering
            #-------------------------------------------------- keyid="key_user"
            # stringsFile=os.path.dirname(os.getcwd()) + "/data_pkg/CSV/"+ topic +"/MTdata/LabelUpdated/more2_Scus"
            # PosStringsFile=os.getcwd() + "/para_data/"+topic+"/cluster/LabelUpdated/InputStrings_POS_Labels"
            #------ createPOSFile(stringsFile,PosStringsFile,clusterfield,keyid)
            #end------------------------------------------------------------------------------ USED FOR NAACL
            
            #To be done with labels as input
            clusterfield="label" #Field in input file for clustering
            keyid="key_user"
            stringsFile=guncontrolpyramiddir+"/more2_Scus"
            PosStringsFile="/Users/amita/git/FacetIdentification/src/Paraphrase_Pkg_data/"+ topic+"/cluster/Phase1/InputStrings_POS_Labels"
            createPOSFile(stringsFile,PosStringsFile,clusterfield,keyid)
    
    POS="Noun_Verb_AdJ"
    processing="STEMMING, cos Distance, num_cluster=70Nouns_Verb_AdJ"
    stem_cluster(stringsFile,clustercsv,vect,clusterfield,keyid,stem,stop,processing,POS,clusterfile_cosine,num_cluster,remS,affinity)
   
            
            
            
            
            
    #begin=========================================================================== NOT USED FOR NAACL
    #processing="STEMMING, Euclidean Distance, num_cluster=200"   NOT USED FOR NAACL
    #POS="ALL"
    # clusterfile_euc=os.getcwd() + "/para_data/"+topic+"/cluster/Euc_Cluster_200"
    # stem_cluster(stringsFile,stem,stop,processing,POS,clusterfile_euc,num_cluster,remS,affinity)
    #processing="STEMMING, cosine Distance, num_cluster=200"
    #clusterfile_cosine=os.getcwd() + "/para_data/"+topic+"/cluster/Cos_Cluster_200_AVG_All"
    #stem_cluster(stringsFile,stem,stop,processing,POS,clusterfile_cosine,num_cluster,remS,affinity)
    #------------------------------------------------------- POS="Noun_Verb_AdJ"
    #----- processing="STEMMING, cosine Distance, num_cluster=50,Nouns_AdJ_Verb"
    # clusterfile_cosine=os.getcwd() + "/para_data/"+topic+"/cluster/Labels/Cos_Cluster_50_AVG_Noun_Adj_Verb"
    # stem_cluster(stringsFile,clusterfield,keyid,stem,stop,processing,POS,clusterfile_cosine,num_cluster,remS,affinity)
    
    
    
    # POS="Noun_AdJ"
    # processing="STEMMING, cos Distance, num_cluster=70Nouns_AdJ"
    # clusterfile_cosine=os.getcwd() + "/para_data/"+topic+"/cluster/LabelUpdated/TFIdf/Cos_Cluster_70_AVG_Noun_Ad"
    # clustercsv=os.getcwd() + "/para_data/"+topic+"/cluster/LabelUpdated/TFIdf/Cos_Cluster_70_AVG_Noun_Ad"
    # stem_cluster(stringsFile,clustercsv,vect,clusterfield,keyid,stem,stop,processing,POS,clusterfile_cosine,num_cluster,remS,affinity)
    #end===========================================================================NOT USED FOR NAACL
    
    
    