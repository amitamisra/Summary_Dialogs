'''
Created on Apr 30, 2014
This file creates dialog pairs by calling function selectpairssql from file  selectdialogpairs. The discussions to be included are in variable
gay_marriage_discussions2. It creates a view for each discussion using table name created in script create_post_quotes
@author: amita
'''
import os
import MySQLdb as mdb
import sys
import selectdialogpairs
import FileHandling
def createtablediscussionsid(dataset_id,topic,Discussions,viewname,Table):
    try:
       
        db1 = mdb.connect(host="localhost",user="root",passwd="",db="iac")
        cursor = db1.cursor(mdb.cursors.DictCursor) 
        Query_discussion_id="Select posts_discussion_id from {table_name}".format(table_name=Table)
        
        discussion_ids=set()
        cursor.execute(Query_discussion_id) 
        rows=cursor.fetchall()
        rows=list(rows)
        for row in rows:
            discussion_ids.add(row.values()[0])
        if All:
            Discussions=discussion_ids    
        for discussion_id in Discussions:
            if All:
                outputcsvStr=os.getcwd() + "/CSV/"+ topic+"/discussion_dialogs/All/" + str(discussion_id)+"dialog"
            else:
                outputcsvStr=os.getcwd() + "/CSV/"+ topic+"/discussion_dialogs/" + str(discussion_id)+"dialog"    
            Query_drop="Drop view if exists " + viewname
            cursor.execute(Query_drop)
            Query_view="""Create View """ + viewname + """  As Select * from """ + Table + """  where posts_discussion_id = %s """ 
            args=(discussion_id,)
            cursor.execute(Query_view,args)
            db1.commit()
            selectdialogpairobj=selectdialogpairs.selectdialogpair(dataset_id,discussion_id,max_turns_dialog,Dialog_Turn,outputcsvStr)
            selectdialogpairobj.selectpairssql(db1, cursor,viewname)
            
            
            
        
    except db1.Error, e:
            print e
            if db1:
                db1.rollback()
        
            sys.exit(1)
            print "Error %d: %s" % (e.args[0],e.args[1])    
            




gay_marriage_discussions2=[34,35,246,788,1062,1036,1037,1061,1062,1097,1226,1245,1281,1287,1292,1590,1598,1685,1690,
                           1756,1805,1807,1875,1897,1939,1990,2218,2280,2377,2583,2623,2844,2922,3089,3124,3134,3139,
                           3151,3176,3358,3485,3612,3639,3686,4166,4350,4692,4706,4727,4749,4825,4843,5084,5176,5320,5342,5418,
                           5589,5645,5655,5657,5670,5672,5680,5705,5714,5722,5811,5827,5846,5889,5890,5893,5894,5907,5923,5694,6117,6124,6137,6139,6151,6162,6180,6229,6293,6298,6319,6331,6338,6393,6397,6422,6479,6493,6545,6600,
                          6646,6716,6784,6788,6797,6923,6949,6968,7111,7122,7145,7173,7178,7185,7337,7434,7491,7522,7594,7614,7621,
                          7858,7910,7916,8171,8200,8228,8297,8364,8376,8383,8412,8598,8675,8747,8750,8761,8764,8765,8792,8834,8854,
                          8881,8905,8924,8930,8934,8960,9001,9132,9252,9331,9341,9390,9391,9470,9522,9568,9571,9619,9643,9668,9689,9719,
                          9745,9852,9989,10019,10073,10218,10349,10354,10416,10456,10466,10523,10538,10588,10577,10585,10722,10730,10765,
                          10786,10824,10831,10841,10844,10853,10951,10978]

#===============================================================================
# table="GAYRIGHTS"  used for gay rights
# topic="gay-rights-debates"  used for gay rights
#===============================================================================

table="DeathPenalty"
topic="death-penalty"
global Dialog_Turn
Dialog_Turn=1
global max_turns_dialog
max_turns_dialog=4
dataset_id=1
max_wordin_post=250
All=False
taskno=1

#discussions=gay_marriage_discussions2 done for gay rights


#===============================================================================
# if All:
#     viewname="gayAll"
# else:                            done for gay rights
#     viewname="gay"
#===============================================================================
    
    
#===============================================================================
# if All:
#     viewname="gunAll"
# else:
#     viewname="gun"     done for gun control
#===============================================================================


if All:
    viewname="deathall"
else:
    viewname="death"    

discussionfile=os.getcwd() + "/CSV/"+topic+"/" + topic+ "_discussions" 
rowlist=FileHandling.read_csv(discussionfile)  
discussions=[row["discussion_id"] for row in rowlist]
createtablediscussionsid(dataset_id,topic,discussions,viewname,table)
if __name__ == '__main__':
    
    pass