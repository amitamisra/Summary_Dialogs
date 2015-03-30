'''
Created on May 12, 2014
created a formatted html file from batch results, pay bonus gives the number of accepted hits in a batch by a worker
@author: amita
'''
import FileHandling
import os
import NewFormat_text
from collections import Counter
from collections import defaultdict
import sys
class FormattedResult:
    def __init__(self,InbatchMT,outputtextfile,Noofdialog_hit):
        self.input=InbatchMT
        self.dialognos_hit=Noofdialog_hit
        self.outputtextfile=outputtextfile
    def PayBonus(self):    
        rowdicts=FileHandling.read_csv(self.input)
        listworker_id=[row["WorkerId"] for row in rowdicts if row["AssignmentStatus"]=="Approved"]
        counter_worker_id=Counter(listworker_id)
        print counter_worker_id
        #if row["Status"]=="Submitted":
        if row["AssignmentStatus"]=="Submitted":
                print "WorkerId still submitted status" + row["WorkerId"]
                sys.exit(1)
        
    def CreateFormatBatchResult(self):
        dict_key=defaultdict(str)
        rowdicts=FileHandling.read_csv(self.input)
        Textline=""
        Textline= Textline+ """<html><head></head><body>"""
        for row in rowdicts:
            worker_id=row["WorkerId"]
            dict_key[worker_id]=dict_key[worker_id]+"<br><br><b>worker_id </b>" + worker_id+"<br>HITid:</b>  " + row["HITId"] \
                                +"<br> <b>Status:</b>" + row["AssignmentStatus"]
            
            for count in range(1,self.dialognos_hit+1):
                    key=row["Input.key"+str(count)]
                    #Answer=row["Answer.Dialog" + str(count) + "_Summary" ]
                    Answer=row["Answer.Dialog"+ str(count)+ "_Summary"  ]
                    new_text=(NewFormat_text.ascii_only(Answer)) 
                    dialog=row["Input.Dialogtext"+str(count)]
                    dialog_text=(NewFormat_text.ascii_only(dialog)) 
                    dict_key[worker_id]=dict_key[worker_id] +"<br><b> key:   </b>" + key + " <br><b> dialog_text:</b>" + dialog_text \
                                        +"<br>"+ "<b>Summary   " + "<br>Word_Count </b>" \
                                        + str(NewFormat_text.word_count(new_text, removelist)) +"<br>" + new_text 
                    
                    
                
            
        for key,value in dict_key.iteritems():
                            Textline="<p>"+ Textline + value + "</p>"    
                
                    
                        
                    
        Textline=Textline + """</body> </html>""" 
        FileHandling.writeHtml(self.outputtextfile, Textline)




#topic="gay-rights-debates"( already done that)
topic="gun-control"
directory =os.getcwd() + "/CSV/"+ topic+"/MTdata/MT1/MT1Results/MT1_midRange_Results/"
input_batchfile=directory+"MT1_midRange_Results"
outputtextfile=directory +"MT1_midRange_Results"
Noofdialogs_hit=3
removelist=[",",".","!","?"]

MTBatchobj=FormattedResult(input_batchfile,outputtextfile,Noofdialogs_hit)         
MTBatchobj.CreateFormatBatchResult()
MTBatchobj.PayBonus()

                
                
                
        
    

if __name__ == '__main__':
    pass