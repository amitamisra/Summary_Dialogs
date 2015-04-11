#!/usr/bin/env python
#coding: utf8 

'''
Created on Oct 16, 2014
This creates features for simiarity among labels, takes input as a json formed from executing stanford parser
RunCoreNLP_CSV.java. RunCoreNLP_CSV.java takes  input as MT2/ResultsV3/MT2_web_interface_split_worker.csv from mechanical hit containing MT labels
for each pair of strings
@author: amita
'''

from __future__ import division
from random import shuffle
from requests import get
from data_pkg import FileHandling
from file_formatting import csv_wrapper
import itertools 
import operator
import os
from collections import defaultdict
from operator import itemgetter
from  nltk.metrics import edit_distance
from nltk.corpus import stopwords
import nltk
from nltk.corpus import wordnet as wn
from  CompareStanfordDependencyRelations import GetCorrPair
from nltk.corpus import webtext
import numpy as np
import math
import sys
from collections import Counter
from pyrouge import Rouge155
from data_pkg import NewFormat_text
from collections import Counter
from operator import sub
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
import word_category_counter
from copy import deepcopy 



global  goldstandard
global NotToUseCategory

NotToUseCategory=["Unique Words","Words Per Sentence","Word Count","Dictionary Words","Common Verbs", "Six Letter Words", "Present Tense",\
                   "Total Function Words", "Word Count", "Total Pronouns","Present Tense","Adverbs", "Impersonal Pronouns", "Sentences","Space","Past Tense", "Auxiliary Verbs",\
                   "Quantifiers","Dash","Number","All Punctuation"," Impersonal Pronouns"]

LIWC_StopList=["'s","think","say","said","get","'ve","believe","saying"]

global FinalLIWC   

global fieldnames
fieldnames=["HITId","HITTypeId","UMBC_" ,"doccounta_", "doccountb_","keya_", "keyb_", "label_cluster_ ", "stringa_", "stringb_"]
def  convert_jsonobjects_tocsv( InputFileJsontxt,OutputCSv):
    try:
            rowdicts=FileHandling.jsontorowdicts(InputFileJsontxt)
            fieldnames= sorted(rowdicts[0].keys())
            newrowdicts=list()
            for row in rowdicts:
                newrow=dict()
                for key in fieldnames:
                    newrow[key]=row[key]
                    #text_obj = TextObj(row[key])
                    #text=text_obj.text
                    #print type(text)
                    #new_text=text.encode('ascii', 'ignore')
                    #newrow[key]=NewFormat_text.ascii_only(newrow[key])
                newrowdicts.append(newrow)        
                
            FileHandling.write_csv(OutputCSv, newrowdicts, fieldnames)
    except Exception as e:
        s = str(e)
        print "error in file" + InputFileJsontxt + "in function FileHandling.convert_json_tocsv"
        print s
        sys.exit(1)


