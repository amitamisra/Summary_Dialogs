
options( stringsAsFactors=F ) 
library(NLP,lib.loc="/Users/amita/software/Rpackage") 
library(SnowballC,lib.loc="/Users/amita/software/Rpackage")
library(tm,lib.loc="/Users/amita/software/Rpackage") #load text mining library
library(MASS,lib.loc="/Users/amita/software/Rpackage")

setwd("~/git/summary_repo/Summary/src/topic_modeling/topic_data/gay-rights-debates/") #sets R's working directory to near where my files are

inputfile="1-8171_3_2__4_5_7_11_1"
#inputfile="1-5342_11_8__13_16_21_22_1"
#inputfile ="1-6229_6_5__7_8_9_16_26_29_46_47_48_2"
#inputfile="1-4350_46_31__54_59_66_69_1"

user="_user5"
corpusfile=paste("modeling_input/sent_inp/",inputfile,"/",sep="")
scufile=paste(inputfile,user,sep="")
scufile
corpusfile
sentoutfile=paste("modeling_output/sent_out/",scufile,"/Topic_sentdoc_likely.csv", sep="")
scuoutfile=paste("modeling_output/sent_out/",scufile,"/Topic_scu_likely.csv", sep="")
posteriorfile=paste("modeling_output/sent_out/",scufile,sep="")
a  <-Corpus(DirSource(corpusfile), readerControl = list(reader=readPlain)) #specifies the exact folder where my text file(s) is for analysis with tm.
#summary(a)  #check what went in
a <- tm_map(a, removeNumbers)
a <- tm_map(a, removePunctuation)
a <- tm_map(a , stripWhitespace)
a <- tm_map(a, content_transformer(tolower))
a <- tm_map(a, removeWords, stopwords("english")) # this stopword file is at C:\Users\[username]\Documents\R\win-library\2.13\tm\stopwords 
astem <- tm_map(a, stemDocument,language = "english")
adtm <-DocumentTermMatrix(astem)
dim(adtm)
rowTotals <- apply(adtm , 1, sum) #Find the sum of words in each Document
adtm.new <- adtm[rowTotals> 0, ]
library(topicmodels,lib.loc="/Users/amita/software/Rpackage")
SCU_Csv_File<-read.csv(file="modeling_input/Scus_weights.csv",,head=TRUE,sep=",")
idcol=grep("id_topic_contrib", colnames(SCU_Csv_File))
#idcol
rownames(SCU_Csv_File) <- SCU_Csv_File[,7]
#dimnames(SCU_Csv_File)
#SCU_Csv_File[1,2]
scu_user<-SCU_Csv_File[grep(scufile, SCU_Csv_File$key_user, ignore.case=T),]
scu_user_wt<-scu_user[scu_user$weight>2,]
ids<-scu_user_wt$id
ids
k<-length(unique(ids))
k
SEED<-2010
jss_TM <- list(VEM = LDA(adtm.new, k = k, control = list(seed = SEED)), VEM_fixed = LDA(adtm.new, k = k,control = list(estimate.alpha = FALSE, seed = SEED)),Gibbs = LDA(adtm.new, k = k, method = "Gibbs",control = list(seed = SEED, burnin = 1000, thin = 100, iter = 1000)),CTM = CTM(adtm.new, k = k, control = list(seed = SEED, var = list(tol = 10^-4), em = list(tol = 10^-3))))
sapply(jss_TM[1:2], slot, "alpha")
sapply(jss_TM, function(x)
  +   + mean(apply(posterior(x)$topics,
                   +                + 1, function(z) - sum(z * log(z)))))
Topic_CTM <- topics(jss_TM[["CTM"]])
#str(Topic_CTM)
Terms_CTM <- terms(jss_TM[["CTM"]], 5)
#Terms_CTM[,1:14]
#Topic_frame_CTM<-data.frame(Topic_CTM,names(Topic_CTM), stringsAsFactors=FALSE)


Topic_VEM <- topics(jss_TM[["VEM"]], 1)
Terms_VEM <- terms(jss_TM[["VEM"]], 5)
#Terms_VEM[,1:14]
#Topic_frame_VEM<-data.frame(Topic_VEM,names(Topic_VEM), stringsAsFactors=FALSE)

Topic_Gibbs <- topics(jss_TM[["Gibbs"]], 1)
Terms_Gibbs <- terms(jss_TM[["Gibbs"]], 5)
#Terms_Gibbs[,1:14]
Topic_frame<-data.frame(Topic_VEM,names(Topic_VEM),Topic_Gibbs,names(Topic_Gibbs), Topic_CTM,names(Topic_CTM),stringsAsFactors=FALSE)
write.csv(Topic_frame,sentoutfile )


