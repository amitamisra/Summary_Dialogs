browser()
options( stringsAsFactors=FALSE) 
library(lpSolve,lib.loc="/Users/amita/software/Rpackage") 
library(irr,lib.loc="/Users/amita/software/Rpackage") 
setwd("~/git/summary_repo/Summary/src/Similarity_Labels/Similarity_Data/gay-rights-debates/MTdata_cluster/Labels_Updated/AllMT_task/") #sets R's working directory to near where my files are

InputFile<-"Results/ExtDist5_NVA_CoreNLP_AllMT_Reg.csv"

warnings() 
mytable<-read.csv(InputFile,header=TRUE,stringsAsFactors=FALSE)
dim(mytable)
class(mytable)

table.sub2 <- subset(mytable, select = c(Id_A142ZRU284W9O:Id_ASK5ZTC22VRZZ))
dim(table.sub2)
mat=data.matrix(table.sub2)
aplha<-kripp.alpha(t(mat),"ordinal")
aplha
aplha_nom<-kripp.alpha(t(mat))
aplha_nom
