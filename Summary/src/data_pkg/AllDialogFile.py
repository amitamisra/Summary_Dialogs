'''
Created on Aug 19, 2014
This File creates dialog and summary file from all csv files 
put on Mechanical Turk and for which pyramid annotations are done in Phase1( LabelsUpdated, used for NAACL AFS task) and Phase2 and combined, removes HTML tags
@author: amita
'''
import os
import FileHandling
from bs4 import BeautifulSoup
import NewFormat_text
def function(rowkey):
    return  str(rowkey).startswith("key")

def AllsummaryAllMT(MTDir):
    MT2_Mid=MTDir+"MT2/MT2Summaries/MT2_midrange/"
    MT2_750=MTDir+"MT2/MT2Summaries/MT2_more750/combined_Summary"
    MT3_Mid=MTDir+"MT3/MT3Summaries/MT3_midRange_Summary"
    MT3_750=MTDir+"MT3/MT3Summaries/MT3_more750_Summary"
    LinesDict=list()
    AllSummList=[MT2_Mid,MT2_750,MT3_Mid,MT3_750]
    for MT in AllSummList:
        keys=os.listdir(MT)
        for keyfilename in keys:
            row=dict()
            row["key"]=keyfilename[:-4]
            row["Summary"]=" ".join(FileHandling.ReadTextFile(MT+"/"+ keyfilename))
            LinesDict.append(row)
            
    return LinesDict

def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] in value:
            return i
    return -1
def Adddialog(directory,tasks,lengthtasks,outfile_1,outfile_2,outfile_1_2,AllPyramid):
    AllSummaryList=AllsummaryAllMT(directory)
    Alldialogs_2=[]
    Alldialogs_1=[]
    fieldnames=["key","Dialog","Summary"]
    HtmlLines_1=list()
    HtmlLines_2=list()
    keys=os.listdir(AllPyramid)
    for task in tasks:
        for len_task in lengthtasks:
            InputFile= directory +"MT" + task +"/" + "MT" + task +"_" + len_task
            rowdicts=FileHandling.read_csv(InputFile)
            rowkeys=rowdicts[0].keys()
            keylist=filter(function, rowkeys)
            for row in rowdicts:
                for Filekey in keylist:
                    rowdict_1=dict()
                    if task == str("3") and "1-5811_33_29__35_38_40_41_43_2"  in row[Filekey]:# is also present in MT2_more750
                        continue 
                    #if "1-1281_466_275__483_561_576_625_633_1" in row[Filekey]: # used for Sample MT2
                     #   continue
                    #if "1-2583_199_195__201_202_207_212_215_233_234_235_2" in row[Filekey]:# used for Test MT2
                     #   continue

                        
                    found = any( row[Filekey] in x for x in keys)
                    if found:
                            index_1=find(AllSummaryList,"key",row[Filekey])
                            rowdict_1["key"]=row[Filekey]
                            dialog_1=row["Dialogtext" +str(Filekey[-1])]
                            soup = BeautifulSoup(dialog_1)
                            text_1= soup.get_text()
                            new_text_1=(NewFormat_text.ascii_only(text_1))
                            rowdict_1["Dialog"]=new_text_1
                            rowdict_1["Summary"]=AllSummaryList[index_1]["Summary"]
                            if rowdict_1 not in Alldialogs_1:
                                Alldialogs_1.append(rowdict_1)
                                HtmlLines_1.append("<br><br><b>Key</b><br>")
                                HtmlLines_1.append(row[Filekey])
                                HtmlLines_1.append("<br><b>Dialog</b>")
                                HtmlLines_1.append(dialog_1)
                                HtmlLines_1.append("<br><br><b>Summaries</b><br>")
                                HtmlLines_1.append(AllSummaryList[index_1]["Summary"])
                            
                    else:
                        index_2=find(AllSummaryList,"key",row[Filekey])
                        rowdict_2=dict()
                        rowdict_2["key"]=row[Filekey]
                        dialog_2=row["Dialogtext" +str(Filekey[-1])]
                        soup_2 = BeautifulSoup(dialog_2)
                        text_2= soup_2.get_text()
                        new_text_2=(NewFormat_text.ascii_only(text_2))
                        rowdict_2["Dialog"]=new_text_2
                        rowdict_2["Summary"]=AllSummaryList[index_2]["Summary"]
                        if rowdict_2 not in Alldialogs_2:
                            Alldialogs_2.append(rowdict_2)
                            HtmlLines_2.append("<br><br><b>Key</b><br>")
                            HtmlLines_2.append(row[Filekey]) 
                            HtmlLines_2.append("<br><b>Dialog</b>")
                            HtmlLines_2.append(dialog_2)
                            HtmlLines_2.append("<br><br><b>Summaries</b><br>")
                            HtmlLines_2.append(AllSummaryList[index_2]["Summary"])
                                 
    HtmlLines_1_str=" ".join(HtmlLines_1)
    HtmlLines_2_str=" ".join(HtmlLines_2)
    
    Alldialogs_1_2=Alldialogs_1+Alldialogs_2  
    HtmlLines_1_2_str= HtmlLines_1_str+HtmlLines_2_str             
    FileHandling.write_csv(outfile_1,Alldialogs_1, fieldnames)
    FileHandling.writeHtml(outfile_1, HtmlLines_1_str)

    FileHandling.write_csv(outfile_2,Alldialogs_2, fieldnames)
    FileHandling.writeHtml(outfile_2, HtmlLines_2_str)
    
    FileHandling.write_csv(outfile_1_2,Alldialogs_1_2, fieldnames) 
    FileHandling.writeHtml(outfile_1_2, HtmlLines_1_2_str) 
    
         
            






if __name__ == '__main__':
    topic="gay-rights-debates"
    directory=os.getcwd() + "/CSV/"+ topic+"/MTdata/"
    tasks=["2","3"]
    lengthtasks=["midrange","more750"]
    AllPyramid=os.getcwd() +"/CSV/"+ topic +"/MTdata/MTPhase1/LabelUpdated/Allpyramids_v1_labels_updated"
    outfile_1=os.getcwd() + "/CSV/"+ topic+"/MTdata/MTPhase1/LabelUpdated/AllDialogs_Summ_MT_Label_updated"
    outfile_2=os.getcwd() + "/CSV/"+ topic+"/MTdata/MTPhase2/AllDialogs_Summ_MT_phase2"
    outfile_1_2=os.getcwd() + "/CSV/"+ topic+"/MTdata/AllDialogs_MT_phase_1_2"
    
    Adddialog(directory,tasks,lengthtasks,outfile_1,outfile_2,outfile_1_2,AllPyramid)