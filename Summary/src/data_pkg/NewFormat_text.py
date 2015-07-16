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
from ast import literal_eval
from collections import MutableMapping
import re
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

#------------------------------------------------------------ print type(string)
                #-------------------------------------------------- print string
                #------------------------------------------ print type(new_text)
                #----------------- #stringnew=unidecode(Dialogrow["Dialogtext"])
                # #stringnew=unicodedata.normalize('NFKD', string).encode('ascii','ignore')
#------------------------------------------------------------------------------ 

def stemstoptokens(stop,stoplist,stem,stemmername,wordlist):
    newwordlist=[]
    for word in wordlist:
                if stem:
                    word=stemmername.stem(word)
                    if stop:
                            stemstoplist=[stemmername.stem(stemword) for stemword in stoplist ]
                            if  word not in stemstoplist:
                                newwordlist.append(word)
                    else:
                            newwordlist.append(word)
                else:
                    if stop:
                            if  word not in stoplist:
                                newwordlist.append(word)
                    else:
                            newwordlist=wordlist
                            
    return newwordlist                        
    
def ascii_only_unicodeerror(text):  
    try:
        text=text.decode('utf-8',errors='strict')
        ascii_str=unidecode.unidecode(text)
        return ascii_str.decode('utf-8')
    except UnicodeDecodeError:
        print text
def getsents(lines): 
        asciitext=ascii_only(lines)
        sent_list = sent_tokenize(asciitext)
        return  sent_list     
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
def convertUnicode_to_dictlist(WordDictList):
        newlist=[]
        for dictlist in WordDictList:
            my_dict = literal_eval(dictlist)
            assert isinstance(my_dict, MutableMapping)
            newlist.append(my_dict)
        return newlist  
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


def removePOSSSeg(text):
    Alltokens=[]
    tokens=str(text).split()
    for token in tokens:
        tokens_Pos=token.split("/")
        tokenNoPos=tokens_Pos[0]
        Alltokens.append(tokenNoPos)
    Newtext= " ".join(Alltokens)  
    return Newtext  

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
    
def changeListtodict(Allrows,listitem):
    NewRows=[] 
    for row in Allrows:  
        newrow=dict()
        for key, value in row.iteritems():
            if key ==listitem :
                contribdict=dict()
                no_of_contrib=len(value)
                for i in range(0,no_of_contrib) :
                    key=listitem + str(i)
                    contribdict[key]=ascii_only(value[i][0])
                newrow[listitem]=contribdict
            else:
                newrow[key]=ascii_only(str(value))
        NewRows.append(newrow) 
    return NewRows   

def replace_s1s2(Text):
    Text1=re.sub("s1|s1:","Author1",Text,flags=re.IGNORECASE ) 
    Text2=re.sub("s2|s2:","Author2",Text1,flags=re.IGNORECASE ) 
    return Text2      
if __name__ == '__main__':
    
    checkencoding()