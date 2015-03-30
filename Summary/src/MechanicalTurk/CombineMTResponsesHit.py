
'''
Created on Oct 27, 2014

@author: amita
'''
import os
from data_pkg import FileHandling
class combineHitResponses:
    def __init__(self,input,output):
        self.input=input
        self.output=output
        
    def ReadInput(self):   
        InputRows= FileHandling.read_csv(self.input) 
        return InputRows
    
    def FindAllResponseHit(self,InputRows):
        for row in InputRows:
            



topic="gay-rights-debates"
inputfile=os.getcwd() + "/"+ topic +"/MTdata_cluster/Labels_Updated/MT_task2/ResultsV2/MT2_AllResults_hits_Batch"
outputfile=os.getcwd() + "/"+ topic +"/MTdata_cluster/Labels_Updated/MT_task2/ResultsV2/MT2_AllResults_hits_Batch"
if __name__ == '__main__':
    pass

