from data_pkg import FileHandling
from collections import Counter
from nlp.text_obj import TextObj
'''
Created on Aug 10, 2014

@author: amita
'''
def removeS(text):
    remove_list=["s1", "s2"]
    text_obj = TextObj(text.decode('utf-8', 'replace'))
    text=(text_obj.text).lower()
    word_list = text.split()
    text=' '.join([i for i in word_list if i not in remove_list])
    return text
def createtokens(text): 
    text_obj = TextObj(text.decode('utf-8', 'replace'))
    tokens=text_obj.tokens 
    return tokens

class FeatureCreate:
    def __init__(self, feature_list,input_file):
        self.feature_list=feature_list
        self.input_file=input_file
    def generate_ngram(self,tokens,ngram,): 
        k=ngram
        list_ngram=list()
        for i in range(len(tokens)-k+1):
                    list_ngram.append("".join(tokens[i:k+i]))

        return list_ngram
    def get_ngrams(self,speaker,feature_vector, tokens,n):

        n_grams=tokens
        word_counts = Counter(n_grams)
        total_words = len(n_grams)
        list=word_counts.items()
        setngram=set(tokens)

        if n==1:
            prefix="uni"
        if n==2:
            prefix="bi"
        if n==3:
            prefix="tri"

        for word in setngram:
            feature_vector[speaker +"_"+ prefix + 'gram'+':'+ word]=word_counts[word]
            
    def create_ngram(self,row,feature_vector,ngram):
        s1=row["SCU1"]
        s2=row["SCU2"]
        s1=removeS(s1)
        s2=removeS(s2)
        s1token=createtokens(s1)
        s2token=createtokens(s2)
        s1_ngram=self.generate_ngram("s1",feature_vector,s1token, ngram=1)
        s2_ngram=self.generate_ngram("s2",feature_vector,s2token, feature_vector,ngram=1)
        
        
        
    

         
         

if __name__ == '__main__':
    pass