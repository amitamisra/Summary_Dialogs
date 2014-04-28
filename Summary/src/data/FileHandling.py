'''
Created on Apr 27, 2014

@author: amita
'''
import os
import csv  
import sys
import codecs
from collections import defaultdict
def write_csv(outputcsv, rowdicts, fieldnames):
        try:
            restval=""
            extrasaction="ignore"
            dialect="excel"
            outputfile = open(outputcsv + ".csv",'w')
            csv_writer = csv.DictWriter(outputfile, fieldnames, restval, extrasaction, dialect, quoting=csv.QUOTE_NONNUMERIC)
            csv_writer.writeheader()
            csv_writer.writerows(rowdicts) 
            outputfile.close()
        except csv.Error :
                print "csverror" + outputcsv
                sys.exit(1)  
                
def read_csv(inputcsv):   
    try:
        inputfile = codecs.open(inputcsv+ ".csv",'r') 
        result = list(csv.DictReader(inputfile))
        return result              
    except csv.Error:
                print "inputcsverror" + inputcsv
                sys.exit(1)                    
                                   
if __name__ == '__main__':
    pass