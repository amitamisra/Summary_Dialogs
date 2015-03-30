'''
Created on Aug 28, 2014

@author: amita
'''
from nltk  import word_tokenize
import nltk



text = word_tokenize("bar  his family from legal protections")
pos_string=nltk.pos_tag(text)
print pos_string

if __name__ == '__main__':
    pass