'''
Created on Sep 16, 2014

@author: amita
'''
from nltk import Tree
from nltk.draw.util import CanvasFrame
from nltk.draw import TreeWidget
from data_pkg import FileHandling
import os
from  nltk import word_tokenize
from nltk import pos_tag
from nltk.chunk import ne_chunk
import os
import operator
import itertools
from paraphrase import Parse_Tree_Manipulation

import os
class Nenkova:
    def __init__(self,ParseTreeJson,ParsedTreeSentDir,DiscourseAddedTrees,DiscourseTreePics):
        self.ParseTreeJson=ParseTreeJson
        self.ParsedTreeSentDir=ParsedTreeSentDir
        self.DiscourseAddedTrees=DiscourseAddedTrees
        self.DiscourseTreePics=DiscourseTreePics

    def ReadList(self):
        RowDicts=FileHandling.jsontorowdicts(self.ParseTreeJson)
        return RowDicts
    def WriteTrees(self,RowDicts):
        for row in RowDicts:
            Lines=list()
            outfile=self.ParsedTreeSentDir + "sent_"+ str(row["sent_No"])
            Lines.append( row["Parse_TreesSent"])
            FileHandling.WriteTextFile(outfile, Lines)
    
    def Draw(self,): 
        filelist=os.listdir(self.DiscourseAddedTrees)
        for filename in filelist:
            if str(filename).startswith("."):
                continue
            TextLines= FileHandling.ReadTextFile(self.DiscourseAddedTrees +filename)
            rowdict=dict()
            rowdict["text"]=TextLines[0]
            
            TreeObj =Parse_Tree_Manipulation.DrawParseTrees(self.DiscourseAddedTrees,self.ParsedTreeSentDir)
            cf=TreeObj.AddTreePS(rowdict, "text")
            cf.print_to_file(self.DiscourseTreePics+filename+".ps")
            
            
          
def Execute(NenkovaTreeObj):
    #RowDicts=NenkovaTreeObj.ReadList()
    #NenkovaTreeObj.WriteTrees(RowDicts)
    NenkovaTreeObj.Draw()
    
    
if __name__ == '__main__':
    
    topic="gay-rights-debates"
    ParseTreeJson=os.path.dirname(os.getcwd()) + "/Parser_Pkg/Parserdata/"+topic+ "/StringInput/InputStrings_ParseTrees.json" 
    ParsedTreeDir=os.path.dirname(os.getcwd()) + "/Parser_Pkg/Parserdata/"+topic+ "/StringInput/Nenkova/ParsedTrees/" 
    DiscourseAddedTrees=os.path.dirname(os.getcwd()) + "/Parser_Pkg/Parserdata/"+topic+ "/StringInput/Nenkova/DiscourseAddedTrees/"
    DiscourseTreePics=os.path.dirname(os.getcwd()) + "/Parser_Pkg/Parserdata/"+topic+ "/StringInput/Nenkova/DiscourseTreePics/"
    NenkovaObj=Nenkova(ParseTreeJson,ParsedTreeDir,DiscourseAddedTrees,DiscourseTreePics)
    Execute(NenkovaObj)