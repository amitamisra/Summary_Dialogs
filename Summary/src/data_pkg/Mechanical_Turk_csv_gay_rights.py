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
    rowdict["35dialog"]="1"   # moved to MT3
    rowdict["788dialog"]="1,2" # moved to MT3
    rowdict["1281dialog"]="1,2,3,5" # dialog1 is sample for MT2,5 moved to MT2, # 2,3,5 moved to MT3
    rowdict["1875dialog"]="1,2" # moved to MT3
    rowdict["2583dialog"]="1,2" # dialog2 is Sample test for MT2 , # 2 moved to MT3
    rowdict["3358dialog"]="1" # moved to Mt3
    rowdict["3124dialog"]="1" # moved to MT3
    rowdict["3134dialog"]="1" #moved to Mt3
    rowdict["4350dialog"]="1"#moved to MT2
    rowdict["dataset"]="forums"
    rowdict["topic"]=topic
    for k,v in  rowdict.iteritems():
        fieldnames.append(k)
    
    if not os.path.exists(directory):
                os.makedirs(directory)   
    rows.append(rowdict)
    outputfile=MTdirectory+ "MT" + str(taskno)+"_discussion_turns"
    FileHandling.write_csv(outputfile, rows, fieldnames)
    
        
def MT2discussion_turns(taskno):
    
    fieldnames=list()
    rowdict=dict()
    rows=list()
   
    rowdict["1281dialog"]="5" #moved to Mt3
    rowdict["4350dialog"]="1"
    rowdict["5176dialog"]="1"
    rowdict["5320dialog"]="1" #moved to Mt3
    rowdict["5342dialog"]="1" 
    rowdict["5670dialog"]="2"
    rowdict["5672dialog"]="1,2" #moved to Mt3
    rowdict["5811dialog"]="1,2" #2 #moved to Mt3
    rowdict["6124dialog"]="1"
    rowdict["6229dialog"]="2,3"
    rowdict["6319dialog"]="2,3" #2 moved to Mt3
    rowdict["6331dialog"]="1"
    rowdict["8171dialog"]="1,2"
    rowdict["8228dialog"]="1"  #moved to Mt3
    rowdict["6646dialog"]="1,2,6,11,13" 
    rowdict["6949dialog"]="1"
    rowdict["7185dialog"]="1" #moved to Mt3
    rowdict["7858dialog"]="1"
    rowdict["8376dialog"]="1"
    rowdict["8834dialog"]="1"
    rowdict["9331dialog"]="1,2,3"
    rowdict["9522dialog"]="1"
    rowdict["9745dialog"]="1"
    rowdict["9989dialog"]="1,2,3,4" #1,3moved to Mt3
    rowdict["10073dialog"]="1,2,4,6" #moved to Mt3
    #rowdict["10349dialog"]="1,2"   moved to Mt3
    
    
    rowdict["dataset"]="forums"
    rowdict["topic"]=topic
    for k,v in  rowdict.iteritems():
        fieldnames.append(k)
    
    if not os.path.exists(directory):
                os.makedirs(directory)   
    rows.append(rowdict)
    outputfile=MTdirectory+ "MT" + str(taskno)+"_discussion_turns"
    FileHandling.write_csv(outputfile, rows, fieldnames)



