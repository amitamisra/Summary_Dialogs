'''
Created on Apr 16, 2015
Take the original pairs file from paraphrase MTHit input, change fields to as in final output from mechanical turk
change _1 to _a, _2 to _ b since this is the final outcome fieldname after processing mechanical turk
@author: amita
'''
from data_pkg import FileHandling
def MTInputSplit(inputcsv,output,NotPairsList):
    AllRows=FileHandling.read_csv(inputcsv)
    fields=AllRows[0].keys()
    fieldnames=set
    for field in fields:
        if field in NotPairsList:
                fieldnames.append(field)
        else:
                fieldnames.append(field[:-1])
    NewRows=[]
    NewRow=dict()
    for row in AllRows:
            for field in fieldnames:
                if field in NotPairsList:
                    NewRow[field+ "_a"]=row[field]
                else:
                    NewRow[field+ "_a"]=row[field+str(1)]
                    

if __name__ == '__main__':
   NotPairsList=["UMBC","uniqueRowNoa_4"] 
   