browser()
options( stringsAsFactors=FALSE) 
library(lpSolve,lib.loc="/Users/amita/software/Rpackage") 
library(irr,lib.loc="/Users/amita/software/Rpackage") 
setwd("~/git/summary_repo/Summary/src/MechanicalTurk/gay-rights-debates/MTdata_cluster/Labels_Updated/") #sets R's working directory to near where my files are
#InputFile<-"MT_task3/Results/MT_Task3_split_worker.csv"

# InputFile<-"MT_task2/ResultsV3/MT2_web_interface_split_worker.csv"

#InputFile<-"AllMT_task/Results/MT_Task2_3split_worker.csv"

#InputFile<-"MT_task4/Results/MT_Task4_split_worker.csv"
#InputFile<-"AllMT_task/Results/MT_Task3_4split_worker.csv"

InputFile<-"AllMT_task/Results/MT_2_4_3_5_split_worker.csv"

warnings() 
mytable<-read.csv(InputFile,header=TRUE,stringsAsFactors=FALSE)
dim(mytable)
class(mytable)

# OutputFile<-"MT_task3/Results/MT_Task3_split_worker_Corr.csv"
# table.sub2 <- subset(mytable, select = c(Input.UMBC_,WorkerId_A1FBBY2JJYRMRI_Response:WorkerId_ASK5ZTC22VRZZ_Response))
# sink("MT_task3/Results/MT_Task3_split_worker.txt")



# table.sub2 <- subset(mytable, select = c(Input.UMBC_,WorkerId_A1GDPTVUU6KVC3_Response:WorkerId_ADUJUZANFOWKW_Response))
# OutputFile<-"MT_task2/ResultsV3/MT2_web_interface_split_workerCorr.csv"
# sink("MT_task2/ResultsV3/MT2_web_interface_split_worker.txt")
# total=500



# OutputFile<-"AllMT_task/Results/MT_Task2_3split_worker_Corr.csv"
# table.sub2 <- subset(mytable, select = c(Input.UMBC_,WorkerId_A1FBBY2JJYRMRI_Response:WorkerId_ASK5ZTC22VRZZ_Response))
# sink("AllMT_task/Results/MT_Task2_3split_worker.txt")
# total=1000

# OutputFile<-"MT_task4/Results/MT_Task4_split_worker_Corr.csv"
# table.sub2 <- subset(mytable, select = c(Input.UMBC_,WorkerId_A142ZRU284W9O_Response:WorkerId_AZ0C38Q5UJFT8_Response))
# sink("MT_task4/Results/MT_Task4_split_worker.txt")
# total=500


# OutputFile<-"AllMT_task/Results/MT_Task3_4split_worker_Corr.csv"
# table.sub2 <- subset(mytable, select = c(UMBC_,Id_A142ZRU284W9O:Id_AZ0C38Q5UJFT8))
# sink("AllMT_task/Results/MT_Task3_4split_worker.txt")
# total=1000



OutputFile<-"AllMT_task/Results/MT_2_4_3_5_split_worker_Corr.csv"
table.sub2 <- subset(mytable, select = c(Id_A142ZRU284W9O:UMBC_))
sink("AllMT_task/Results/MT_2_4_3_5_split_worker.txt")
total=1000



ncolm<-ncol(table.sub2)
ncolm

for(i in names(table.sub2)){
  targetColumn <- table.sub2[,i]
  len<-length(targetColumn[is.na(targetColumn)])
  cat(i)
  cat("\t")
  cat(total-len)
  cat("\n\n")
   
}
sink()
names(table.sub2)
class(table.sub2)
corr<-cor(table.sub2,use="pairwise.complete.obs")
write.csv(corr,OutputFile)
          
                