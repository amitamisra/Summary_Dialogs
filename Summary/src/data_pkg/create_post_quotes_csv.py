'''
Created on Apr 27, 2014
This creates a post quote file containing posts and corresponding quotes. Use reply links to identify the quotes , there may be more than one 
quote links in the database, hence post_quotes file may contain more than one quote associated with a post.quote index
field distinguishes these quotes that are different parts of a quotesourcepost. select full quote text for each of these
and do not select based on start and end index  in the quote as it breaks dialog chains, then just select one record to get the quote text using 
min( quote_index) as all indexes contain same text.
@author: amita
'''
import os
import MySQLdb as mdb
import sys
import FileHandling
from string import Template


#===============================================================================
# create a csv file with name OutputFileStr contains all posts and quotes, there is only  one quote for a post containing the whole quote text
#===============================================================================
def Post_Quotes_Unique_Csv(OutputFile_Unique_Str,dataset,topic):
    Query_Unique= """ select posts.dataset_id As posts_dataset_id,posts.discussion_id As posts_discussion_id, posts.post_id As posts_post_id,
                posts.author_id As posts_author_id,
                posts.timestamp As posts_timestamp,posts.parent_post_id As posts_parent_post_id,posts.parent_missing As posts_parent_missing,
                posts.native_post_id As posts_native_post_id,
                posts.text_id As post_text_id, discussions.discussion_url As discussion_url,
                Min(quotes.quote_index) As Min_quotes_quote_index,quotes.parent_quote_index As quotes_parent_quote_index,
                quotes.text_index As quotes_text_index,
                quotes.text_id As quotes_text_id, quotes.source_post_id As quotes_post_id, quotes.source_start,quotes.source_end,
                quotes.source_truncated,quotes.source_altered,quotes.alternative_source_info,quote_source_post.dataset_id
                 As quote_source_post_dataset_id,quote_source_post.discussion_id  As quote_source_post_discussion_id ,
                quote_source_post.post_id As quote_source_post_id,quote_source_post.author_id As quote_source_author_id,
                quote_source_post.timestamp As quote_source_timestamp,quote_source_post.parent_post_id As quote_source_parent_post_id,
                quote_source_post.parent_missing As quote_source_parent_missing, quote_source_post.native_post_id As quote_source_native_post_id,
                quote_source_post.text_id As quote_source_text_id,text.text as post_text,
                if(quotes.source_altered or quotes.source_start is null or quotes.source_end is null,quote_text.text,
                    substr(quote_text.text,
                    quotes.source_start + 1,
                    quotes.source_end - quotes.source_start)) as quote_text_Partial,
                quote_text.text As Fullquote_text
                from posts join discussions USING (discussion_id , dataset_id)
                join datasets USING (dataset_id) join text USING (text_id , dataset_id)
               join topics USING (topic_id) join quotes USING (post_id , dataset_id , discussion_id)
              join text as quote_text ON (quotes.text_id = quote_text.text_id and quotes.dataset_id = quote_text.dataset_id)
             inner join  posts as quote_source_post ON (quote_source_post.post_id = quotes.source_post_id
            and quote_source_post.discussion_id = quotes.discussion_id
           and quote_source_post.dataset_id = quotes.dataset_id)
           where
           datasets.name = (%s)
           and topic = (%s)
         and parent_quote_index is null
        group by posts.dataset_id , posts.discussion_id , posts.post_id , quotes.source_post_id"""
    try:
            
        db1 = mdb.connect(host="localhost",user="root",passwd="",db="iac")
        cursor = db1.cursor(mdb.cursors.DictCursor)     
        args=(dataset,topic)
        cursor.execute(Query_Unique,args)
        rowdicts_tuple= cursor.fetchall()
        Listrowdicts=list(rowdicts_tuple)
        Fieldnames=sorted(Listrowdicts[0].keys())
        directory = os.path.dirname(OutputFile_Unique_Str)            
        if not os.path.exists(directory):
            os.makedirs(directory)   
        FileHandling.write_csv(OutputFile_Unique_Str,Listrowdicts,Fieldnames)          
        
    #quotes.source_start+1, #MySQL starts counting at 1
    #quotes.source_end - quotes.source_start) #the length of the quote
    # parent_quote_index is null   #avoids nested quotes
    
    except db1.Error, e:
            print e
            if db1:
                db1.rollback()
        
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
  
    
    finally:    
        
            if db1:    
                db1.close()       
