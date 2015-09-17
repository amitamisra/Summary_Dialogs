'''
Created on Apr 11, 2015

@author: amita
'''
import FileHandling

def splitcsv(inputcsv, outfolder,numtosplit):
    FileHandling.splitcsv(inputcsv, outfolder, numtosplit)

def json_to_csv(inputjson,outcsv):
    FileHandling.convert_json_tocsv(inputjson, outcsv)
    
def csvtojson(inputcsv,output):   
    listdict=FileHandling.read_csv(inputcsv)
    FileHandling.writejson(listdict, output)
if __name__ == '__main__':
    #inputjson= "/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/MTdata/Phase1/LabelUpdated/CoreNLPmore2_Scus.json"
    #outputcsv="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/MTdata/Phase1/LabelUpdated/CoreNLPmore2_Scus"
     
    #inputjson="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gun-control/MTdata/Phase1/Pyramids_Natural/CoreNLPmore2_Scus_EXT.json"
    #outputcsv="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gun-control/MTdata/Phase1/Pyramids_Natural/CoreNLPmore2_Scus_EXT"
    # inputcsv="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/MTdata/Phase1/LabelUpdated/more2_Scus"
    # outjson="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/MTdata/Phase1/LabelUpdated/more2_Scus"
    #----------------------------------------------- csvtojson(inputcsv,outjson)
#------------------------------------------------------------------------------ 
    
    # inputjson= "/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/MTdata/Phase1/LabelUpdated/CoreNLPDistExtmore2_Scus.json"
    # outputcsv="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/MTdata/Phase1/LabelUpdated/CoreNLPDistExtmore2_Scus"
    #----------------------------------- AddstanfordDetails(inputjson,outputcsv)
    # inputjson="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gun-control/MTdata/Phase1/Pyramids_Natural/CoreNLPDistExtmore2_Scus.json"
    # outputcsv="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gun-control/MTdata/Phase1/Pyramids_Natural/CoreNLPDistExtmore2_Scus"
    #----------------------------------- AddstanfordDetails(inputjson,outputcsv)
    
    
    #inputjson="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/MTdata/Phase1/LabelUpdated/CoreNLPmore2_Scus_Disamb_EXT.json"
    #outputcsv ="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/MTdata/Phase1/LabelUpdated/CoreNLPmore2_Scus_Disamb_EXT"
    #inputjson="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gun-control/MTdata/Phase1/Pyramids_Natural/more2_Scus_Disamb.json"
    #outputcsv="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gun-control/MTdata/Phase1/Pyramids_Natural/more2_Scus_Disamb_EXT"
    
    
    inputjson= "/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/MTdata/Phase1/LabelUpdated/more2_Scus_Disamb.json"
    outputcsv="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/MTdata/Phase1/LabelUpdated/more2_Scus_Disamb"
    
    inputjson="/Users/amita/git/FacetIdentification/data/dialog_data/CSV/gun-control/MTdata/Phase1/MTSummary/AllMTSummary_50/CoreNLPNaturalSummaryOneSumm.json"
    outputcsv="/Users/amita/git/FacetIdentification/data/dialog_data/CSV/gun-control/MTdata/Phase1/MTSummary/AllMTSummary_50/CoreNLPNaturalSummaryOneSumm"
     
    inputjson="/Users/amita/git/FacetIdentification/data/dialog_data/CSV/gun-control/MTdata/Phase1/MTSummary/AllMTSummary_50/Ext_DistCoreNLPNaturalSummaryOneSumm.json"    
    outputcsv="/Users/amita/git/FacetIdentification/data/dialog_data/CSV/gun-control/MTdata/Phase1/MTSummary/AllMTSummary_50/Ext_DistCoreNLPNaturalSummaryOneSumm"
    
    
    inputjson="/Users/amita/git/FacetIdentification/data/dialog_data/CSV/gun-control/MTdata/Phase1/MTSummary/AllMTSummary_50/CorefSimpSumm.json"
    outputcsv="/Users/amita/git/FacetIdentification/data/dialog_data/CSV/gun-control/MTdata/Phase1/MTSummary/AllMTSummary_50/CorefSimpSumm"
   
    inputjson="/Users/amita/git/FacetIdentification/data/dialog_data/CSV/gun-control/MTdata/Phase1/MTSummary/CorefReplacedSummary/AllMTSummary_50Replaced/CoreNLPRepCorefSimpSumm.json"
    outputcsv="/Users/amita/git/FacetIdentification/data/dialog_data/CSV/gun-control/MTdata/Phase1/MTSummary/CorefReplacedSummary/AllMTSummary_50Replaced/CoreNLPRepCorefSimpSumm"
       
    inputjson="/Users/amita/git/FacetIdentification/data/dialog_data/CSV/gun-control/MTdata/Phase1/Pyramids_Natural/Disammore2_Scus.json"
    outputcsv="/Users/amita/git/FacetIdentification/data/dialog_data/CSV/gun-control/MTdata/Phase1/Pyramids_Natural/Disammore2_Scus"
    
    inputcsv=" /Users/amita/git/FacetIdentification/data/SQL_data/Alltopicscv"
    outputjson="/Users/amita/git/FacetIdentification/data/SQL_data/Alltopicscv"
    
    json_to_csv(inputjson,outputcsv)
   
   
   
    