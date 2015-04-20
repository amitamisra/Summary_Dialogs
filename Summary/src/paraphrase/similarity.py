'''
Created on Aug 9, 2014
Rhis program takes an input as two SCUs from balanced pairs file and computes similarity between them
@author: amita
only used sss function from this file in naacl 2015
'''
from data_pkg import FileHandling
from requests import get
import os
from paraphrase import Features_old
import numpy as np

    
def UMBC_similarity(BalancedPairsDir):
    fieldnames=["umbc_sim","label"]
    umbc_allrows=list()
    FileList = os.listdir(BalancedPairsDir)
    OutDir=os.path.dirname(BalancedPairsDir) +"/" +"UMBCSimPairs"
    if not (os.path.exists(OutDir)):
        os.makedirs(OutDir)
    for InpFile in FileList :
        rowdicts=FileHandling.read_csv(BalancedPairsDir +"/"+InpFile[:-4])
        for row in rowdicts:
            umbc_row=dict()
            s1=row["SCU1"]
            s2=row["SCU2"]
            #print type(s1)
            s1=Features_old.removeS(s1)
            s2=Features_old.removeS(s2)
            type_sim='relation'
            corpus='webbase'
            sim= sss(s1,s2,type_sim,corpus)
            umbc_row["umbc_sim"]=sim
            umbc_row["label"]=row["label"]
            umbc_allrows.append(umbc_row)
            
    outfile= OutDir+"/" + "AllScus" 
    FileHandling.write_csv(outfile, umbc_allrows, fieldnames)  
        
    



def sss(s1, s2, type_sim='relation', corpus='webbase'):
    sss_url = "http://swoogle.umbc.edu/SimService/GetSimilarity"
    try:
        response = get(sss_url, params={'operation':'api','phrase1':s1,'phrase2':s2,'type':type,'corpus':corpus})
        return float(response.text.strip())
    except:
        print 'Error in getting similarity for %s: %s' % ((s1,s2), response)
        return -1


def UMBC_dis_matrix(Allstrings):
        Allstrings.append("heterosexual male with a girlfriend would not receive his healthcare benefits")
        Allstrings.append("gay marriage laws would not affect marriage for anyone")
        Allstrings.append("redefining marriage does not hurt anyone")
        Allstrings.append("Right Wing was against both gay marriage and polygamy while the left wing was for it")
        Allstrings.append("federal recognition of gay marriage will be soon coming")
        Allstrings.append("there was no gay lifestyle to be prejudiced against")
        Allstrings.append("Free to be gay as long as they weren't openly gay")
        Allstrings.append("Anti-gay marriage supporters will support civil unions in lieu of gay marriage")
        Allstrings.append("once brought to a public vote, marriage equality will not be passed")
        Allstrings.append("Legally, it is complicated to legalize gay marriage in all states")
        Allstrings.append("Constitutional right to be opposed to gay marriage as well as gay people themselves")
        Allstrings.append("marriage should be between a heterosexual couple")
        
        type_sim='relation'
        corpus='webbase'
        length=len(Allstrings)
        Sim=np.zeros((length, length))
        i=0
        j=0
        listdict=list()
        
        for i in range(0,length):
            for j in range(i,length):
                if i==j:
                    Sim[i][j]=1
                else:    
                    S1=Allstrings[i]
                    S2=Allstrings[j]
                    
                    Sim[i][j]=sss(S1, S2, type_sim, corpus)
                    if Sim[i][j]==-1:
                        errdict=dict()
                        errdict["S1"]=S1
                        errdict["S2"]=S2
                        errdict["row"]=i
                        errdict["col"]=j
                        (S1,S2,i,j)
                        listdict.append(errdict)
                
        Sim=Sim+ Sim.T - np.diag(Sim.diagonal())
        print(str(type(Sim)))
        print (Sim.shape)
        return (Sim,listdict)   
        
        
        
        

if __name__ == '__main__':
    topic="gay-rights-debates"
    
    s1="offending the sensibilities of people does not constitute harm"
    s2="offending the sensibilities of people is harm"
    s3="harming others by offending their sensibilities "
    s4="towards the rights of gay people"
    s5="people in support of marriage equality is growing"
    s6a="heterosexual nature of the relationship that is important, not how the children are conceived within the relationship"
    s6b="marriage should be between a heterosexual couple"
    s7a="inappropriate to label disagreement on gay marriage as bigotry"
    s7b="funny how violence is used to end an argument against religion"
    s8a="gay community is the cause of the AIDs epidemic in the US."
    s8b="No one argues the point that AIDs was spread in the United States by homosexuals."
    sim1=sss(s1,s2)
    sim2=sss(s1,s3)
    sim3=sss(s2,s3)
    sim6=sss(s6a,s6b)
    sim7=sss(s7a,s7b)
    sim8=sss(s8a,s8b)
    print "sim6= "+ str(sim6)
    print "sim7= "+ str(sim7)
    print "sim8= "+ str(sim8)
    #print "sim4= "+ str(sim4)
    #===========================================================================
    # sim1= 0.8403531
    #sim2= 0.5883513
    #sim3= 0.7325452
    #sim4= 0.42750984
    #===========================================================================
    #------------------------------------------------ topic="gay-rights-debates"
    #------ BalancedPairsDir=os.getcwd()+ "/data_pkg/"+ topic +"/Balanced_Pairs"
    #----------------------------------------- UMBC_similarity(BalancedPairsDir)
    Allstrings=list()
    simtextfile=os.getcwd() + "/para_data/"+topic+"/cluster/LabelUpdated/TFIdf/checkumbc"
    ErrorFile=os.getcwd() + "/para_data/"+topic+"/cluster/LabelUpdated/TFIdf/Error_checkumbc"
    fieldnames=["S1","S2","row","col"]
    
    Sim_Error= UMBC_dis_matrix(Allstrings)
    np.savetxt(simtextfile, Sim_Error[0],fmt='%-7.3f')
    FileHandling.write_csv(ErrorFile, Sim_Error[1], fieldnames)
        
    