'''
Created on Apr 27, 2014

@author: amita
'''
#------------------ This file updates discussions in iac database for fourforums
#-------------- and maps discussions to gay rights and updates topic_id for gay
#----------------------------------------------------------------- rights in iac

import os
import MySQLdb as mdb
import sys
import FileHandling

class AddTopics: 
    def __init__(self,):
        print ""
    
    # return a list of rows from iac table discussions for a given url and a dataset
    def GetDiscussions(self,RegExp,dataset_id="1"): 
        try:
            db1 = mdb.connect(host="localhost",user="root",passwd="",db="iac")
            cursor = db1.cursor(mdb.cursors.DictCursor) 
            Query= "select * from discussions where dataset_id = (%s) and discussions.discussion_url regexp  (%s)"            
            print RegExp
            args=(dataset_id,RegExp,)
            cursor.execute(Query,args)
            rowdicts_tuple= cursor.fetchall()
            Listrowdicts=list(rowdicts_tuple)
            for row in Listrowdicts:
                del row["topic_id"]
                row["topic_id"]="8"    
            return Listrowdicts
        except db1.Error, e:
            print e
            if db1:
                db1.rollback()
        
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
  
    
   
        finally:    
        
            if db1:    
                db1.close()    
    # write rowdicts containing rows for a particualar topic from iac database, filename is output file as string
    def  writecsv(self, rowdicts,filename):
        Fieldnames=rowdicts[0].keys()
        directory = os.path.dirname(filename)
        print directory
        if not os.path.exists(directory):
            os.makedirs(directory)        
        FileHandling.write_csv(filename, rowdicts, Fieldnames)
 
 
        
    # create a temporary table TMPTABLE for merging the topics with the iac database
    #--------- filename is the input csv as string containing topic mapped to discussions
    def CreateTable(self,filename,Query_tmpTable,Query_Insert):
                              
        try:
            db1 = mdb.connect(host="localhost",user="root",passwd="",db="iac")
            cursor = db1.cursor(mdb.cursors.DictCursor)  
            cursor.execute(Query_tmpTable)
            rows=FileHandling.read_csv(filename)  # read rowdicts from input filename           
            cursor.executemany(Query_Insert,rows)
            db1.commit()
            
           
        
        except db1.Error, e:
            print e
            if db1:
                db1.rollback()
        
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
  
    
   
        finally:    
        
            if db1:    
                db1.close()  
                
                
    def UpdateDatabaseTable(self):
        try:
            db1 = mdb.connect(host="localhost",user="root",passwd="",db="iac")
            cursor = db1.cursor(mdb.cursors.DictCursor)            
            QueryUpdate= """update discussions As D INNER JOIN TMPTABLE As T 
                    ON (D.dataset_id = T.dataset_id and 
                        D.discussion_id = T.discussion_id)
                       SET D.topic_id =T.topic_id
                       where D.dataset_id = T.dataset_id and 
                       D.discussion_id = T.discussion_id"""
                            
            cursor.execute(QueryUpdate) 
            db1.commit()              
        except db1.Error, e:
            print e
            if db1:
                db1.rollback()
        
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
  
    
   
        finally:    
        
            if db1:    
                db1.close()        
                   
    def DropTmpTable(self):
        
        try:
            db1 = mdb.connect(host="localhost",user="root",passwd="",db="iac")
            cursor = db1.cursor(mdb.cursors.DictCursor) 
            cursor.execute("Drop TABLE if Exists TMPTABLE")  
            db1.commit()
        
        
        except db1.Error, e:
            print e
            if db1:
                db1.rollback()
        
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
  
    
   
        finally:    
        
            if db1:    
                db1.close()     
              
# Perform initializations for topic name and regular expression for url mapped to
#------------------------------------------------- discussions table in database
topic="gay-rights-debates"
RegExp="http://www.4forums.com/political/(" + topic +")/.*" # topic url to be mapped
filename=os.getcwd() + "/CSV/"+ topic+"/" + topic+ "_discussions"      # create a csv of topic mapped to all discussions 
Query_tmpTable="""CREATE TABLE IF NOT EXISTS TMPTABLE (dataset_id tinyint unsigned,
                    discussion_id  mediumint unsigned, discussion_url varchar(255), 
                    title varchar(255),topic_id mediumint unsigned null, initiating_author_id int unsigned null,
                    native_discussion_id int unsigned null,primary key (dataset_id, discussion_id), 
                    foreign key (dataset_id) references datasets(dataset_id),foreign key (topic_id) references topics(topic_id),
                    foreign key (dataset_id, initiating_author_id) references authors(dataset_id, author_id) 
                        )"""  
                        
Query_Insert="""INSERT INTO TMPTABLE (dataset_id, discussion_id, discussion_url,title,
                      topic_id,initiating_author_id ,native_discussion_id) VALUES ( %(dataset_id)s,%(discussion_id)s, %(discussion_url)s
                    ,%(title)s,%(topic_id)s,%(initiating_author_id)s,%(native_discussion_id)s)"""



addtopicobj = AddTopics()
rowdicts=addtopicobj.GetDiscussions(RegExp)
addtopicobj.WriteCsv(rowdicts,filename)
addtopicobj.CreateTable(filename,Query_tmpTable,Query_Insert)
addtopicobj.UpdateDatabaseTable()
addtopicobj.DropTmpTable()

if __name__ == '__main__':
    pass