#===============================================================================
# create a csv file with name OutputFileStr contains all posts and quotes, there may be more than one quote for 
# a post depending on quote start and quote end position
#===============================================================================
def Post_Quotes_Csv(OutputFileStr,dataset,topic):
    try:
            db1 = mdb.connect(host="localhost",user="root",passwd="",db="iac")
            cursor = db1.cursor(mdb.cursors.DictCursor) 
            Query= """select posts.dataset_id As posts_dataset_id , posts.discussion_id As posts_discussion_id,
                    posts.post_id As posts_post_id, posts.author_id As posts_author_id, posts.timestamp As posts_timestamp,
                    posts.parent_post_id As posts_parent_post_id, posts.parent_missing As posts_parent_missing, posts.native_post_id As
                    posts_native_post_id, posts.text_id As post_text_id,quotes.quote_index,
                    quotes.parent_quote_index, quotes.text_index As quotes_text_index,quotes.text_id As quotes_text_id,
                    quotes.source_discussion_id As quotes_source_discussion_id, quotes.source_post_id As quotes_source_post_id, 
                    quotes.source_start As quotes_source_start , quotes.source_end As quotes_source_end,
                    quotes.source_truncated As quotes_source_truncated, quotes.source_altered As quotes_source_altered,
                    quotes.alternative_source_info As quotes_alternative_source_info,
                    quote_source_post.dataset_id As quote_source_post_dataset_id, quote_source_post.discussion_id 
                    As quote_source_post_discussion_id ,quote_source_post.post_id As quote_source_post_id,
                    quote_source_post.author_id As quote_source_author_id, quote_source_post.timestamp As quote_source_timestamp,
                    quote_source_post.parent_post_id As quote_source_parent_post_id, quote_source_post.parent_missing 
                    As quote_source_parent_missing, quote_source_post.native_post_id As
                    quote_source_native_post_id, quote_source_post.text_id As quote_source_text_id,
                    text.text as post_text,
                    if( 
                    quotes.source_altered or 
                    quotes.source_start is null or 
                    quotes.source_end is null,
                    quote_text.text,
                    substr(
                    quote_text.text,
                    quotes.source_start+1, 
                    quotes.source_end - quotes.source_start) 
                    ) as quote_text,
                    quote_text.text  As Fullquote_text
                    from posts
                  join discussions using (discussion_id, dataset_id)
                  join datasets using(dataset_id)
                  join text using(text_id, dataset_id)
                  join topics using(topic_id)
                  join quotes using(post_id, dataset_id, discussion_id)
                  join text as quote_text on
                       (quotes.text_id=quote_text.text_id and quotes.dataset_id=quote_text.dataset_id)
                  inner join posts as quote_source_post on 
                  (quote_source_post.post_id=quotes.source_post_id and 
                 quote_source_post.discussion_id=quotes.discussion_id and
                quote_source_post.dataset_id=quotes.dataset_id)
                 where 
                      datasets.name= (%s) and
                      topic= (%s)and
                      parent_quote_index is null"""  
            
            args=(dataset,topic)
            cursor.execute(Query,args)
            rowdicts_tuple= cursor.fetchall()
            Listrowdicts=list(rowdicts_tuple)
            Fieldnames=Listrowdicts[0].keys()
            directory = os.path.dirname(OutputFileStr)            
            if not os.path.exists(directory):
                os.makedirs(directory)   
            FileHandling.write_csv(OutputFileStr,Listrowdicts,Fieldnames)          
    
    #quotes.source_start+1, #MySQL starts counting at 1
    #quotes.source_end - quotes.source_start) #the length of the quote
    # parent_quote_index is null   #avoids nested quotes
    
    except db1.Error, e:
            print e
            if db1:
                db1.rollback()
        
            sys.exit(1)
            print "Error %d: %s" % (e.args[0],e.args[1])
  
    
    finally:    
        
            if db1:    
                db1.close()   

