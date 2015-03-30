browser()
options( stringsAsFactors=FALSE) 
library(lpSolve,lib.loc="/Users/amita/software/Rpackage") 
library(irr,lib.loc="/Users/amita/software/Rpackage") 
#setwd("~/git/summary_repo/Summary/src/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/") #sets R's working directory to near where my files are

#InputFile<-"~/git/summary_repo/Summary/src/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task3/task3_oneitem.csv" # second task file with all 630 pairs
#InputFile<-"~/git/summary_repo/Summary/src/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/MT_task3/task3_oneitem_UMBCTop500.csv" # second task file with all 500 pairs

InputFile<-"~/git/summary_repo/Summary/src/paraphrase/para_data/gay-rights-debates/cluster/LabelUpdated/TFIdf/Pairs_Cos_Cluster_70_AVG_Noun_Verb_Ad.csv" # File with all 1131 pairs
warnings() 
mytable<-read.csv(InputFile,header=TRUE,stringsAsFactors=FALSE)
dim(mytable)
class(mytable)
hist(mytable$UMBC ,col ="pink",breaks=14,main="Histogram with Normal Curve",xlab="Pairs distribution for all pairs in the dataset")
#table.sub2 <- subset(mytable, select = c(UMBC_))