class Features:
    def __init__(self,Input_withdistSim, LIWC_words, LIWC_Category,FeatureFile,RandomizeFeatureFile,TrainingTextFile):
        self.Input_withdistSim=Input_withdistSim
        self.LIWC_words=LIWC_words
        self.LIWC_Category= LIWC_Category
        self.FeatureFile=FeatureFile
        self.TrainingTextFile=TrainingTextFile
        self.RandomizeFeatureFile=RandomizeFeatureFile
        
     
    def KeepSubVerbAdjAdv(self,WordDictList): 
        WordList=list()
        for worddict in WordDictList:
            if (worddict["pos"]).startswith( ("JJ","RB", "NN","VB") ):
                WordList.append(worddict)
        return   WordList      
           
    def ReadJson(self):
        InputRows=FileHandling.jsontorowdicts(self.Input_withdistSim)
        return InputRows
   
    def LevDistance(self,row,NewRow,KeepSubVerbObj):
        if KeepSubVerbObj:
            
            XWordDict=row["Word_Dictstringa_"]
            SortedListX=sorted(XWordDict, key=lambda x: int(operator.itemgetter("index")(x)))
            ReducedWordListX=self.KeepSubVerbAdjAdv(SortedListX)
            
            
            YWordDict=row["Word_Dictstringb_"]
            SortedListY=sorted(YWordDict, key=lambda x: int(operator.itemgetter("index")(x)))
            ReducedWordListY=self.KeepSubVerbAdjAdv(SortedListY)
            
            
            StringA=" ".join(word["lemma"] for word in ReducedWordListX)
            StringB=" ".join(word["lemma"] for word in ReducedWordListY)
        else:
            
            StringA=row["stringa_"]
            StringB=row["stringb_"]
        Lev_Dist= edit_distance(StringA, StringB)
        NewRow["Lev_Dist"]=Lev_Dist
        
    def LCS(self,row,NewRow,KeepSubVerbObj):
        if KeepSubVerbObj:
            XWordDict=row["Word_Dictstringa_"]
            ReducedWordListX=self.KeepSubVerbAdjAdv(XWordDict)
            
            YWordDict=row["Word_Dictstringb_"]
            ReducedWordListY=self.KeepSubVerbAdjAdv(YWordDict)
            
            X=" ".join(word["lemma"] for word in ReducedWordListX)
            Y=" ".join(word["lemma"] for word in ReducedWordListY)
        else:    
            X=row["stringa_"]
            Y=row["stringb_"]
        
        m = len(X)
        n = len(Y)
        # An (m+1) times (n+1) matrix
        C = [[0 for j in range(n+1)] for i in range(m+1)]
        for i in range(1, m+1):
            for j in range(1, n+1):
                if X[i-1] == Y[j-1]: 
                    C[i][j] = C[i-1][j-1] + 1
                else:
                    C[i][j] = max(C[i][j-1], C[i-1][j])
        return C
    
    
    
    def buildVector(self,iterable1, iterable2):
        counter1 = Counter(iterable1)
        counter2= Counter(iterable2)
        all_items = set(counter1.keys()).union( set(counter2.keys()) )
        vector1 = [counter1[k] for k in all_items]
        vector2 = [counter2[k] for k in all_items]
        return (vector1 , vector2)

    def cosim(self,v1, v2):
        dot_product = sum(n1 * n2 for n1,n2 in zip(v1, v2) )
        magnitude1 = math.sqrt (sum(n ** 2 for n in v1))
        magnitude2 = math.sqrt (sum(n ** 2 for n in v2))
        if (magnitude1==0 or magnitude2==0):
            return 0
        return dot_product / (magnitude1 * magnitude2)

    
    def UnigramCosine(self,row):
        XWordDict=row["Word_Dictstringa_"]
        YWordDict=row["Word_Dictstringb_"]
        Xlist=list()
        Ylist=list()
        for wordx in XWordDict:
            if wordx["word"].lower() not in Stop_List:
                Xlist.append(wordx["lemma"] )
        for wordy in YWordDict:
            if wordy["word"] not in Stop_List:
                Ylist.append(wordy["lemma"] )
                
        X_Y=self.buildVector(Xlist,Ylist) 
        cosimunigram=self.cosim(X_Y[0],X_Y[1])
        row["cosunigram"]=cosimunigram
                       
        
    def bigramCosine(self,row): 
        XWordDict=row["Word_Dictstringa_"]
        YWordDict=row["Word_Dictstringb_"]
        Xlistsorted = sorted(XWordDict, key=lambda x: int(operator.itemgetter("index")(x)))
        Ylistsorted=sorted(YWordDict, key=lambda x: int(operator.itemgetter("index")(x)))
        Xlist=[word["lemma"] for word in Xlistsorted]
        Ylist=[word["lemma"] for word in Ylistsorted ]
        
        Xbigram=list(nltk.bigrams(Xlist))
        Ybigram=list(nltk.bigrams(Ylist))
        X_Y=self.buildVector(Xbigram,Ybigram) 
        cosimbigram=self.cosim(X_Y[0],X_Y[1])
        row["cosbigram"]=cosimbigram
        
    
    
    def ExtNVACosine(self,Xlist,Ylist):
        X_Y=self.buildVector(Xlist,Ylist) 
        cosimunigram=self.cosim(X_Y[0],X_Y[1])
        return cosimunigram
                       
    
    #Find common unigrams in pairs
    def ngramOverlap(self,row,NewRow,ngram):
       # Uni_lemma_overlap_count=0
        #Uni_word_overlap_count=0
        Bi_lemma_overlap_count=0
        Bi_word_overlap_count=0
        Tri_lemma_overlap_count=0
        Tri_word_overlap_count=0
        common_word_unigram={}
        common_lemma_unigram={}
        XWordDict=row["Word_Dictstringa_"]
        YWordDict=row["Word_Dictstringb_"]
        Xlistsorted = sorted(XWordDict, key=lambda x: int(operator.itemgetter("index")(x)))
        Ylistsorted=sorted(YWordDict, key=lambda x: int(operator.itemgetter("index")(x)))
        Xlist_lemma=[word["lemma"] for word in Xlistsorted]
        Ylist_lemma=[word["lemma"] for word in Ylistsorted ]
        Xlist_word=[word["word"] for word in Xlistsorted]
        Ylist_word=[word["word"] for word in Ylistsorted ]
        if "1" in ngram:
            for i in Xlist_lemma:
                if i not in Stop_List:
                    common_lemma_unigram[i] = Ylist_lemma.count(i) 
            for i in Xlist_word:
                if i not in Stop_List:
                    common_word_unigram[i] = Ylist_word.count(i) 
            Uni_lemma_overlap_count=sum(common_lemma_unigram.itervalues()) 
            Uni_word_overlap_count= sum(common_word_unigram.itervalues())        
        
        if "2" in ngram:  
            common_lemma_bigram ={}
            common_word_bigram={}
            Xbigram_lemma=list(nltk.bigrams(Xlist_lemma))
            Ybigram_lemma=list(nltk.bigrams(Ylist_lemma))
            Xbigram_word=list(nltk.bigrams(Xlist_word))
            Ybigram_word=list(nltk.bigrams(Ylist_word))
            for i in Xbigram_lemma:
                common_lemma_bigram[i] = Ybigram_lemma.count(i) 
            for i in Xbigram_word:
                common_word_bigram[i] = Ybigram_word.count(i)
            Bi_lemma_overlap_count=sum(common_lemma_bigram.itervalues()) 
            Bi_word_overlap_count= sum(common_word_bigram.itervalues())        
                
                
        if "3" in ngram: 
            common_lemma_trigram ={}
            common_word_trigram={}
            Xtrigram_lemma=list(nltk.trigrams(Xlist_lemma))
            Ytrigram_lemma=list(nltk.trigrams(Ylist_lemma))
            Xtrigram_word=list(nltk.trigrams(Xlist_word))
            Ytrigram_word=list(nltk.trigrams(Ylist_word))
            for i in Xtrigram_lemma:
                common_lemma_trigram[i] = Ytrigram_lemma.count(i) 
            for i in Xtrigram_word:
                common_word_trigram[i] = Ytrigram_word.count(i)
            Tri_lemma_overlap_count=sum(common_lemma_trigram.itervalues()) 
            Tri_word_overlap_count= sum(common_word_trigram.itervalues()) 
                
        NewRow["Uni_lemma_overlap_count"]=Uni_lemma_overlap_count  
        NewRow["Bi_lemma_overlap_count"]= Bi_lemma_overlap_count    
        NewRow["Tri_lemma_overlap_count"]=Tri_lemma_overlap_count
       # return(Uni_lemma_overlap_count,Uni_word_overlap_count,Bi_lemma_overlap_count,Bi_word_overlap_count, Tri_lemma_overlap_count,Tri_word_overlap_count)           
                
    def FreqDistTrain(self,rows):  
        NounListWord=[]
        VerbListWord=[]
        AdjListWord=[]
        NounListLemma=[]
        VerbListLemma=[]
        AdjListLemma=[]
           
           
        for row in rows:
            XWordDict=row["Word_DictSent"]
            Xdict_listsorted = sorted(XWordDict, key=lambda x: int(operator.itemgetter("index")(x)))
            Xlist_lemma_Noun=[word["lemma"] for word in Xdict_listsorted if str(word ["pos"]).startswith ("NN") ]
            Xlist_word_Noun=[word["word"].lower() for word in Xdict_listsorted if str(word ["pos"]).startswith ("NN") ]
            
            Xlist_lemma_Verb=[word["lemma"] for word in Xdict_listsorted if str(word ["pos"]).startswith ("VB")and word["word"] not in Stop_List ]
            Xlist_word_Verb=[word["word"].lower() for word in Xdict_listsorted if str(word ["pos"]).startswith ("VB") and word["word"] not in Stop_List ]
            
            Xlist_lemma_Adj=[word["lemma"] for word in Xdict_listsorted if str(word ["pos"]).startswith ("JJ") ]
            Xlist_word_Adj=[word["word"].lower() for word in Xdict_listsorted if str(word ["pos"]).startswith ("JJ") ]
            
            NounListWord.extend(Xlist_word_Noun)
            VerbListWord.extend(Xlist_word_Verb)
            AdjListWord.extend(Xlist_word_Adj)
            
            NounListLemma.extend(Xlist_lemma_Noun)
            VerbListLemma.extend(Xlist_lemma_Verb)
            AdjListLemma.extend(Xlist_lemma_Adj)
            
        NounFreq=Counter(NounListWord) 
        AdjFreq=Counter(AdjListWord)  
        VerbFreq=Counter(VerbListWord) 
        Lines=[]
        NounFreq=NounFreq.most_common(20)
        AdjFreq=AdjFreq.most_common(20)
        VerbFreq=VerbFreq.most_common(20)
        for word in NounFreq:
            if word[0] not in Lines:
                Lines.append(word[0])
                Lines.append("\n")
        for word in AdjFreq:
            if word[0] not in Lines:
                Lines.append(word[0]) 
                Lines.append("\n")
        for word in VerbFreq:
            if word[0] not in Lines:
                Lines.append(word[0]) 
                Lines.append("\n")
        FileHandling.WriteTextFile(self.LIWC_words,Lines) 
                  
            
    
    
    def FreqDistTrainNLTKPOS(self): 
        DocumentLines=FileHandling.ReadTextFile(self.TrainingTextFile) 
        Document=" ".join(DocumentLines)
        sentences = nltk.sent_tokenize(Document)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences=[ word for word in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences] 
        NounListWord=[]
        VerbListWord=[]
        AdjListWord=[]
        for postuples in sentences:
            for postag in postuples:
                if (postag[1]).startswith("NN") and postag[0] not in Remove_List:
                    NounListWord.append(postag[0].lower())
                
                if (postag[1]).startswith("VB") and  postag[0] not in Stop_List:
                    VerbListWord.append(postag[0].lower())
                
                if (postag[1]).startswith("JJ") and postag[0] not in Remove_List: 
                    AdjListWord.append(postag[0].lower())        
             
        NounFreq=Counter(NounListWord) 
        AdjFreq=Counter(AdjListWord)  
        VerbFreq=Counter(VerbListWord) 
        Lines=[]
        NounFreq=NounFreq.most_common(20)
        AdjFreq=AdjFreq.most_common(20)
        VerbFreq=VerbFreq.most_common(20)
        for word in NounFreq:
            if word[0] not in Lines:
                Lines.append(word[0])
                Lines.append("\n")
        for word in AdjFreq:
            if word[0] not in Lines:
                Lines.append(word[0]) 
                Lines.append("\n")
        for word in VerbFreq:
            if word[0] not in Lines:
                Lines.append(word[0]) 
                Lines.append("\n")
        FileHandling.WriteTextFile(self.LIWC_words,Lines) 
                  
    
    
    def LIWCOverlap(self, row,NewRow):
        StringA=row["stringa_"]
        StringB=row["stringb_"]
        LIWCA=word_category_counter.score_text(StringA)
        LIWCB=word_category_counter.score_text(StringB)
        print LIWCA
        print LIWCB
        for category in FinalLIWC  :
            A_categ_count=LIWCA[category]
            B_categ_count=LIWCB[category]
            NewRow["LIWC_Catg_"+category]=min(A_categ_count,B_categ_count)
            
        
    
    def StanforDep_synsetPairs(self,row,NewRow):
       # print row["Input.stringb_"] 
        DepStringA=row["collapsedependencydictstringa_"]  
        DepStringB=row["collapsedependencydictstringb_"] 
        Word_DictA=row["Word_Dictstringa_"]
        Word_DictB=row["Word_Dictstringb_"]
        StringA=row["stringa_"]
        StringB=row["stringb_"]
        SubObjPairs_VerbPairs = GetCorrPair(DepStringA,StringA, Word_DictA,DepStringB,StringB,Word_DictB)
        return SubObjPairs_VerbPairs
    
    #------------------------------------------- def ExtractPOSWords(self,rows):
        #------------------------------------------------------ for row in rows:
            #------------------------- Word_DictA=row["Word_DictInput.stringa_"]
            #------------------------- Word_DictB=row["Word_DictInput.stringb_"]
            # NounList=[Word_Dict["word"] if str(Word_Dict["pos"]).startswith("NN") else ""]
            # VerbList=[Word_Dict["word"] if str(Word_Dict["pos"]).startswith("VB") else ""]
            # AdjList=[Word_Dict["word"] if str(Word_Dict["pos"]).startswith("RB")else ""]
            # AdjList=[Word_Dict["word"] if str(Word_Dict["pos"]).startswith("JJ") else "" ]
                  
    def DistCalc(self,SubPair,DistaneFeatureList,A_Word_Count, B_Word_Count,row,NewRow,dictfield):  
        Norm=np.log2(A_Word_Count) + np.log2(B_Word_Count)
        if Norm ==0:
            print " error norm =0"
            print " error in LCS sim " +"\n"+row["HITId"] + "\n"+row["stringa_"]
            sys.exit(0)
            
        simp_path=0
        sim_lch=0
        sim_wup=0
        sim_ic=0
        for synpair in SubPair:
            if "path" in DistaneFeatureList:
                New_sim=0
                New_sim=synpair[0].path_similarity(synpair[1])
                if New_sim is None:
                    New_sim=0 
                if New_sim==-1:
                    print " error in Path sim " +  synpair[0] + " , " +synpair[1] + "\n"+row["HITId"] + "\n"+row["stringa_"]
                    sys.exit(0)
                simp_path=simp_path+ New_sim   
            if "lch" in  DistaneFeatureList:
                    pos0=synpair[0]._pos
                    pos1=synpair[1]._pos
                    if str(pos0) == str(pos1):
                        New_sim=0
                        New_sim=synpair[0].lch_similarity(synpair[1])
                        if New_sim is None:
                            New_sim=0 
                        if New_sim==-1:
                            print " error in LCS sim " +  synpair[0] + " , " +synpair[1] + "\n"+row["HITId"] + "\n"+row["stringa_"]
                            sys.exit(0)
                    else:
                        New_sim=0       
                    sim_lch=sim_lch + New_sim    
            if "wup" in  DistaneFeatureList:
                    New_sim=0
                    New_sim= synpair[0].wup_similarity(synpair[1])
                    if New_sim is None:
                        New_sim=0 
                    if New_sim==-1:
                        print " error in WUP sim " +  synpair[0] + " , " +synpair[1] + "\n"+row["HITId"] + "\n"+row["stringa_"]
                        sys.exit(0)
                    sim_wup=sim_wup + New_sim  
