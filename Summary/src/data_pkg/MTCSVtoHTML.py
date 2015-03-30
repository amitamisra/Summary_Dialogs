'''
Created on Nov 13, 2014

@author: amita
'''
from data_pkg import FileHandling
def ReadRows(inputcsv):
    rows=FileHandling.read_csv(inputcsv)
    return rows
def Format(rows,noofitems):
    Lines=list()
    for row in rows:
        for count in range (1,noofitems+1):
            Lines.append("<br>")
            Lines.append("<br><b>Key</b>")
            Lines.append(row["key"+ str(count)])
            Lines.append("<br><b>Dialogtext</b>")
            Lines.append(row["Dialogtext" + str(count)])
            
            
            
    return Lines

def WriteHtml(outputfile,lines):
    f = open(outputfile +".html",'w')
    all_lines=" ".join(lines)
    all_lines= """<html><head></head><body>""" + all_lines +"""</body> </html>"""  
    f.write(all_lines)    
    f.close()
def Execute(InputCsv,OutHTML,noofitems):
    rows=ReadRows(InputCsv)
    FormattedLines=Format(rows,noofitems)
    WriteHtml(OutHTML, FormattedLines)
    
    

        
        
if __name__ == '__main__':
    InputCsv="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/MTdata/MT2/MT2_midrange"
    OutHTML="/Users/amita/git/summary_repo/Summary/src/data_pkg/CSV/gay-rights-debates/MTdata/MT2/MT2_midrange"
    noofitems=5
    Execute(InputCsv,OutHTML,noofitems)
    