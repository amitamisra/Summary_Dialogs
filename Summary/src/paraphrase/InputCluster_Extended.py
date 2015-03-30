'''
Created on Aug 26, 2014
Takes input an extended json strings file created using DISCO.Each row is a sentence 
from summaries in ALLMT file.Input contains POS and also extended poS
@author: amita
'''

from sklearn.feature_extraction.text  import CountVectorizer
from  sklearn.cluster import AgglomerativeClustering
import preprocess_text
import os
import data_pkg.FileHandling
from sklearn import metrics
import operator
import itertools
from sklearn.metrics import pairwise_distances


class ExtendedCluster:
    def __init__(self,num_cluster,clusterfield,keyid,ExtStringsCsv,clusterfile,POS,affinity): 
        self.ExtStringCSv=ExtStringsCsv
        self.OutclusterFile=clusterfile
        self.num_cluster=num_cluster
        self.affinity=affinity
        self.POS=POS
        self.clusterdfield=clusterfield
        self.keyid=keyid
    
    
    def Create_Ext_Agg_cluster(self,stem,stop,processing,remS): 
         
        Allrow_dicts=data_pkg.FileHandling.read_csv(self.ExtStringCSv)
        Allstrings=list()
        #Allstrings=[rowdict_str["Text_original"] for rowdict_str in Allrow_dicts]
        for row_dict in Allrow_dicts:
            if self.POS =="ALL_EXT":
                Stringrow=row_dict["Text_original"]+row_dict["Adj_Extended"]+row_dict["Noun_Extended"] +row_dict["Verb_Extended"]
                Allstrings.append(Stringrow)
            else:
                Stringrow=row_dict["Adj"]+row_dict["Adj_Extended"]+row_dict["Noun"]+row_dict["Noun_Extended"]#+row_dict["Verb"]#+row_dict["Verb_Extended"]
                Allstrings.append(Stringrow)
                 
        Allstrings_process=[preprocess_text.preprocess(string_text, stem,stop) for string_text in Allstrings]  
         
        if remS:
            Allstrings_process=[preprocess_text.removeS(text) for text in Allstrings_process]            
        vectorizer = CountVectorizer()    
        term_doc=vectorizer.fit_transform(Allstrings_process)
        #-------------------------- feature_names=vectorizer.get_feature_names()
        #--z---------------------------------------------- Array=term_doc.toarray
         
        if self.affinity=='euclidean':
            Agg_cluster=AgglomerativeClustering(n_clusters=self.num_cluster,affinity='euclidean')
        if self.affinity=='cosine':
            Agg_cluster=AgglomerativeClustering(n_clusters=self.num_cluster,linkage='average',affinity='cosine')
        Res_Labels=Agg_cluster.fit_predict(term_doc.toarray())
        self.cluster_tup_list=self.tuple_Ext_cluster_doc(Res_Labels,Allstrings,Allrow_dicts)
        #term_doc_lsa = lsa.fit_transform(term_doc)
        print type (term_doc)
        self.metric=metrics.silhouette_score(term_doc.toarray(), Res_Labels, metric=self.affinity)
        print Res_Labels
        print("n_samples: %d, n_features: %d" % term_doc.shape) 
            
    
    def tuple_Ext_cluster_doc(self,Res_Labels,Allstrings,Allrow_dicts):
        doccount=0
        cluster_list=list() 
        for label in Res_Labels:
            row_cluster=dict()
            row_cluster["label"]=label
            row_cluster["doccount"]=doccount
            row_cluster["string"]=Allstrings[doccount]
            row_cluster["key"]=Allrow_dicts[doccount][self.keyid]
            row_cluster["Text_original"]=Allrow_dicts[doccount]["Text_original"]
            doccount=doccount+1
            cluster_list.append(row_cluster)   
        return cluster_list
    
    def  write_Ext_cluster(self,processing):
        AllList=list()
        self.cluster_tup_list.sort(key= operator.itemgetter("label"))
        AllList.append("PREPROCESSING :"+ processing)
        AllList.append("Metric"+ str(self.metric))
        count=0
        for key, items in itertools.groupby(self.cluster_tup_list, operator.itemgetter('label')):
            AllList.append("\n\n NEW CLUSTER  " + str(count)+"\n\n\n")
            OneCluster=list(items) 
            count=count+1
            for contrib in  OneCluster:
                #AllList.append("\n processed_string :" + contrib["string"] + "\n")
                AllList.append("key  "+contrib["key"] + "\n")
                AllList.append("\n\n"+ contrib["Text_original"] + "\n")
            
        
        data_pkg.FileHandling.WriteTextFile(self.OutclusterFile,AllList)
            
def createExCluster(ExtstringsFile,clusterfield,keyid,stem,stop,processing,POS,clusterfile,num_cluster,remS,measure,):
        
        
        ExtClusterobj=ExtendedCluster(num_cluster,clusterfield,keyid,
                                      ExtstringsFile,clusterfile,POS,measure)
        ExtClusterobj.Create_Ext_Agg_cluster(stem,stop,processing,remS)
        ExtClusterobj.write_Ext_cluster(processing)
    
if __name__ == '__main__':
    topic="gay-rights-debates"
    
    stem=True 
    stop=True
    num_cluster=70
    remS=True 
    choice=2 
    if choice ==1:
        #To be done with summaries as input
        clusterfield="text" #Field in input file for clustering
        keyid="key"
        stringsFile=os.getcwd() + "/para_data/"+topic+"/cluster/Extended_3/Summaries/PosExtendedStrings.txt"
        PosStringsFileCsv=os.getcwd() + "/para_data/"+topic+"/cluster/Extended_3/Summaries/PosExtendedStrings"
        clusterdir=os.getcwd() + "/para_data/"+topic+"/cluster/Extended_3/Summaries/"
        data_pkg.FileHandling.convert_json_tocsv(stringsFile, PosStringsFileCsv)
        
    else:
        if choice ==2:
            #To be done with labels as input
            clusterfield="label" #Field in input file for clustering
            keyid="key"
            clusterdir=os.getcwd() + "/para_data/"+topic+"/cluster/Extended_3/LabelUpdated/"
            stringsFile=os.getcwd() + "/para_data/"+topic +"/cluster/Extended_3/LabelUpdated/PosExtLabelUp.txt"
            PosStringsFileCsv=os.getcwd() + "/para_data/"+topic+"/cluster/Extended_3/LabelUpdated/ExtPOS_LabelUp"
            data_pkg.FileHandling.convert_json_tocsv(stringsFile,PosStringsFileCsv)
            
    
    
    
    
    
    
    
    
    #POS="ALL_EXT"
    #clusterfile_cosine=clusterdir+ "Cos_Cluster_70_AVGAllEx"
    #processing="STEMMING, remove stop words cosine Distance, num_cluster=70,NAll EXt removed s1 s2"
    
    
    
    POS="Noun Adj"
    processing="STEMMING, remove stop words cosine Distance, num_cluster=70,Nouns_adj+ Extend Nouns_AdJ,removed s1 s2"
    clusterfile_cosine=clusterdir+ "Cos_Cluster_70_AVGNounADj_extNoun_Adj"

    
    createExCluster(PosStringsFileCsv,clusterfield,keyid,stem,stop,processing,POS,clusterfile_cosine,num_cluster,remS,measure="cosine")
    

