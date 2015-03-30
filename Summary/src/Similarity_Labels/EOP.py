from data_pkg import FileHandling

'''
Created on Oct 28, 2014
Take a json  input file created using EOP java module with 4 annotators overlapping 
@author: amita
'''
def JsonToCsv(InputJson,OutputCsv):
    FileHandling.convert_json_tocsv(InputJson, OutputCsv)
    
if __name__ == '__main__':
    import sys
    print sys.executable
    topic= "gay-rights-debates"
    InputJson="/Users/amita/git/summary_repo/Summary/src/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task2/ResultsV2/Overlap_Corre_4_MT1_MT2_Entail3.json"
    OutputCsv="/Users/amita/git/summary_repo/Summary/src/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task2/ResultsV2/Overlap_Corre_4_MT1_MT2_Entail3"
    JsonToCsv(InputJson,OutputCsv)