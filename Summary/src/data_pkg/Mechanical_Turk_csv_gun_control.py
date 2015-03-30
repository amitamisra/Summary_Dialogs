# encoding=utf8  


'''
Created on May 1, 2014

@author: amita
'''
import FileHandling
from unidecode import unidecode
import NewFormat_text
from nlp.text_obj import TextObj
import MySQLdb as mdb
import sys
reload(sys)
import os
import re
from html import HTML


def MT1discussion_turns(taskno):
    
    fieldnames=list()
    rowdict=dict()
    rows=list()
    rowdict["49dialog"]="1"   
    rowdict["173dialog"]="1,2" 
    rowdict["342dialog"]="1"
    rowdict["483dialog"]="1" 
    rowdict["534dialog"]="1" 
    rowdict["546dialog"]="1,2,3" 
    rowdict["623dialog"]="1" 
    rowdict["662dialog"]="1" 
    rowdict["670dialog"]="1"
    rowdict["671dialog"]="1"
    rowdict["682dialog"]="1"
    rowdict["690dialog"]="1" # select the first dialogue from the file as 2 dialogues with same authors have same no of turns
    rowdict["737dialog"]="1" # select the first dialogue as it has more turns
    rowdict["751dialog"]="1"
    rowdict["764dialog"]="1,2,3" #select the  dialogue3  as it comes before dialogue 4 both have same authors and same number of turns
    rowdict["817dialog"]="1"
    rowdict["1073dialog"]="1"
    rowdict["1084dialog"]="1"
    rowdict["1103dialog"]="1"
    rowdict["1116dialog"]="1"
    rowdict["1121dialog"]="1"
    rowdict["1131dialog"]="1,4,6"
    rowdict["1134dialog"]="1"
    rowdict["1185dialog"]="1"
    #rowdict["1543dialog"]="1"  move to MT2
    rowdict["3320dialog"]="1,2"
   
    
    rowdict["dataset"]="forums"
    rowdict["topic"]=topic
    for k,v in  rowdict.iteritems():
        fieldnames.append(k)
    
    if not os.path.exists(directory):
                os.makedirs(directory)   
    rows.append(rowdict)
    outputfile=MTdirectory+ "MT" + str(taskno)+"_discussion_turns"
    FileHandling.write_csv(outputfile, rows, fieldnames)
    


class Mechanical_Turk:
    def __init__(self,InputcsvStr,dialogturns):
        
        self.inputcsvStr=InputcsvStr
        self.dialogturns=dialogturns

     
    
    
    def SqlAuthorList(self):
        try:
            db1 = mdb.connect(host="localhost",user="root",passwd="",db="iac")
            cursor = db1.cursor(mdb.cursors.DictCursor) 
            Query_Author="select username from authors where dataset_id=1"
            cursor.execute(Query_Author) 
            rows=cursor.fetchall()
            rows=list(rows)
            Authorlist=[row['username'] for row in rows]
            return Authorlist
        except db1.Error, e:
            print e
            if db1:
                db1.rollback()
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
            
            
            
    def formatascii(self,string):    
        removetokenlist="emoticon"
        #string=str(Htmltext)
        text_obj = TextObj(string)
        #text=text_obj.text
        tokens=text_obj.tokens
        tokens=NewFormat_text.removetokens(tokens,removetokenlist) 
        new_text=" ".join(tokens)
        new_text=new_text.decode('utf-8', 'ignore')
        return(NewFormat_text.ascii_only(new_text))   
             
    
    def createdialoginputfile(self,inputcsvStr,dialogturns,AllDialogs_more750,AllDialogs_midrange,AlltextAllFiles):
        try:
                global Textline_750
                global Textline_Mid
                rows=list()
                rowdicts=FileHandling.read_csv(self.inputcsvStr)
              
                for turn in self.dialogturns:
                    
                        rows = [row for row in rowdicts if row['Dialog_Turn'] == str(turn)]
                        Dialogrow=dict()
                        Htmltext=HTML()
                        Dialogrow["Dialogtext"]=""
                        first=True
                        count=1 
                        turnno=1
                        number_turns=len(rows)
                        #if number_turns < 14:
                        for row in rows:
                            
                            row["Fullquote_text"]= self.formatascii(row["Fullquote_text"])
                            row["post_text"]=self.formatascii(row["post_text"])
                            
                            if (first==True):
                               
                                Htmltext.p("S1:" + str(turnno)+ row["Fullquote_text"])
                                
                                Dialogrow["Dialogtext"]=(Dialogrow["Dialogtext"])+ "<br><b>"+"S1:"+ \
                                            str(turnno)+"-  "+'</b>'+ (row["Fullquote_text"])
                                len_key=len(row["key"])
                                Dialogrow["key"]=row["key"][:len_key-1]            
                                
                                Dialogrow["Dialogtext"]= Dialogrow["Dialogtext"]+"<br><b> S2:"+\
                                            str(turnno)+"-  </b>"+(row["post_text"])
                                           
                                Htmltext.p("S2:" + str(turnno)+ row["post_text"])            
                                first=False
                                turnno=turnno+1
                            else:
                                if count==1:
                                    Dialogrow["Dialogtext"]=Dialogrow["Dialogtext"]+" <br><b>S1:"+ \
                                            str(turnno)+"-  </b>"+(row["post_text"]) 
                                    Htmltext.p("S1:" + str(turnno)+ row["post_text"])        
                                    
                                    Dialogrow["key"]= Dialogrow["key"]+"_"+ str(row["posts_post_id"])      
                                    count=2
                                else:
                                    if count==2:
                                        Dialogrow["Dialogtext"]=Dialogrow["Dialogtext"]+"<br><b> S2:"+str(turnno)+"-  </b>"+(row["post_text"] )
                                        Dialogrow["key"]= Dialogrow["key"]+"_"+str(row["posts_post_id"]) 
                                        Htmltext.p("S2:" + str(turnno)+ row["post_text"])    
                                        count=1
                                        turnno=turnno+1
                        
                       
                        
                        
                        
                        
                        Dialogrow["key"]= Dialogrow["key"]+"_"+ str(turn)  
                        text_obj = TextObj(Dialogrow["Dialogtext"])
                        #text=text_obj.text
                        tokens=text_obj.tokens
                        #string=unicode(Dialogrow["Dialogtext"],errors="ignore")
                        word_count=len(tokens)
                        Dialogrow["Total_Count"]=word_count
                        if word_count >= 750:
                            Textline_750= Textline_750 + "<p><b> KEY:</b>"+str(Dialogrow["key"]) + str(Dialogrow["Dialogtext"]) + "</p>"
                       
                        
                        #print Dialogrow["key"]
                        if word_count < 1500:
                            if word_count >= 750:  
                                AllDialogs_more750.append(Dialogrow)
                            else:    
                                #===============================================
                                # if word_count <=500 :
                                #     AllDialogs_less500.append(Dialogrow)
                                # else:    
                                #===============================================
                                        Textline_Mid= Textline_Mid + "<p><b> KEY:</b>"+str(Dialogrow["key"]) + str(Dialogrow["Dialogtext"]) + "</p>"
                                        AllDialogs_midrange.append(Dialogrow)        
                            AlltextAllFiles.append(Dialogrow["Dialogtext"])
                        else:
                            print "word count > 1500  " + str(Dialogrow["key"])
        except : 
            print " error in file" + self.inputcsvStr
            
            sys.exit(1)         
    
    def createhitinput(self,outputcsv,No_ofitem,No_ofhits):
        MTrow=dict()
        
        Fieldnames=list()
        MTRows=list()
        rowdicts=FileHandling.read_csv(self.inputcsvStr) 
        intc=1
        extc=0
        first=True
        for row in rowdicts:
            if extc < No_ofhits:  
                
                if intc<=No_ofitem:
                
                    MTrow["key" +str(intc)]=row["key"]
                    MTrow["Dialogtext"+str(intc)]=row["Dialogtext"]                    
                    if first:
                        Fieldnames.append("key" +str(intc))
                        Fieldnames.append("Dialogtext"+str(intc))
                    intc=intc+1       
                                         
                if intc-1==No_ofitem:
                    MTRows.append(MTrow)   
                    extc=extc+1
                    intc=1
                    MTrow=dict()
                    first=False 
                    
            else:
                break
                
        FileHandling.write_csv(outputcsv, MTRows, Fieldnames)            




    
      



 
           
