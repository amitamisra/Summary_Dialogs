'''
Created on May 1, 2014
creates a csv file for each discussion containing dialog pairs, filename comes from class object created in create_chain_discussion_topic
@author: amita
'''
import FileHandling
import sys
import os
from operator import itemgetter
from nlp.text_obj import TextObj


class selectdialogpair:
    def __init__(self,dataset_id,discussion_id,max_turns_dialog,Dialog_Turn,outputcsvStr):
        self.max_turns_dialog=max_turns_dialog
        self.discussion_id=discussion_id
        self.Dialog_Turn=1
        self.dataset_id=dataset_id
        self.outputcsvStr=outputcsvStr

    def length(self,getitem):
            #removetokenlist="emoticon"
            text=getitem["post_text"]
            #===================================================================
            # print type(text)
            # text=unicode(text,errors='replace')
            # print type(text)
            #===================================================================
            text_obj = TextObj(text)
            text=text_obj.text
            tokens = text_obj.tokens
            #tokens=NewFormat_text.removetokens(tokens,removetokenlist)
            #new_text=" ".join(tokens)
            num_words=len(tokens)
            #getitem["post_text"]=new_text
            getitem["Word_Count"]=num_words
            
    def lengthQuote(self,getitem):
        #removetokenlist="emoticon"
        text=getitem["Fullquote_text"]
        #=======================================================================
        # text=unicode(text,errors='replace')
        #=======================================================================
        text_obj = TextObj(text)
        text=text_obj.text
        tokens=text_obj.tokens
        #tokens=NewFormat_text.removetokens(tokens,removetokenlist)
        #new_text=" ".join(tokens)
        #getitem["Fullquote_text"]=new_text
        num_words=len(tokens)
        return num_words
                   

    #def removeemoticon(ListPair[0])
    def createrowsdialogs(self,PairTuple):
     
                max_wordin_post=250
                #PrevQuoteId=PairList[0]["Quote_Id"]
                ListPair=list(PairTuple)
                PrevRespId=ListPair[0]["posts_post_id"]
                TextList=list()
                AllList=list()
                ListPair[0]["Dialog_Turn"]=self.Dialog_Turn
                ListPair[0]["key"]= str(self.dataset_id )+"-"+ str(self.discussion_id) +"_"+ str(ListPair[0]["posts_post_id"])+"_"+str(ListPair[0]['quote_source_post_id'])+"_"+ str(self.Dialog_Turn)
                self.length(ListPair[0])
                #ListPair[0]=self.removeemoticon(ListPair[0])
                TextList.append(ListPair[0])
                ListPair.pop(0)
                if any(d['quote_source_post_id'] == PrevRespId for d in ListPair):
                    index= map(itemgetter('quote_source_post_id'), ListPair ).index(PrevRespId)
                else:
                    index=-1    
                
                while ListPair:
                    if index !=-1:
                        getitem=ListPair[index]
                        if str(self.discussion_id)=="2583" and (getitem["posts_post_id"])==195:
                            print "2583"
                        getitem["key"]= str(self.dataset_id )+"-"+ str(self.discussion_id) +"_"+ str(getitem["posts_post_id"])+"_"+str(getitem['quote_source_post_id'])+"_"+ str(self.Dialog_Turn)
                        getitem["Dialog_Turn"]=self.Dialog_Turn
                        self.length(getitem)
                        TextList.append(getitem)
                        PrevRespId=getitem["posts_post_id"]
                        ListPair.pop(index)
                        if any(d['quote_source_post_id'] == PrevRespId for d in ListPair):
                            index= map(itemgetter('quote_source_post_id'), ListPair ).index(PrevRespId)
                        else:
                            index=-1 
                                       
                    else:
                        while TextList and self.lengthQuote(TextList[0]) > max_wordin_post: 
                            TextList.pop(0)
                        if len(TextList) > self.max_turns_dialog:    
                            
                            seq = [x['Word_Count'] for x in TextList]
                            subseq_more250_index=[i for i, j in enumerate(seq) if int(j) > max_wordin_post]
                            
                            if subseq_more250_index:
                                previndex=subseq_more250_index[0]
                                if len(subseq_more250_index)==1 :
                                    if subseq_more250_index[0] >=5:
                                        for i in range(0, subseq_more250_index[0]):
                                            TextList[i]["Dialog_Turn"]=self.Dialog_Turn 
                                        self.Dialog_Turn=self.Dialog_Turn+1 
                                        AllList.extend(TextList[0:(subseq_more250_index[0]) ])
                                    else:
                                        lenTextlist=len(TextList)    
                                        if lenTextlist-1 - previndex >=6 :
                                            for i in range(previndex+2,lenTextlist):
                                                TextList[i]["Dialog_Turn"]=self.Dialog_Turn 
                                            self.Dialog_Turn=self.Dialog_Turn+1 
                                            AllList.extend(TextList[previndex+2:lenTextlist])
                                                
                                    
                                else:    
                                    for ind in subseq_more250_index[1:]:
                                        if ind - previndex >=7:
                                            for i in range(previndex+2, ind):
                                                TextList[i]["Dialog_Turn"]=self.Dialog_Turn 
                                            self.Dialog_Turn=self.Dialog_Turn+1    
                                            AllList.extend(TextList[previndex+2:ind])
                                        previndex=ind
                                    lenTextlist=len(TextList)    
                                    if lenTextlist-1 - previndex >=6 :
                                        for i in range(previndex+2,lenTextlist):
                                            TextList[i]["Dialog_Turn"]=self.Dialog_Turn 
                                        self.Dialog_Turn=self.Dialog_Turn+1 
                                        AllList.extend(TextList[previndex+2:lenTextlist])
                                    
                            else:
                                AllList.extend(TextList)
                                self.Dialog_Turn=self.Dialog_Turn+1            
                                
                        PrevRespId=ListPair[0]["posts_post_id"]
                        TextList=list()
                        ListPair[0]["Dialog_Turn"]=self.Dialog_Turn
                        self.length(ListPair[0])
                        ListPair[0]["key"]= str(self.dataset_id )+"-"+ str(self.discussion_id) +"_"+ str(ListPair[0]["posts_post_id"])+"_"+str(ListPair[0]['quote_source_post_id'])+"_"+ str(self.Dialog_Turn)
                        TextList.append(ListPair[0])
                        ListPair.pop(0)
                        if any(d['quote_source_post_id'] == PrevRespId for d in ListPair):
                            index= map(itemgetter('quote_source_post_id'), ListPair ).index(PrevRespId)
                        else:
                            index=-1 
                               
                return AllList           
    def selectpairssql(self,db1,cursor,viewname): 
        
                
                sql_Pairs="""SELECT * FROM """ + viewname + """  WHERE ((posts_author_id = %s and quote_source_author_id = %s) or
                  (posts_author_id = %s and  quote_source_author_id = %s))""" 
                
                AllList=list()
                try:
                    

                    Query3="""SELECT least(quote_source_author_id, posts_author_id) as Author_A, greatest(quote_source_author_id, posts_author_id)
                             as Author_B, COUNT(*) as cnt FROM %s GROUP BY least(quote_source_author_id, posts_author_id), greatest(quote_source_author_id, posts_author_id)  HAVING (COUNT(*) > 3)""" % viewname   
                    cursor.execute(Query3)
                    rowdicts= cursor.fetchall()
                    for pair in rowdicts:
                        args=pair["Author_A"],pair["Author_B"],pair["Author_B"],pair["Author_A"]
                        cursor.execute(sql_Pairs,args)
                        pairdicts=cursor.fetchall()
                       
                        TextListPair=self.createrowsdialogs(pairdicts)
                        if TextListPair:
                            AllList.extend(TextListPair)
        
                             
                    db1.commit()
                    if AllList: 
                        fieldnames=FileHandling.getcolumnnames(db1,viewname)                       
                        fieldnames.add("Dialog_Turn")
                        fieldnames.add("Word_Count")
                        fieldnames.add("key")
                        sorted(fieldnames)
                        directory = os.path.dirname(self.outputcsvStr) 
                        if self.outputcsvStr=="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/discussion_dialogs/1037dialog":
                            print "stop"          
                        if not os.path.exists(directory):
                            os.makedirs(directory)   
                        
                        FileHandling.write_csv(self.outputcsvStr, AllList, fieldnames) 
                except db1.Error, e:
                    print e
                    if db1:
                        db1.rollback()
                
                    print "Error %d: %s" % (e.args[0],e.args[1])
                    sys.exit(1)
                                 
All=True

if __name__ == '__main__':
            pass