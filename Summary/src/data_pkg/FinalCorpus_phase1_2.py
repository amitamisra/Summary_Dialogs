'''
Created on Aug 19, 2014
This File creates  takes input files as dialog and summaries(which pyramid annotations are done in Phase1( LabelsUpdated, used for NAACL AFS task) and Phase2 and combined, )
,formats them removes extra whitespaces  and newlines.

@author: amita
'''
import os
import FileHandling
import NewFormat_text




def Formatsummary(infile,outfile,formatcolumn):
    inrows=FileHandling.read_csv(infile)
    keys= inrows[0].keys()
    AllRows=list()
    for row in inrows:
        newrow=dict()
        for key in keys:
            if key not in formatcolumn:
                newrow[key]=row[key]
            else:
                text=row[key]
                newtext=NewFormat_text.correctPunct(text)
                newtext=newtext.strip(' \t\n\r')
                newrow[key]=newtext
        AllRows.append(newrow) 
    fieldnames=AllRows[0].keys()
    FileHandling.write_csv(outfile, AllRows, fieldnames) 
    FileHandling.writejson(AllRows, outfile)              
                
                
                
                
def execute(infile_1,infile_2,infile_1_2,outfile_1,outfile_2,outfile_1_2,formatcolumn):  
    Formatsummary(infile_1,outfile_1,formatcolumn) 
    Formatsummary(infile_2,outfile_2,formatcolumn) 
    Formatsummary(infile_1_2,outfile_1_2,formatcolumn) 
         
    

if __name__ == '__main__':
    topic="gay-rights-debates"
    formatcolumn=["Dialog", "Summary"]
    infile_1=os.getcwd() + "/CSV/"+ topic+"/MTdata/MTPhase1/LabelUpdated/AllDialogs_Summ_MT_Label_updated"
    infile_2=os.getcwd() + "/CSV/"+ topic+"/MTdata/MTPhase2/AllDialogs_Summ_MT_phase2"
    infile_1_2=os.getcwd() + "/CSV/"+ topic+"/MTdata/AllDialogs_MT_phase_1_2"
    
    outfile_1=os.getcwd() + "/CSV/"+ topic+"/MTdata/MTPhase1/LabelUpdated/AllDialogs_phase1_Formatted"
    outfile_2=os.getcwd() + "/CSV/"+ topic+"/MTdata/MTPhase2/AllDialogs_phase2_Formatted"
    outfile_1_2=os.getcwd() + "/CSV/"+ topic+"/MTdata/AllDialogs_phase_1_2_Formatted"
    execute(infile_1,infile_2,infile_1_2,outfile_1,outfile_2,outfile_1_2,formatcolumn) 
    