#             if "jcs" in  DistaneFeatureList:
#                     New_sim=0  
#                     pos0=synpair[0]._pos 
#                     pos1=synpair[1]._pos
#                     if str(pos0) == str(pos1):
#                         New_sim= synpair[0].jcn_similarity(synpair[1], webtext_ic)
#                         if New_sim is None:
#                             New_sim=0 
#                         if New_sim==-1:
#                             print " error in IC sim " +  synpair[0] + " , " +synpair[1] + "\n"+row["HITId"] + "\n"+row["stringa_"]
#                             sys.exit(0)
#                     else:
#                         New_sim=0       
#                     sim_ic=sim_ic + New_sim
               
        simp_path_norm=simp_path
        NewRow[dictfield+"_Path"]  = simp_path_norm
     
#         sim_lch_norm=sim_lch/(Norm) 
#         row[dictfield+"_lch"]  = sim_lch_norm
#      
#         sim_wup_norm=sim_wup/(Norm) 
#         row[dictfield+"_wup"]  = sim_wup_norm
       
    
    def SynsetDistanceFeatures(self,row,NewRow):
        SubObjPairs_VerbPairs=self.StanforDep_synsetPairs(row,NewRow)
       # DistaneFeatureList=["path","lch","wup","res","jcs","lin"]
        DistaneFeatureList=["path"]
        SubPair=SubObjPairs_VerbPairs[0]
        VerbPair=SubObjPairs_VerbPairs[1]
        NNpair=SubObjPairs_VerbPairs[2]
        A_Word_Count=SubObjPairs_VerbPairs[3]
        B_Word_Count=SubObjPairs_VerbPairs[4]
        self.DistCalc(SubPair,DistaneFeatureList,A_Word_Count, B_Word_Count,row,NewRow,"noun")
        self.DistCalc(VerbPair,DistaneFeatureList,A_Word_Count, B_Word_Count,row,NewRow,"verb")
        #self.DistCalc(NNpair,DistaneFeatureList,A_Word_Count, B_Word_Count,row,NewRow,"nn")
        
        
    def Rougue(self,row,NewRow):
        r = Rouge155()
        writedir=os.getcwd() + "/Similarity_Data/gay-rights-debates/MTdata_cluster/Labels_Updated/Rougue/"
        count=0
        LinesA=list()
        StringA=NewFormat_text.ascii_only(row["stringa_"])
        Filename=writedir+"System/string_."+str(count)
        LinesA.append(StringA)
        FileHandling.WriteTextFile(Filename, LinesA)
        StringB=NewFormat_text.ascii_only(row["stringb_"])
        LinesB=list()
        LinesB.append(StringB)
        Filename=writedir+"Model/string_.A."+str(count)
        FileHandling.WriteTextFile(Filename, LinesB)
        r.system_dir = writedir+"System/"
        r.model_dir = writedir+"Model/"
        r.system_filename_pattern = 'string_.(\d+).txt'
        r.model_filename_pattern = 'string_.[A-Z].#ID#.txt'
        output = r.convert_and_evaluate()
      #  print(output)
        output_dict = r.output_to_dict(output)
        NewRow["rouge_1_f_score"]=output_dict["rouge_1_f_score"]
        NewRow["rouge_2_f_score"]=output_dict["rouge_2_f_score"]
        NewRow["rouge_3_f_score"]=output_dict["rouge_3_f_score"]
        NewRow["rouge_4_f_score"]=output_dict["rouge_4_f_score"]
        NewRow["rouge_l_f_score"]=output_dict["rouge_l_f_score"]
        NewRow["rouge_s*_f_score"]=output_dict["rouge_s*_f_score"]
        NewRow["rouge_su*_f_score"]=output_dict["rouge_su*_f_score"]
        NewRow["rouge_w_1.2_f_score"]=output_dict["rouge_w_1.2_f_score"]
        
    def WordDiff(self,row,NewRow):
        Word_DictA=row["Word_Dictstringa_"]
        Word_DictB=row["Word_Dictstringb_"]
        NewRow["diff_len"]=abs(sub(len(Word_DictA), len(Word_DictB)))
            
    
    def Distributionalsimilarity(self,row,NewRow): 
        Ext5Noun_a=(row["5ExtendedStringNounstringa_"]).split()
        lemmExt5Noun_a=list(set([lmtzr.stem(word) for word in Ext5Noun_a]))
        
        Ext5Noun_b=(row["5ExtendedStringNounstringb_"]).split()
        lemmExt5Noun_b=list(set([lmtzr.stem(word) for word in Ext5Noun_b]))
        
        Ext5Verb_a=(row["5ExtendedStringVerbstringa_"]).split()
        lemmExt5Verb_a=list(set([lmtzr.stem(word) for word in Ext5Verb_a]))
        
        Ext5Verb_b=(row["5ExtendedStringVerbstringb_"]).split()
        lemmExt5Verb_b=list(set([lmtzr.stem(word) for word in Ext5Verb_b]))
        
        Ext5Adj_a=(row["5ExtendedStringAdjstringa_"]).split()
        lemmExt5Adj_a=list(set([lmtzr.stem(word) for word in Ext5Adj_a]))
       
        Ext5Adj_b=(row["5ExtendedStringAdjstringb_"]).split()
        lemmExt5Adj_b=list(set([lmtzr.stem(word) for word in Ext5Adj_b]))
        
        #=======================================================================
        # row["ExtNounsim"]=self.ExtNVACosine(lemmExt5Noun_a, lemmExt5Noun_b)
        # row["ExtVerbsim"]=self.ExtNVACosine(lemmExt5Verb_a, lemmExt5Verb_b)
        # row["ExtAdjsim"]=self.ExtNVACosine(lemmExt5Adj_a, lemmExt5Adj_b)
        #=======================================================================
        stem_a=lemmExt5Noun_a+ lemmExt5Verb_a+ lemmExt5Adj_a
        stem_b=lemmExt5Noun_b+ lemmExt5Verb_b+ lemmExt5Adj_b
        NewRow["Dist_Sim_Noun"]=self.ExtNVACosine(lemmExt5Noun_a, lemmExt5Noun_b)
        NewRow["Dist_Sim_Verb"]=self.ExtNVACosine(lemmExt5Verb_a, lemmExt5Verb_b)
        NewRow["Dist_Sim_Adj"]=self.ExtNVACosine(lemmExt5Adj_a, lemmExt5Adj_b)
        
        
    def AddLabel(self,row,NewRow)  :
        NewRow["MeanSimLabel"]=row["SimLabel"]
     
     
    def sss(self,row, type_sim='relation', corpus='webbase'):
        sss_url = "http://swoogle.umbc.edu/SimService/GetSimilarity"
        try:
            s1=row["stringa_"]
            s2=row["stringb_"]
            response = get(sss_url, params={'operation':'api','phrase1':s1,'phrase2':s2,'type':type,'corpus':corpus})
            return float(response.text.strip())
        except:
            print response.raw
            print response.reason
            print 'Error in getting similarity for %s: %s' % ((s1,s2), response)
            print "filename_ "+ row["filename"]+ "id1_ " + row["id1"] + "id12_ " + row["id2"] +"\n"
            return 0.0
        
    def UMBCSIM(self,row): 
        type_sim='relation'
        corpus='webbase'
        sim= self.sss(row,type_sim,corpus)
        return sim 
        
    def AddUMBC(self,row,NewRow): 
        NewRow["UMBC"]=row["UMBC_"]