if __name__ == '__main__':
    FileStr=dict()
    topic="gun-control"
    taskno=1
    directory=os.getcwd() + "/CSV/"+ topic+"/discussion_dialogs/"
    MTdirectory=os.getcwd() + "/CSV/"+ topic+"/MTdata/MT"+ str(taskno)+"/"
    outputcsvdialog=MTdirectory +"Dialog_File"
    
    outputMT1=MTdirectory+"MT" +str(taskno)+"_more750"
    outputMT3=MTdirectory+"MT"+str(taskno)+"_midrange"
    
    outputHT_750=MTdirectory+"MT" +str(taskno)+"_more750"
    outputHT_Mid=MTdirectory+"MT" +str(taskno)+"_Mid"
    
    MTfile=MTdirectory+"MT"+str(taskno)+"_discussion_turns"
    
    fieldnames=list()
    AlltextAllFiles=list()
    Alldialogs_more750=list()
    Alldialogs_midrange=list()
    
    global Textline_750
    global Textline_Mid
    Textline_750=""
    Textline_Mid=""
    No_ofitem=3
    
    fieldnames.append("Dialogtext")
    fieldnames.append("key")
    fieldnames.append("Total_Count")
    MT1discussion_turns(taskno) ## call this once for each MT task

    #MT2discussion_turns(taskno)
    
    #MT3discussion_turns(taskno)
    
    
    MTrow=FileHandling.read_csv(MTfile)
    FileStr=MTrow[0]
    
    
    
    outputtextfile=MTdirectory +"dialog_text"
    for k,v in FileStr.iteritems():
        if "dialog" in k:
            inputfile=directory+k
            inputdialogturns=[s for s in re.split('[\s,]+',v)]
            MTobject= Mechanical_Turk(inputfile,inputdialogturns)
            MTobject.createdialoginputfile(inputfile, inputdialogturns, Alldialogs_more750,Alldialogs_midrange,AlltextAllFiles)
    FileHandling.WriteTextFile(outputtextfile,AlltextAllFiles)
    inputdialogturns=""
    
    FileHandling.write_csv(outputcsvdialog+"_more750",Alldialogs_more750, fieldnames)
    MTobject1=Mechanical_Turk(outputcsvdialog+"_more750",inputdialogturns)

 
    FileHandling.write_csv(outputcsvdialog+"_midrange",Alldialogs_midrange, fieldnames)
    MTobject3=Mechanical_Turk(outputcsvdialog+"_midrange",inputdialogturns)
 
    FileHandling.writeHtml(outputHT_750, Textline_750)
    FileHandling.writeHtml(outputHT_Mid, Textline_Mid)
    
    No_ofhits=4
    MTobject1.createhitinput(outputMT1,No_ofitem,No_ofhits)
    
    No_ofhits=7
    MTobject3.createhitinput(outputMT3,No_ofitem,No_ofhits)