random_scu_user_wt=scu_user_wt[sample(nrow(scu_user_wt)),]
#dimnames(scu_user_wt)
#scu_wt_contrib<-scu_user_wt[,c('contrib')]
#scu_wt_contrib
#scu_topic_contrib<-scu_user_wt[,c('topic_contrib_str')]
map<-list(content="topic_contrib_str",id="id_topic_contrib")
myReader <- readTabular(mapping = map)
scu_topic_Corpus <- VCorpus(DataframeSource(random_scu_user_wt), readerControl = list(reader = myReader))
#<- VCorpus(VectorSource(scu_user_wt$topic_contrib_str))
#str(scu_topic_Corpus)
scu_topic_Corpus <- tm_map(scu_topic_Corpus, removeNumbers)
scu_topic_Corpus<- tm_map(scu_topic_Corpus, removePunctuation)
scu_topic_Corpus<- tm_map(scu_topic_Corpus , stripWhitespace)
scu_topic_Corpus<- tm_map(scu_topic_Corpus, content_transformer(tolower))
scu_topic_Corpus <- tm_map(scu_topic_Corpus, removeWords, stopwords("english")) # this stopword file is at C:\Users\[username]\Documents\R\win-library\2.13\tm\stopwords 
scu_topic_Corpus <- tm_map(scu_topic_Corpus, stemDocument,language="english")

#str(scu_topic_Corpus)
"id"
meta(scu_topic_Corpus[[1]])
scu_topic_dtm <-DocumentTermMatrix(scu_topic_Corpus)
str(scu_topic_dtm)
#write.table(scu_topic_dtm,paste(posteriorfile,"/SCU_dtm.csv",sep=""))
dim(scu_topic_dtm)
#str(scu_topic_dtm)
rowTotals_scu <- apply(scu_topic_dtm , 1, sum) #Find the sum of words in each Document
scu_topic_dtm.new <- scu_topic_dtm[rowTotals_scu> 0, ]
library(topicmodels,lib.loc="/Users/amita/software/Rpackage")
SEED<-2010
scu_topic_TM <- list(VEM = LDA(scu_topic_dtm.new, k = k, control = list(seed = SEED)), VEM_fixed = LDA(scu_topic_dtm.new, k = k,control = list(estimate.alpha = FALSE, seed = SEED)),Gibbs = LDA(scu_topic_dtm.new, k = k, method = "Gibbs",control = list(seed = SEED, burnin = 1000, thin = 100, iter = 1000)),CTM = CTM(scu_topic_dtm.new, k = k, control = list(seed = SEED, var = list(tol = 10^-4), em = list(tol = 10^-3))))

sapply(scu_topic_TM , function(x)
  +   + mean(apply(posterior(x)$topics,
                   +                + 1, function(z) - sum(z * log(z)))))
Topic_CTM_Manual <- topics(scu_topic_TM [["CTM"]])
#Topic_CTM_Manual
Terms_CTM_Manual <- terms(scu_topic_TM [["CTM"]], 5)
#Terms_CTM_Manua[,1:14]
#Topic_frame_CTM_Manual<-data.frame(Topic_CTM_Manual,names(Topic_CTM_Manual), stringsAsFactors=FALSE)

Topic_VEM_Manual <- topics(scu_topic_TM [["VEM"]], 1)
Terms_VEM_Manual <- terms(scu_topic_TM [["VEM"]], 5)
#Terms_VEM_Manual[,1:14] 
#Topic_frame_VEM_Manual<-data.frame(Topic_VEM_Manual,names(Topic_VEM_Manual), stringsAsFactors=FALSE)

Topic_Gibbs_Manual <- topics(scu_topic_TM [["Gibbs"]], 1)
#Topic_Gibbs_Manual
Terms_Gibbs_Manual <- terms(scu_topic_TM [["Gibbs"]], 5)
#Terms_Gibbs_Manual[,1:14]

Term_Frame_SCU<-data.frame(Terms_CTM_Manual,Terms_VEM_Manual, Terms_Gibbs_Manual,stringsAsFactors=FALSE)
colnames(Term_Frame_SCU)[1:k]<- paste("CTM_SCU", colnames(Term_Frame_SCU)[1:k], sep = "_")
colnames(Term_Frame_SCU)[k+1:k*2]<-paste("VEM_SCU", colnames(Term_Frame_SCU)[k+1:k*2], sep = "_")
colnames(Term_Frame_SCU)[((k*2)+1):(k*3)]<-paste("Gibbs_SCU", colnames(Term_Frame_SCU)[((k*2)+1):(k*3)], sep = "_")
#Term_Frame_SCU
Topic_frame_SCU<-data.frame(Topic_CTM_Manual,names(Topic_CTM_Manual),Topic_VEM_Manual,names(Topic_VEM_Manual),Topic_Gibbs_Manual,names(Topic_Gibbs_Manual), stringsAsFactors=FALSE)
Sorted_Topic_Scu<-Topic_frame_SCU[order(names(Topic_CTM_Manual)),] 
write.csv(Sorted_Topic_Scu,scuoutfile )
CTMposterior_SCU<-posterior(scu_topic_TM [["CTM"]])
CTM_SCU_Posterior_terms<-data.frame(CTMposterior_SCU$terms,stringsAsFactors=FALSE)
CTM_SCU_Posterior_doc<-data.frame(CTMposterior_SCU$topics,stringsAsFactors=FALSE)
#attributes(CTM_SCU_Posterior_doc)
Sorted_CTM_SCU_Posterior_doc<- CTM_SCU_Posterior_doc[order(row.names(CTM_SCU_Posterior_doc)),] 
write.csv(CTM_SCU_Posterior_terms,paste(posteriorfile,"/CTM_TermDist.csv",sep=""))
write.csv(Sorted_CTM_SCU_Posterior_doc,paste(posteriorfile,"/CTM_DocDist.csv",sep=""))
write.csv(Term_Frame_SCU,paste(posteriorfile,"/Top_Terms.csv",sep=""))