#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Created on May 6, 2014

@author: amita
'''

import unicodedata
from nlp.text_obj import TextObj
import os
import FileHandling
from file_formatting import csv_wrapper
import unidecode


#------------------------------------------------------------ print type(string)
                #-------------------------------------------------- print string
                #------------------------------------------ print type(new_text)
                #----------------- #stringnew=unidecode(Dialogrow["Dialogtext"])
                # #stringnew=unicodedata.normalize('NFKD', string).encode('ascii','ignore')
#------------------------------------------------------------------------------ 
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
def ascii_only(text):
    """If you really can't use unicode..."""
    
    text=text.decode('utf-8',errors='strict')
    ascii_str=unidecode.unidecode(text)
    
    #===========================================================================
    # chars = list()
    # for ch in nfkd:
    #     
    #     #TODO: Handle punctuation and other things which this can miss
    #     if 9 <= ord(ch) <= 126:
    #         chars.append(ch)
    # ascii_str = ''.join(chars)
    #===========================================================================
    return ascii_str.decode('utf-8')


def correctPunct(new_text):  
        new_text=new_text.replace(" .", ".") 
        new_text=new_text.replace(" ,", ",")  
        new_text=new_text.replace(" ?", "?") 
        new_text=new_text.replace(" !", "!") 
        return new_text  

def ascii_only_posts(text):
    """If you really can't use unicode..."""
    
   # text=text.decode('utf-8',errors='strict')
    ascii_str=unidecode.unidecode(text)
    
    #===========================================================================
    # chars = list()
    # for ch in nfkd:
    #     
    #     #TODO: Handle punctuation and other things which this can miss
    #     if 9 <= ord(ch) <= 126:
    #         chars.append(ch)
    # ascii_str = ''.join(chars)
    #===========================================================================
    return ascii_str.decode('utf-8')



def removetokens(tokens,removetoken):
    newtokenlist=list()
    for token in tokens:
        if removetoken in token:
            continue
            
        else:
            newtokenlist.append(token)
    return newtokenlist

def word_count(text,removelist):
    text_obj= TextObj(text)
    text=text_obj.text
    tokens = text_obj.tokens
    tokens= [x for x in tokens if x not in removelist]
    num_words=len(tokens)
    return num_words

def replacetoken(tokens,replacefrom,replaceto):
    
    tokens=[replaceto if x in replacefrom else x  for x in tokens ]
    
    return tokens

def checkencoding():
    topic="gay-rights-debates"
    inputfile=os.getcwd()+ "/CSV/"+ topic +"/Summaries/TextFiles/TextFiles_1/1-6229_6_5__7_8_9_16_26_29_46_47_48_2_user2.txt" 
    outputcsv=os.getcwd()+ "/CSV/"+ topic +"/Summaries/TextFiles/TextFiles_1/chkencoding"
    punctuation = { 0x2018:0x27, 0x2019:0x27, 0x201C:0x22, 0x201D:0x22 }
    Text=FileHandling.ReadTextFile(inputfile)
    new_text=Text[0].decode('utf-8')
    chk_dict=dict()
   
    #new_text=new_text.decode('utf-8')
    
    #csv_wrapper.write_csv(outputcsv, rowdicts, fieldnames, get_keys_from_first_row=True)
    #===========================================================================
    # new_text=new_text.replace(u'’', u"'")
    # new_text=new_text.replace(u'“', u"'")
    # new_text=new_text.replace(u'”', u"'")
    # new_text=ascii_only(new_text) 
    #===========================================================================
    
    print (new_text)
    print type(new_text)
    new_text=unidecode.unidecode(new_text)
    print new_text
    print type(new_text)
    new_text=new_text.decode('utf-8')
    print type(new_text)
    chk_dict["text"]=new_text
    rowdicts=list()
    rowdicts.append(chk_dict)
    fieldnames=list()
    fieldnames.append("text")
    FileHandling.write_csv(outputcsv, rowdicts, fieldnames)
    
    
if __name__ == '__main__':
    
    checkencoding()