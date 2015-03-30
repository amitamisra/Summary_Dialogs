import Tkinter as tk
import tkFont
'''
Created on Sep 23, 2014
A text widget with a new method, HighlightPattern 

    example:

    text = CustomText()
    text.tag_configure("red",foreground="#ff0000")
    text.HighlightPattern("this should be red", "red")

    The highlight_pattern method is a simplified python 
    version of the tcl code at http://wiki.tcl.tk/3246
    
@author: amita
'''
class CustomText(tk.Text):
    
    def __init__(self,text):
        tk.Text.__init__(self)
        self.insert(tk.INSERT ,text)

    def highlight_pattern(self, pattern, tag, start="1.0", end="end", regexp=False):
        '''Apply the given tag to all text that matches the given pattern

        If 'regexp' is set to True, pattern will be treated as a regular expression
        '''

        start = self.index(start)
        end = self.index(end)
        self.mark_set("matchStart",start)
        self.mark_set("matchEnd",start)
        self.mark_set("searchLimit", end)

        countVar = tk.StringVar()
        while True:
            
            index = self.search("car", stopindex="end", count=countVar)
            if index == "": break
            self.mark_set("matchStart", index)
            self.mark_set("matchEnd", "%s+%sc" % (index,countVar.get()))
            self.tag_add(tag, "matchStart","matchEnd")

   
if __name__ == '__main__':
    text = CustomText("this should be red")
    text.tag_configure("red",foreground="#ff0000")
    text.highlight_pattern("this should be red", "red")
 