def MT3discussion_turns(taskno):
    fieldnames=list()
    rowdict=dict()
    rows=list()
    rowdict["35dialog"]="1"
    rowdict["788dialog"]="1,2" 
    rowdict["1281dialog"]="1,2,3,4,6,11,12" 
    rowdict["1875dialog"]="1,2" 
    rowdict["2280dialog"]="1" 
    rowdict["2583dialog"]="1,3"#,4"  useless
    rowdict["2844dialog"]="1,2" 
    rowdict["3089dialog"]="1" 
    rowdict["3124dialog"]="1" 
    rowdict["3134dialog"]="1"#,2 useless
    rowdict["3358dialog"]="1"
    
    
    rowdict["5320dialog"]="1"
    rowdict["5672dialog"]="1,2"   
    rowdict["5811dialog"]="2"
    #rowdict["6151dialog"]="1"  useless
    rowdict["6319dialog"]="2"
    rowdict["6646dialog"]="3,7,8,10" # 9 was useless hence selected 10
    rowdict["6493dialog"]="2" #1useless
    rowdict["7185dialog"]="1,3"
    rowdict["9391dialog"]="1,2,4,6,8,9,11,12,13,14,21"     
    rowdict["9989dialog"]="1"  # ,3 is useless
    rowdict["9390dialog"]="1" 
    rowdict["10354dialog"]="1"
    rowdict["10585dialog"]="1"
    rowdict["10824dialog"]="1"
    rowdict["10951dialog"]="1,2,3" 
    rowdict["10978dialog"]="2" #1,3 useless
    rowdict["10073dialog"]="1,2,4,6"
    rowdict["10349dialog"]="1,4"# 2 had less data_pkg , 4 had more
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
             
    
    def createdialoginputfile(self,inputcsvStr,dialogturns,AllDialogs_more750,AllDialogs_less500,AllDialogs_midrange,AlltextAllFiles):
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
        except : 
            print " error in file" + self.inputcsvStr
            
            sys.exit(1)         
    
    def createhitinput(self,outputcsv):
        MTrow=dict()
        No_ofitem=3
        No_ofhits=7
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
    topic="gay-rights-debates"
    taskno=3
    directory=os.getcwd() + "/CSV/"+ topic+"/discussion_dialogs/"
    MTdirectory=os.getcwd() + "/CSV/"+ topic+"/MTdata/MT"+ str(taskno)+"/"
    outputcsvdialog=MTdirectory +"Dialog_File"
    
    outputMT1=MTdirectory+"MT" +str(taskno)+"_more750"
    outputMT2=MTdirectory+"MT"+str(taskno)+"_less500"
    outputMT3=MTdirectory+"MT"+str(taskno)+"_midrange"
    
    outputHT_750=MTdirectory+"MT" +str(taskno)+"_more750"
    outputHT_Mid=MTdirectory+"MT" +str(taskno)+"_Mid"
    
    MTfile=MTdirectory+"MT"+str(taskno)+"_discussion_turns"
    
    fieldnames=list()
    AlltextAllFiles=list()
    Alldialogs_more750=list()
    Alldialogs_less500=list()
    Alldialogs_midrange=list()
    
    global Textline_750
    global Textline_Mid
    Textline_750=""
    Textline_Mid=""
    
    fieldnames.append("Dialogtext")
    fieldnames.append("key")
    fieldnames.append("Total_Count")
    #MT1discussion_turns(taskno) ## call this once for each MT task

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
            MTobject.createdialoginputfile(inputfile, inputdialogturns, Alldialogs_more750,Alldialogs_less500,Alldialogs_midrange,AlltextAllFiles)
    FileHandling.WriteTextFile(outputtextfile,AlltextAllFiles)
    inputdialogturns=""
    
    FileHandling.write_csv(outputcsvdialog+"_more750",Alldialogs_more750, fieldnames)
    MTobject1=Mechanical_Turk(outputcsvdialog+"_more750",inputdialogturns)

    FileHandling.write_csv(outputcsvdialog+"_less500",Alldialogs_less500, fieldnames)
    MTobject2=Mechanical_Turk(outputcsvdialog+"_less500",inputdialogturns)
 
    FileHandling.write_csv(outputcsvdialog+"_midrange",Alldialogs_midrange, fieldnames)
    MTobject3=Mechanical_Turk(outputcsvdialog+"_midrange",inputdialogturns)
 
    FileHandling.writeHtml(outputHT_750, Textline_750)
    FileHandling.writeHtml(outputHT_Mid, Textline_Mid)
    MTobject1.createhitinput(outputMT1)
    MTobject2.createhitinput(outputMT2)
    MTobject3.createhitinput(outputMT3)
    MTobject1.createhitinput(outputMT1) 