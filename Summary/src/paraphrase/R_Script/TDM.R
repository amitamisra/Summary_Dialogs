options( stringsAsFactors=F ) 
library(NLP,lib.loc="/Users/amita/software/Rpackage") 
library(SnowballC,lib.loc="/Users/amita/software/Rpackage")
library(tm,lib.loc="/Users/amita/software/Rpackage") #load text mining library
library(MASS,lib.loc="/Users/amita/software/Rpackage")
library(stringi,lib.loc="/Users/amita/software/Rpackage")

setwd("~/git/summary_repo/Summary/src/paraphrase/data/gay-rights-debates/") #sets R's working directory to near where my files are
filelist=list.files("TDM_Dir/TDM_Inp")
for (inputfile in filelist)
{ 
  inputfile
  inpfile=paste("TDM_Dir/TDM_Inp/",inputfile, sep="")
  inpfile
  SCU_df<-read.csv(file=inpfile,head=TRUE,sep=",")
  SCU_df[1]
  SCU_df[2]
  map<-list(content="SCU",id="id")
  myReader <- readTabular(mapping = map)
  scu_Corpus <- VCorpus(DataframeSource(SCU_df), readerControl = list(reader = myReader))
  scu_Corpus
  meta(scu_Corpus[[3]])
  scu_Corpus<- tm_map(scu_Corpus , stripWhitespace)
  scu_Corpus<- tm_map(scu_Corpus, content_transformer(tolower))
  scu_Corpus <- tm_map(scu_Corpus, removeWords, c(stopwords("english"),"s1","s2")) # this stopword file is at C:\Users\[username]\Documents\R\win-library\2.13\tm\stopwords 
  
  scu_dtm_tf <-DocumentTermMatrix(scu_Corpus)
  scu_dtm_tfidf<-DocumentTermMatrix(scu_Corpus,control = list(weight = weightTfIdf))
  dim(scu_dtm_tf)
  
  scu_df_tf<-as.matrix(scu_dtm_tf)
  outfile_tf=paste("TDM_Dir/TDM_TF/",inputfile, sep="")
  
  scu_df_tfidf<-as.matrix(scu_dtm_tfidf)
  outfile_tfidf=paste("TDM_Dir/TDM_TFIDF/",inputfile, sep="")
  
  write.csv(scu_df_tf, outfile_tf)
  write.csv(scu_df_tfidf, outfile_tfidf)
}