#         newUmbc=self.UMBCSIM(row)
#         NewRow["NEWUMBC"]=newUmbc
           
    def AddFeatures(self,row,NewRow):
        FeatureList=["UMBC","MeanSimilarityMT","LIWC","Ext_Dist","SynsetDistance","UnigramOverlap","bigramoverlap","LevDistance","Rougue", "worddiff"]
        
        
        if "LIWC" in FeatureList:
            self.LIWCOverlap(row,NewRow)
        
        if "Ext_Dist" in FeatureList:
            self.Distributionalsimilarity(row,NewRow)
        
        if "worddiff" in FeatureList:
            self.WordDiff(row,NewRow)
        
        
        if   "UnigramOverlap"  in FeatureList:
            ngram=["1","2","3"]
            self.ngramOverlap(row,NewRow,ngram)
        if "Rougue" in FeatureList:
            self.Rougue(row,NewRow) 
        if "SynsetDistance" in FeatureList:
            print
            self.SynsetDistanceFeatures(row,NewRow)
        
        if  "bigramCosine"   in FeatureList:
            print
            self.bigramCosine(row,NewRow);
        if "LCS" in FeatureList:
            KeepSubVerbObj=True
            self.LCS(row, KeepSubVerbObj)
        if "LevDistance" in FeatureList:
            KeepSubVerbObj=True
            self.LevDistance(row,NewRow, KeepSubVerbObj)  
        if  "MeanSimilarityMT" in FeatureList:
            self.AddLabel(row,NewRow)
        if   "UMBC" in FeatureList:
            self.AddUMBC(row,NewRow) 
        if goldstandard==True:
            NewRow["gold"]=row["Id_A2TNNKHFNY5WQ4"]  
        
                
            
        #return row        
             
