'''
Created on Aug 31, 2014
Reads the file  para_data/gay-rights-debates/cluster/Summaries/InputStrings_ParseTrees.json , created from cornlp
 containing parse trees from stanford parser.
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


class DrawParseTrees:
    
    def __init__(self,ParseTreeJson,TreePics,DepPath):
        self.ParseTreeJson=ParseTreeJson
        self.TreePics=TreePics
        self.DepPath=DepPath

    def ReadList(self):
        RowDicts=FileHandling.jsontorowdicts(self.ParseTreeJson)
        return RowDicts
    def AddTreePS(self,Row_Json,field):
        cf = CanvasFrame()
        
        tree=Tree.fromstring(Row_Json[field])
        treecanvas = TreeWidget(cf.canvas(),tree)
        #canvas_id = cf.canvas.create_text(10, 10, anchor="nw")
        #cf.canvas.itemconfig(canvas_id, text="this is the text")
        # cf.insert(canvas_id, 12, "new ")
        cf.add_widget(treecanvas,30,10) # (10,10) offsets
        return cf
    
    
    def DrawtoFile(self,cf,count,dirpath,field):
        
        cf.print_to_file(dirpath+ field +"_"+str(count)+'.ps')
        
    def DrawTrees(self,rowdicts):
        #count=0
        rowdicts.sort(key=operator.itemgetter("key"))
        for key, items in itertools.groupby(rowdicts, operator.itemgetter('key')):
            grouprows=list(items)
            for row in grouprows:
                #count=count+1
                keypath=self.TreePics + row["key"] 
                if not os.path.exists(keypath):
                    os.mkdir(keypath)
                dirpath= keypath+"/"+ "Sent" +"_"+row["Sent_No"] 
                countArg=row["Arg_No"]    
                canvastree=self.AddTreePS(row,"Parse_TreesParsed_Argument")
                collapseddependencyArg=row["collapsedependencyParsed_Argument"]
                basicdependencyArg=row["BasicdependencyParsed_Argument"]
                FileHandling.WriteTextFile(dirpath+"_Arg"+countArg+"_CollapseDep", collapseddependencyArg)
                FileHandling.WriteTextFile(dirpath+"_Arg"+countArg+"_BasicDep", basicdependencyArg)
                self.DrawtoFile(canvastree,countArg,dirpath, "Args")
                canvastree.destroy()
                count_sent=row["Sent_No"]
                canvastree=self.AddTreePS(row,"Parse_TreesSent",)
                self.DrawtoFile(canvastree,count_sent,dirpath,"Sent" )
                canvastree.destroy()
                
            
    def DrawTreesDepSeq(self,rowdicts):
        count=0
        for row in rowdicts:
            count=count+1
            dirpathDep=self.DepPath
            if not os.path.exists(dirpathDep):
                os.mkdir(dirpathDep)
                
            canvastree=self.AddTreePS(row,"Parse_TreesParsed_Argument")
            collapsedependencyArg=row["collapsedependencyParsed_Argument"]
            basicdependencyArg=row["BasicdependencyParsed_Argument"]
            FileHandling.WriteTextFile(dirpathDep +"_CollapseArg"+str(count), collapsedependencyArg)
            FileHandling.WriteTextFile(dirpathDep +"_BasicArg"+str(count), basicdependencyArg) 
            canvastree.print_to_file(dirpathDep +"_Arg"+str(count)+'.ps')
            canvastree.destroy()
            




#===============================================================================
# tokens = word_tokenize(s)
# tagged = pos_tag(tokens)
# entities = ne_chunk(tagged)
# entities
#===============================================================================



t = Tree.fromstring("(ROOT (S (NP (NN marriage)) (VP (VBZ is) (VP (VBN defined) (PP (IN as) (NP (DT a) (NN family) (NN unit))) (PP (VBN based) (PP (IN on) (NP (DT a) (JJ heterosexual) (NN contract)))))) (. .)))")
# s1 = '(ROOT (S (NP (NN S2)) (VP (VBZ argues) (SBAR (IN that) (S (NP (DT the) (JJ religious) (NN freedom) (NN argument)) (VP (MD could) (VP (VB be) (VP (VBN used) (PP (IN in) (NP (DT any) (NN format))) (S (VP (TO to) (VP (VB justify) (NP (DT any) (NN action))))))))))) (. .)))'
# s2='(ROOT (S (NP (NN S2)) (ADVP (RB seemingly)) (VP (VBZ corrects) (NP (NN S1)) (PP (IN by) (S (VP (VBG noting) (SBAR (IN that) (S (NP (NP (DT the) (NNPS States)) (PP (IN in) (NP (NN question)))) (VP (VBD had) (RB not) (VP (VB put) (NP (DT the) (NN issue)) (PP (TO to) (NP (NP (DT the) (JJ general) (NN public)) (PP (IN for) (NP (DT a) (NN vote))))))))))))) (. .)))'
#----------------------------------------------------------------- t2 = Tree(s2)
# s3="(ROOT (SBARQ (WHADVP (WRB How)) (SQ (MD will) (NP (NNS states)) (VP (VB use) (NP (NP (DT the) (NN choice)) (PP (IN of) (NP (NN law) (NN doctrine)))) (SBAR (IN so) (IN that) (S (NP (DT the) (NNP FFC) (NN clause)) (VP (VBZ does) (RB not) (VP (VB apply))))))) (. ?)))"
#------------------------------------------------------------------- t3=Tree(s3)
s="(ROOT (S (NP (NN S1)) (VP (VBZ contends) (SBAR (S (NP (NN he\/she)) (VP (VP (VBZ does) (RB not) (VP (VB hate) (NP (NNS gays)))) (CC but) (VP (VBZ does) (RB n't) (VP (VB feel) (SBAR (S (NP (NN marriage)) (VP (MD should) (VP (VB be) (VP (VBN redefined) (S (VP (TO to) (VP (VB allow) (SBAR (IN for) (S (NP (PRP them)) (VP (TO to) (VP (VB wed.))))))))))))))))))) (. .))), (ROOT (S (NP (NN S2)) (VP (VBZ feels) (SBAR (S (NP (NP (NP (NN S1) (POS 's)) (NN objection)) (PP (TO to) (NP (NP (NP (NNS gays)) (CC and) (NP (DT the) (NN family) (POS 's))) (SBAR (S (NP (PRP they)) (VP (MD would) (VP (VB make)))))))) (VP (VBZ is) (NP (NN prejudice)))))) (. .)))"


print "Convert bracketed string into tree:"

s=""" (ROOT
  (S
    (NP (NNP S1))
    (VP
      (VP (VBZ refutes)
        (NP
          (NP (DT this) (NN assertion))
          (, ,)
          (VP (VBG citing)
            (NP
              (NP (DT a) (NN number))
              (PP (IN of)
                (NP
                  (NP (NNS countries))
                  (SBAR
                    (WHNP (WDT which))
                    (S
                      (VP
                        (VP (VBP recognize)
                          (NP (JJ same-sex) (NN marriage)))
                        (CC and)
                        (VP (VBZ compares)
                          (NP
                            (NP (DT the) (NN lack))
                            (PP (IN of)
                              (NP
                                (NP (JJ reproductive) (NN potential))
                                (PP (IN for)
                                  (NP (JJ homosexual) (NNS couples))))))
                          (PP (TO to)
                            (NP (DT a) (JJ heterosexual) (NN couple)))))))))
              (SBAR
                (WHNP (WDT that))
                (S
                  (VP (VBZ chooses)
                    (S (RB not)
                      (VP (TO to)
                        (VP (VB have)
                          (NP (NNS children))))))))))))
      (CC or)
      (VP (VBZ is)
        (ADJP (JJ unable)
          (S
            (VP (TO to)
              (VP (VB have)
                (NP (NNS children))))))))
    (. .)))"""


s=""" (ROOT
  (S
    (NP (NNP S2))
    (VP (VBZ cites)
      (NP (DT the) (NN fact))
      (SBAR (IN that)
        (S
          (NP (JJ gay) (NN marriage))
          (VP
            (VP (VBZ is)
              (ADVP (RB already))
              (VP (VBN allowed)
                (PP (IN in)
                  (NP (JJ many) (NNS countries)))))
            (CC and)
            (VP (VBZ feels)
              (SBAR
                (S
                  (NP (PRP it))
                  (ADVP (RB soon))
                  (VP (MD will)
                    (VP (VB be)
                      (PP (IN in)
                        (NP
                          (NP (DT the) (NN state))
                          (PP (IN of)
                            (NP (NNP Massachusetts))))))))))))))
    (. .))) """
#s="(ROOT(S(NP (PRP$ My) (JJ favorite) (NNS colors))(VP (VBP are)(ADJP (JJ blue)(CC and)(JJ green)))(. .)))"
s= """ (ROOT (S (NP (NNP S1)) (VP (VBZ begins) (NP (DT the) (NN dialog)) (PP (IN by) (S (VP (VBG stating) (SBAR (IN that) (S (NP (PRP he)) (VP (VBZ supports) (NP (DT the) (NN right) (S (VP (TO to) (VP (VP (VB own)) (, ,) (VP (VB carry) (PP (IN in) (NP (JJS most) (NNS places)))) (, ,) (CC and) (VP (VB use) (NP (NP (NNS guns)) (PP (IN for) (NP (NN self-defense)))))))))))))))) (. .))) """
s=""" (ROOT (S (NP (NNP S1)) (VP (VP (VBZ is) (VP (VBN offended))) (CC and) (VP (VBZ asks) (S (NP (NNP S2)) (VP (TO to) (VP (VB discontinue) (NP (DT the) (NNS attacks))))))) (. .))) """
s=""" (ROOT (S (NP (NNP S2)) (VP (VBZ questions) (SBAR (WHADVP (WRB how)) (S (NP (NNP S1)) (VP (MD can) (VP (VP (VB be) (ADJP (JJ pro-gun))) (CC and) (VP (VB support) (NP (NN encroachment)) (PP (IN upon) (NP (NP (DT the) (NNS policies)) (PP (IN of) (NP (DT the) (NN right) (S (VP (TO to) (VP (VB bear) (NP (NNS arms))))))))))))))) (. .))) """ 
s=""" (ROOT (S (NP (NNP S2)) (VP (VBZ cites) (NP (DT the) (NN fact)) (SBAR (IN that) (S (S (NP (JJ gay) (NN marriage)) (VP (VBZ is) (ADVP (RB already)) (VP (ADVP (RB in)) (VBN allowed) (PP (IN in) (NP (JJ many) (NNS countries)))))) (CC and) (S (ADVP (RB soon)) (NP (PRP it)) (VP (MD will) (VP (VB be) (PP (IN in) (NP (NP (DT the) (NN state)) (PP (IN of) (NP (NNP Austin))))))))))))) """
s=""" (ROOT (S (NP (PRP He)) (ADVP (RB also)) (VP (VBZ agrees) (SBAR (IN that) (S (NP (EX there)) (VP (MD should) (VP (VB be) (NP (NP (NNS restrictions)) (PP (IN on) (SBAR (WHNP (WP who)) (S (VP (MD can) (VP (VB carry))))))) (, ,) (SBAR (WHADVP (WRB where)) (S (NP (NNS individuals)) (VP (MD can) (VP (VB carry)))))))))) (. .))) """
s=""" (ROOT (S (NP (NNP S2)) (VP (VBZ challenges) (S (NP (NNP S1)) (VP (TO to) (VP (VB explain) (SBAR (WHADVP (WRB how)) (S (NP (PRP he)) (VP (VBZ is) (NP (JJ pro-gun) (NNS rights)) (SBAR (IN if) (S (NP (PRP he)) (ADVP (RB also)) (VP (VBZ wants) (S (VP (TO to) (VP (VB place) (NP (NNS limits)) (PP (IN on) (NP (DT those) (NNS rights)))))))))))))))) (. .))) """
#t=Tree(s)
#t.draw()
s=""" (ROOT (S (NP (NP (DT The) (NN question)) (SBAR (IN if) (S (NP (PRP it)) (VP (VBZ is) (ADJP (JJ okay) (S (VP (TO to) (VP (VB have) (NP (DT a) (JJ nuclear) (NN weapon)))))))))) (VP (VBZ is) (VP (VBN asked))) (. .))) """
if __name__ == '__main__':
    topic="gay-rights-debates"
    tt=Tree.fromstring(s)
    tt.draw()
    ParseTreeJson=os.path.dirname(os.getcwd()) + "/Parser_Pkg/Parserdata/"+topic+ "/Summaries/InputStrings_ParseTrees.json" 
    TreePics=os.path.dirname(os.getcwd()) + "/Parser_Pkg/Parserdata/"+topic+ "/Summaries/TreePics/" 
    DepPath=os.path.dirname(os.getcwd()) + "/Parser_Pkg/Parserdata/"+topic+ "/Summaries/Tree_Dependency_Seq/"
    DrawParseTreeObj=DrawParseTrees(ParseTreeJson,TreePics,DepPath)
    rowdicts=DrawParseTreeObj.ReadList()
    DrawParseTreeObj.DrawTrees(rowdicts)
    DrawParseTreeObj.DrawTreesDepSeq(rowdicts)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
#===============================================================================
#     
#     
#     s="(ROOT(S(SBAR (IN After)(S(NP (PRP I))(VP (VBD went)(PP (TO to)(NP (DT the) (NN store))))))(, ,)(NP (PRP I))(VP (VBD went)(NP (NN home)))))"
# s= """(ROOT(S(S(NP (NNP NASA))(VP (MD wo) (RB n't)(VP (VB attempt)(NP (DT a) (NN rescue)))))(: ;)
#     (S(ADVP (RB instead))(, ,)(NP (PRP it))(VP (MD will)(VP (VB try)(S(VP (TO to)(VP (VB predict)(SBAR (SBAR (IN whether)
#     (S(NP(NP (DT any))(PP (IN of)(NP (DT the) (NN rubble))))(VP (MD will)(VP (VB smash)(PP (TO to)(NP (DT the) (NN ground)))))))
#     (CC and)(SBAR(WHADVP (WRB where))))))))))(. .)))"""
# s="""(ROOT(S(NP (PRP It))(VP (VBZ 's)(NP(NP (DT the) (JJ petulant) (NN complaint))(PP (IN of)(NP (DT an) (JJ impudent) (NNP American)))(SBAR(WHNP (WP whom))(S(NP (NNP Sony))(VP (VBD hosted)(PP (IN for) (NP (DT a) (NN year)))(SBAR (IN while)(S
# (NP (PRP he))(VP (VBD was)(PP (IN on)(NP(NP (DT a) (NNP Luce) (NNP Fellowship))(PP(PP (IN in)(NP (NNP Tokyo)))
# (: --)(PP (TO to)(NP(NP (DT the) (NN regret))(PP (IN of)(NP (DT both) (NNS parties))))))))))))))))))"""
# 
# s= """Workers described clouds of blue dust that hungover parts of the factory even though exhaust fans ventilated the air."""
# s="""(ROOT(S(NP (NNPS Workers))(VP (VBD described)(NP(NP (`` ``)(NP (NNS clouds))(PP (IN of)(NP (JJ blue) (NN dust)))('' ''))
#  (SBAR(WHNP (WDT that))(S(VP (VBD hung)(PP (IN over)(NP(NP (NNS parts))(PP (IN of)(NP (DT the) (NN factory)))))(SBAR (RB even) (IN though)(S(NP (JJ exhaust) (NNS fans)) (VP (VBD ventilated)(NP (DT the) (NN air))))))))))))"""
# 
# 
# s=""" (ROOT (S (NP (NP (DT The) (JJ average) (NN maturity)) (PP (IN for) (NP (NNS funds)))) (VP (VBP open) (ADVP (RB only)) (PP (TO to) (NP (NP (NNS institutions)) (, ,) (VP (VBN considered) (PP (IN by) (NP (DT some))) (S (VP (TO to) (VP (VB be) (NP (DT a) (JJR stronger) (NN indicator)) (SBAR (IN because) (S (NP (DT those) (NNS managers)) (VP (VBP watch) (NP (DT the) (NN market)) (ADVP (RB closely))))))))) (, ,) (VP (VBN reached) (NP (NP (NP (DT a) (JJ high) (NN point)) (PP (IN for) (NP (DT the) (NN year)))) (: --) (NP (CD 33) (NNS days))))))) (. .))) """
#     
# s=""" (ROOT (S (SBAR (IN Since) (S (NP (DT the) (NN budget)) (VP (VBZ measures) (NP (NN cash) (NN flow))))) (, ,) (NP (DT a) (JJ new) (ADJP ($ $) (CD 1)) (JJ direct) (NN loan)) (VP (VBZ is) (VP (VBN treated) (PP (IN as) (NP (DT a) (ADJP ($ $) (CD 1)) (NN expenditure))))) (. .)))"""
# s="(ROOT(S(NP (PRP He))(VP (VBD wiped)(NP (DT the) (NN counter)))(. .)))"
# 
# s="The current distribution arrangement ends in March 1990, although Delmed said it will continue to provide some supplies of the peritoneal dialysis productsto National Medical, the spokeswoman said."
# s="""(ROOT
#   (S
#     (S
#       (NP (DT The) (JJ current) (NN distribution) (NN arrangement))
#       (VP (VBZ ends)
#         (PP (IN in)
#           (NP (NNP March) (CD 1990)))
#         (, ,)
#         (SBAR (IN although)
#           (S
#             (NP (NNP Delmed))
#             (VP (VBD said)
#               (SBAR
#                 (S
#                   (NP (PRP it))
#                   (VP (MD will)
#                     (VP (VB continue)
#                       (S
#                         (VP (TO to)
#                           (VP (VB provide)
#                             (NP
#                               (NP (DT some) (NNS supplies))
#                               (PP (IN of)
#                                 (NP (DT the) (JJ peritoneal) (NN dialysis) (NNS products))))
#                             (PP (TO to)
#                               (NP (NNP National) (NNP Medical)))))))))))))))
#     (, ,)
#     (NP (DT the) (NN spokeswoman))
#     (VP (VBD said))
#     (. .)))"""
#     
# s="Advocates said the 90-cent-an-hour rise, to $4.25 an hour by April 1991, is too small for the working poor, while opponents argued that the increase will still hurt small business and cost many thousands of jobs."    
# s="""(ROOT
#   (SINV
#     (S
#       (NP (NNS Advocates))
#       (VP (VBD said)
#         (NP (DT the) (JJ 90-cent-an-hour) (NN rise))
#         (, ,)
#         (PP (TO to)
#           (NP
#             (NP ($ $) (CD 4.25))
#             (NP (DT an) (NN hour))))
#         (PP (IN by)
#           (NP (NNP April) (CD 1991)))))
#     (, ,)
#     (VP (VBZ is)
#       (ADJP (RB too) (JJ small)
#         (PP (IN for)
#           (NP (DT the) (JJ working) (NN poor))))
#       (, ,)
#       (SBAR (IN while)
#         (S
#           (NP (NNS opponents))
#           (VP (VBD argued)
#             (SBAR (IN that)
#               (S
#                 (NP (DT the) (NN increase))
#                 (VP (MD will)
#                   (ADVP (RB still))
#                   (VP (VB hurt)
#                     (NP (JJ small) (NN business)
#                       (CC and)
#                       (NN cost))))))))))
#     (NP
#       (NP (JJ many) (NNS thousands))
#       (PP (IN of)
#         (NP (NNS jobs))))
#     (. .)))"""
# 
# s="She became an abortionist accidentally, and continued because it enabled her to buy jam, cocoa and other war-rationed goodies." 
# s=""" (ROOT
#   (S
# #===============================================================================
    #------------------------------------------------------------ (NP (PRP She))
    #----------------------------------------------------------------------- (VP
      #-------------------------------------------------------- (VP (VBD became)
        #----------------------------------------- (NP (DT an) (NN abortionist))
        #--------------------------------------------- (ADVP (RB accidentally)))
      #------------------------------------------------------------------- (, ,)
      #---------------------------------------------------------------- (CC and)
      #----------------------------------------------------- (VP (VBD continued)
        #---------------------------------------------------- (SBAR (IN because)
          #------------------------------------------------------------------ (S
            #----------------------------------------------------- (NP (PRP it))
            #------------------------------------------------- (VP (VBD enabled)
              #-------------------------------------------------------------- (S
                #------------------------------------------------ (NP (PRP her))
                #--------------------------------------------------- (VP (TO to)
                  #------------------------------------------------ (VP (VB buy)
                    #----------------------------- (NP (NN jam) (, ,) (NN cocoa)
                      #------------------------------------------------ (CC and)
                      #----- (JJ other) (NN war-rationed) (NNS goodies))))))))))
    #---------------------------------------------------------------- (. .)))"""
#------------------------------------------------------------------------------ 
# s="Longer maturities are thought to indicate declining interest rates because they permit portfolio managers to retain relatively higher rates for a longer period."
#-------------------------------------------------------------------- s="""(ROOT
  #-------------------------------------------------------------------------- (S
    #---------------------------------------- (NP (JJR Longer) (NNS maturities))
    #------------------------------------------------------------- (VP (VBP are)
      #------------------------------------------------------- (VP (VBN thought)
        #-------------------------------------------------------------------- (S
          #--------------------------------------------------------- (VP (TO to)
            #------------------------------------------------- (VP (VB indicate)
              #------------------ (NP (VBG declining) (NN interest) (NNS rates))
              #---------------------------------------------- (SBAR (IN because)
                #------------------------------------------------------------ (S
                  #--------------------------------------------- (NP (PRP they))
                  #-------------------------------------------- (VP (VBP permit)
                    #-------------------------------------------------------- (S
                      #---------------------- (NP (NN portfolio) (NNS managers))
                      #--------------------------------------------- (VP (TO to)
                        #--------------------------------------- (VP (VB retain)
                          #------------------------------------------------- (NP
                            #----------------------------------------------- (NP
                              #------------- (ADJP (RB relatively) (JJR higher))
                              #------------------------------------ (NNS rates))
                            #-------------------------------------- (PP (IN for)
                              # (NP (DT a) (JJR longer) (NN period)))))))))))))))
    #------------------------------------------------------------------- (. .)))
#------------------------------------------------------------------------------ 
#--------------------------------------------------------------------------- """
#------------------------------------------------------------------------------ 
#-------- s="(S (NP-SBJ Casey) (VP should (VP have (VP thrown (NP the ball)))))"
#------------------------------------------------------------------------------ 
#------------------------------------ s="My favorite colors are blue and green."
# s="(ROOT (S (NP (PRP$ My) (JJ favorite) (NNS colors)) (VP (VBP are) (ADJP (JJ blue) (CC and) (JJ green))) (. .))) "
# s="(S1 (S (NP (PRP$ My) (JJ favorite) (NNS colors)) (VP (AUX are) (ADJP (JJ red) (CC and) (JJ green))) (. .)))"
#------------------------------------- s="After I went to the store,I went home"
# s="(ROOT (S (SBAR (IN After) (S (NP (PRP I)) (VP (VBD went) (PP (TO to) (NP (DT the) (NN store)))))) (, ,) (NP (PRP I)) (VP (VBD went) (NP (NN home)))))"
# s="(ROOT (S (SBAR (IN After#0#Temporal) (S (NP (PRP I)) (VP (VBD went) (PP (TO to) (NP (DT the) (NN store)))))) (, ,) (NP (PRP I)) (VP (VBD went) (NP (NN home))))) "
#------------------------------------------------------------------------------ 
# s=""" S1 refutes this assertion , citing a number of countries which recognize same-sex marriage and compares the lack of reproductive potential for homosexual couples to a heterosexual couple that chooses not to have children or is unable to have children .
#--------------------------------------------------------------------------- """
# s=" (ROOT (S (NP (NNP S1)) (VP (VP (VBZ refutes) (NP (NP (DT this) (NN assertion)) (, ,) (VP (VBG citing) (NP (NP (DT a) (NN number)) (PP (IN of) (NP (NP (NNS countries)) (SBAR (WHNP (WDT which)) (S (VP (VP (VBP recognize) (NP (JJ same-sex) (NN marriage))) (CC and) (VP (VBZ compares) (NP (NP (DT the) (NN lack)) (PP (IN of) (NP (NP (JJ reproductive) (NN potential)) (PP (IN for) (NP (JJ homosexual) (NNS couples)))))) (PP (TO to) (NP (DT a) (JJ heterosexual) (NN couple))))))))) (SBAR (WHNP (WDT that)) (S (VP (VBZ chooses) (S (RB not) (VP (TO to) (VP (VB have) (NP (NNS children)))))))))))) (CC or) (VP (VBZ is) (ADJP (JJ unable) (S (VP (TO to) (VP (VB have) (NP (NNS children)))))))) (. .))) "
# s=""" (ROOT (S (NP (NNP S1)) (VP (VP (VBZ refutes) (NP (NP (DT this) (NN assertion)) (, ,) (VP (VBG citing) (NP (NP (DT a) (NN number)) (PP (IN of) (NP (NP (NNS countries)) (SBAR (WHNP (WDT which)) (S (VP (VP (VBP recognize) (NP (JJ same-sex) (NN marriage))) (CC and#0#0) (VP (VBZ compares) (NP (NP (DT the) (NN lack)) (PP (IN of) (NP (NP (JJ reproductive) (NN potential)) (PP (IN for#1#0) (NP (JJ homosexual) (NNS couples)))))) (PP (TO to) (NP (DT a) (JJ heterosexual) (NN couple))))))))) (SBAR (WHNP (WDT that)) (S (VP (VBZ chooses) (S (RB not) (VP (TO to) (VP (VB have) (NP (NNS children)))))))))))) (CC or#2#0) (VP (VBZ is) (ADJP (JJ unable) (S (VP (TO to) (VP (VB have) (NP (NNS children)))))))) (. .))) """
#------------------------------------------------------ s=""" (Elaboration[N][S]
  #--------------------- _!S2 claims that marriage is defined as a family unit!_
  #------------------------------ _!based on a heterosexual contract . <s>!_)"""
    