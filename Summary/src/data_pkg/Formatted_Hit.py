'''
Created on Jun 8, 2014
@author: amita
'''
import FileHandling
import os
import NewFormat_text
from collections import OrderedDict
#from nlp.text_obj import TextObj

class IndividualHits:
    def __init__(self,InHitMT,outputtextfile,Noofdialog_hit):
        self.input=InHitMT
        self.dialognos_hit=Noofdialog_hit
        self.outputtextfile=outputtextfile
        
    def CreateHitOutput(self):
        rowdicts=FileHandling.read_csv(self.input)
        Textline=""
        Textline= Textline + """<html><head></head><body>"""
        for row in rowdicts:
            num_dialog=0
            Textline=Textline +"<p><b>" +"Worker_Id" +"</p></b>"
            Textline=Textline+row["WorkerId"]
            Textline=Textline+"<p><b>" +"HIT_Id" +"</p></b>"
            Textline=Textline+row["HitId"]
            while num_dialog < self.dialognos_hit: 
                    Dialog=row["Input.key"+ str(num_dialog+1)]
                    Textline=Textline +"<p><b>"+"Dialog" + Dialog +"</p></b>"
                    Text_Summary=row["Answer.Dialog"+ str(num_dialog+1)+"_Summary"]
                    Text_Summary=NewFormat_text.ascii_only(Text_Summary)
                    Word_count= str(NewFormat_text.word_count(Text_Summary, removelist))
                    Textline=Textline +"<p><b>"+"Word_Count" + Word_count +"</p></b>"
                    Textline= Textline+"<p><b>"+"Summary" + str(num_dialog) +"</p></b>"
                    Textline= Textline + Text_Summary
                    num_dialog=num_dialog+1
                    
        Textline=Textline + """</body> </html>""" 
        FileHandling.writeHtml(self.outputtextfile, Textline)            


if __name__ == '__main__':
    topic="gun-control"
    InputCsv= os.getcwd()+ "/"+ topic +"/MTdata/MT1/Summary/MT1Results_1_more750"
    OutHTML=os.getcwd()+ "/"+ topic +"/MTdata/MT1/Summary/MT1Results_1_more750"
    directory=""
    removelist=[]
    Noofdialog_hit=3
    for fileid in os.listdir(directory):
        if not fileid.startswith('.') and fileid.endswith(".csv"):
           
            MThitobj= IndividualHits(directory+fileid[:-4],directory+fileid[:-4],Noofdialog_hit)
            MThitobj.CreateHitOutput()