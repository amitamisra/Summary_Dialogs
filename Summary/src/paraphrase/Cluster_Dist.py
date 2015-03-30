'''
Created on Sep 2, 2014

@author: amita
'''
import os
from data_pkg import FileHandling
import similarity
import numpy as np
from  sklearn.cluster import AgglomerativeClustering
class AggCluster_Dist:
    def __init__(self,StringsFile,DistanceFile,clusterfile_Agg,clustercsv,Error_Dist,num_cluster,clusterfield,affinity,keyid):
        self.StringsFile= StringsFile
        self.DistanceFile=DistanceFile
        self.OutclusterFile=clusterfile_Agg
        self.clustercsv=clustercsv
        self.num_cluster=num_cluster
        self.clusterdfield=clusterfield
        self.affinity=affinity
        self.keyid=keyid
        self.Error_Dist=Error_Dist

    def CreateDistanceMatrixFile(self):
        fileobj=file(self.DistanceFile,"wb")
        #=======================================================================
        # Allrow_dicts=FileHandling.read_csv(self.StringsFile)
        # Allstrings=[rowdict_str[self.clusterdfield] for rowdict_str in Allrow_dicts]
        #=======================================================================
        Allstrings=list()
        sim_tup=similarity.UMBC_dis_matrix(Allstrings) 
        Sim_Mat=sim_tup[0]
        Error_dicts=sim_tup[1]
        if Error_dicts:
            fieldnames=Error_dicts[0].keys()
            FileHandling.write_csv(self.Error_Dist, Error_dicts, fieldnames)
         
        np.save(fileobj,Sim_Mat)
        fileobj.close()
    def CreateCluster(self):
        Fileobj=file(self.DistanceFile,"rb")
        SimArray=np.load(self.DistanceFile)
        Fileobj.close()
        
        print SimArray
        AggClusterDistObj=AgglomerativeClustering(n_clusters=self.num_cluster,linkage='average',affinity=self.affinity) 
        Res_Labels=AggClusterDistObj.fit_predict(SimArray)
        print Res_Labels
         
        
        
        
if __name__ == '__main__':
    topic="gay-rights-debates"
    StringsFile=os.path.dirname(os.getcwd()) + "/data_pkg/CSV/"+ topic +"/MTdata/LabelUpdated/more2_Scus"
    clusterFile_Agg=os.getcwd() + "/para_data/"+topic+"/Dist_cluster/LabelUpdated/UMBC_Cluster"
    clustercsv=os.getcwd() + "/para_data/"+topic+"/Dist_cluster/LabelUpdated/UMBC_Cluster"
    DistanceFile=os.getcwd() + "/para_data/"+topic+"/Dist_cluster/LabelUpdated/UMBC_Dist"
    Error_Dist=os.getcwd() + "/para_data/"+topic+"/Dist_cluster/LabelUpdated/UMBC_Error"
    num_cluster=2
    clusterfield=clusterfield="label" #Field in input file for clustering
    keyid="key_user"
    affinity="precomputed"
    Aggcluster_dist=AggCluster_Dist(StringsFile,DistanceFile,clusterFile_Agg,clustercsv,Error_Dist,num_cluster,clusterfield,affinity,keyid)
    
    
    #Aggcluster_dist.CreateDistanceMatrixFile() 
    Aggcluster_dist.CreateCluster()
     
            
    pass