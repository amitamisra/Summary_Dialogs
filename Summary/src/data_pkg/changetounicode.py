'''
Created on Sep 30, 2014

@author: amita
'''
import FileHandling
import NewFormat_text
import os
def changeTexttounicode(InputDir):
    FileList=os.listdir(InputDir)
    for InputFile in FileList:
        if str(InputFile).startswith("."):
            continue
        Input=InputDir+"/"+InputFile
        NewLines=list()
        TextLines=FileHandling.ReadTextFile(Input)
        for text in TextLines:
            new_text=NewFormat_text.ascii_only(text)
            NewLines.append(new_text)
        Output=InputDir +"/"+  InputFile  
        FileHandling.WriteTextFile(Output[:-4], NewLines)    
    
    
if __name__ == '__main__':
    topic="gay-rights-debates"
    TaskNo=2
    InputDir=os.getcwd() +"/CSV/"+ topic+ "/MTdata/MT"+ str(TaskNo)+"/"+"MT"+str(TaskNo)+"Summaries/MT2_more750/Batch3_only_summary"
    changeTexttounicode(InputDir)