# From the unique csv file as InputCsv created in function Post_Quotes_Csv, create the table for a given topic
def CreateTable_Post_Quotes_Unique(InputCsv,File_Col_Unique,topic,Table_topic):
        
    Query_Topic_Create="CREATE TABLE IF NOT EXISTS {table_name} (posts_dataset_id tinyint unsigned, posts_discussion_id  mediumint unsigned, posts_post_id mediumint unsigned, \
     posts_author_id int unsigned,posts_timestamp datetime null,posts_native_post_id int unsigned null,\
     post_text_id int unsigned,discussion_url varchar(255),\
    quote_source_post_dataset_id tinyint unsigned,quote_source_post_discussion_id mediumint unsigned,quote_source_post_id  mediumint unsigned,\
    quote_source_author_id int unsigned, quote_source_timestamp datetime null, quote_source_native_post_id mediumint unsigned,\
    quote_source_text_id int unsigned,\
    post_text longtext,Fullquote_text longtext,\
    primary key (posts_dataset_id, posts_discussion_id,posts_post_id,quote_source_post_id),\
                    foreign key (posts_dataset_id) references datasets(dataset_id),\
                    foreign key(posts_dataset_id,posts_discussion_id) references discussions(dataset_id,discussion_id),\
                    foreign key(posts_dataset_id,posts_discussion_id,posts_post_id)references posts(dataset_id,discussion_id,post_id),\
                    foreign key (posts_dataset_id, posts_author_id) references authors(dataset_id, author_id) )".format(table_name=Table_topic) 
                        
    Query_Topic_Insert="INSERT INTO {table_name} (posts_dataset_id , posts_discussion_id, posts_post_id,\
                    posts_author_id,posts_timestamp,posts_native_post_id ,post_text_id,discussion_url,\
                    quote_source_post_dataset_id ,quote_source_post_discussion_id ,quote_source_post_id,\
                    quote_source_author_id ,quote_source_timestamp ,quote_source_native_post_id, quote_source_text_id,\
                    post_text ,Fullquote_text)\
                    VALUES ( %(posts_dataset_id)s,%(posts_discussion_id)s, %(posts_post_id)s,\
                    %(posts_author_id)s,%(posts_timestamp)s,%(posts_native_post_id)s ,%(post_text_id)s ,\
                    %(discussion_url)s,%(quote_source_post_dataset_id)s ,%(quote_source_post_discussion_id)s ,\
                    %(quote_source_post_id)s ,%(quote_source_author_id)s ,%(quote_source_timestamp)s,\
                    %(quote_source_native_post_id)s,%(quote_source_text_id)s,%(post_text)s ,\
                    %(Fullquote_text)s)".format(table_name=Table_topic) 


    try:     
            Setcolnames=set()
            db1 = mdb.connect(host="localhost",user="root",passwd="",db="iac")
            cursor = db1.cursor()  
            print Query_Topic_Create
            cursor.execute(Query_Topic_Create)
            #colselect="SELECT column_name FROM information_schema.columns WHERE TABLE_NAME  = `DeathPenalty`"
            #print colselect
            #args=(Table_topic,)
            cursor.execute("""SELECT * from {table_name}""".format(table_name=Table_topic))
            print cursor.description
            for colname in cursor.description :
                Setcolnames.add(colname[0])
            print Setcolnames
            FileHandling.KeepColumns_Csv(InputCsv,File_Col_Unique ,Setcolnames)
            rows=FileHandling.read_csv(File_Col_Unique)  # read rowdicts from input filename
            cursor = db1.cursor(mdb.cursors.DictCursor)
            querin=Query_Topic_Insert
            print querin
            for row in rows:
                cursor.execute(querin,row)
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
 


if __name__ == '__main__':
    # change these 3 variables for every topic
    
    topic="evolution"
    Table_topic="Evolution"
    dataset="fourforums"
             
    
    
    #---------------------------------------------------------- topic="abortion" done once
    #---------------------------------------------------- Table_topic="Abortion" done once
    #------------------------------------------------------ dataset="fourforums" done once
             
    
    
    # topic="gay-rights-debates" # used for gay rights, done once
    # Table_topic="GAYRIGHTS"     # used for gay rights, done once
    
    # topic="gun-control"done once
    # Table_topic="GunControl" used for gun control done once
    
    
    filename=os.getcwd() + "/CSV/"+topic+"/" + topic+ "QRPairs"  
    filename_unique=os.getcwd() + "/CSV/"+topic+"/" + topic+ "QRPairs_unique"  
    file_col_unique=os.getcwd() + "/CSV/"+topic+"/" + topic+ "QRPairs_col_unique"  
    
    
    
    # done for gay marriage
    #----------- Post_Quotes_Csv(filename,dataset="fourforums",topic="gay marriage")
    # Post_Quotes_Unique_Csv(filename_unique,dataset="fourforums",topic="gay marriage") used for gay marriage
    
    # done for gun control
    #Post_Quotes_Csv(filename,dataset="fourforums",topic="gun control")
    #Post_Quotes_Unique_Csv(filename_unique,dataset="fourforums",topic="gun control")  used for gun control
    
    
    Post_Quotes_Csv(filename,dataset,topic)
    Post_Quotes_Unique_Csv(filename_unique,dataset,topic)
     
    CreateTable_Post_Quotes_Unique(filename_unique,file_col_unique,topic,Table_topic)                       