def createLIWCCategory(Featuresobj):  
    global FinalLIWC   
    AllLIWC_WordsList=FileHandling.ReadTextFile(Featuresobj.LIWC_words+".txt")
    LIWC_WordsList=[ word for word in AllLIWC_WordsList if word not in  LIWC_StopList ]
    LIWCstring=" ".join( LIWC_WordsList)
    LIWCCategory_counter=word_category_counter.score_text(LIWCstring)
    print LIWCCategory_counter
    keys=LIWCCategory_counter.keys()
    FinalLIWC= [ word for word in keys if word not in NotToUseCategory]
             
    
def Execute(Featuresobj) :
    #Featuresobj.FreqDistTrainNLTKPOS() #do this once to create top liwc pos words
    
    
    createLIWCCategory(Featuresobj)
    Allrowdicts=list()
    Allrow_string=list()
    rows=Featuresobj.ReadJson() 
    
    for row in rows:
        Row_withString=dict()
        NewRow=dict()
       
        Featuresobj.AddFeatures(row,NewRow)
        Row_withString= deepcopy(NewRow)
        Row_withString["stringa"]=row["stringa_"]
        Row_withString["stringb"]=row["stringb_"]
        
        
        Allrowdicts.append(NewRow)
        Allrow_string.append(Row_withString)
        
    fieldnames=sorted(Allrowdicts[0].keys())    
    csv_wrapper.write_csv(Featuresobj.FeatureFile, Allrowdicts) 
    #shuffle(Allrowdicts)
    csv_wrapper.write_csv(Featuresobj.RandomizeFeatureFile,Allrow_string)
       
        
