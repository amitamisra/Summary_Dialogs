'''
Created on Aug 15, 2014

@author: amita
'''
from nlp.text_obj import TextObj
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize
import re


def removeS(text):
    #remove_list=["s1", "s2","S1","S2"]
    pattern1 = re.compile('[sS][1-2]')
    text=re.sub(pattern1, '', text)
    #word_list = word_tokenize(text)
    return text

    


def preprocess(text,stem,stop):
    from nltk.corpus import stopwords
    text=text.lower()
    #text_obj = TextObj(text.decode('utf-8', 'replace'))
    tokens=word_tokenize(text)
    if stop:
        stopwords = stopwords.words('english')
        tokens = [w for w in tokens if w not in stopwords]
    if stem:
        stem_tokens=list()
        stemmer = PorterStemmer()
        for token in tokens:
            stem_tokens.append(stemmer.stem(token))
        text=" ".join(stem_tokens)
    else:    
        text=" ".join(tokens)
    return text
         
                