if __name__ == '__main__':
    Stop_List = set(stopwords.words('english'))
    Remove_List=["(",")"]
    stem=True
    lmtzr= SnowballStemmer("english")
    #webtext_ic = wn.ic(webtext,False,0) # @UndefinedVariable
    
    topic="gay-rights-debates"
    TrainingLIWC="/Users/amita/git/summary_repo/Summary/src/Similarity_Labels/Similarity_Data/CD_Convince_Forums_taining_gayrightsText.txt"
    LIWC_words=os.getcwd() + "/Similarity_Data/gay-rights-debates/MTdata_cluster/Labels_Updated/TopLIWC_category_words"
    LIWC_Category=os.getcwd() + "/Similarity_Data/gay-rights-debates/MTdata_cluster/Labels_Updated/TopLIWC_category"
    Input_withdistSim=os.getcwd()+ "/Similarity_Data/gay-rights-debates/MTdata_cluster/Labels_Updated/AllMT_task/Results/ExtDist5_NVA_CoreNLP_AllMT_Reg.json"
   
    goldstandard=False
    
     # RandomizeFeatureFile=os.getcwd() + "/Similarity_Data/gay-rights-debates/MTdata_cluster/Labels_Updated/AllMT_task/ResultsGold/Rand_FeatureFileAllMT_Reg.csv"
    # # FeatureFile=os.getcwd() + "/Similarity_Data/gay-rights-debates/MTdata_cluster/Labels_Updated/AllMT_task/ResultsGold/FeatureFileAllMT_Reg.csv"
    # # InputCSvwithdistSim=os.getcwd()+ "/Similarity_Data/gay-rights-debates/MTdata_cluster/Labels_Updated/AllMT_task/ResultsGold/ExtDist5_NVA_CoreNLP_AllMT_Reg"
# #------------------------------------------------------------------------------
    
    FeatureFile=os.getcwd() + "/Similarity_Data/gay-rights-debates/MTdata_cluster/Labels_Updated/AllMT_task/Results/FeatureFileAllMT_Reg.csv"
    InputCSvwithdistSim=os.getcwd()+ "/Similarity_Data/gay-rights-debates/MTdata_cluster/Labels_Updated/AllMT_task/Results/ExtDist5_NVA_CoreNLP_AllMT_Reg"
    StringFeatureFile=os.getcwd() + "/Similarity_Data/gay-rights-debates/MTdata_cluster/Labels_Updated/AllMT_task/Results/String_FeatureFileAllMT_Reg.csv"
    
    
    convert_jsonobjects_tocsv(Input_withdistSim,InputCSvwithdistSim)
    Featuresobj=Features(Input_withdistSim, LIWC_words, LIWC_Category,FeatureFile,StringFeatureFile,TrainingLIWC)
    #Featuresobj=Features(Input_withdistSim, LIWC_words, LIWC_Category,FeatureFile,TrainingLIWC)
    Execute(Featuresobj)
   
    pass