"""
Created on Tue Dec 15 20:30:51 2015

@author: awang
"""

def ExcelReadtoList():
     import tkinter as tk
     from tkinter import filedialog
     
     root = tk.Tk()
     root.withdraw()

     F = filedialog.askopenfilename()
     
     import xlwings as xw
     
     wb = xw.Workbook(F)
     
     Results={}
     Result={}
     
     endRow=500
     endCol=100
     
     sheetNo=1
     
     while True:
         try:
             carrier=xw.Sheet(sheetNo).name
             Results[carrier]=xw.Range(sheetNo,(1,1),(endRow,endCol)).value
             maxCol=1
             for i in range(0,endRow):
                 countCol=endCol-1
                 for j in range(endCol-1,-1,-1): 
                     if Results[carrier][i][j]!=None:
                         break
                     else:
                         countCol-=1
                 if maxCol<countCol:
                    maxCol=countCol
             maxRow=1
             for i in range(0,endCol):
                countRow=endRow-1
                for j in range(endRow-1,-1,-1):
                    if Results[carrier][j][i]!=None:
                        break
                    else:
                        countRow-=1
                if maxRow<countRow:
                    maxRow=countRow
                    
             Result[carrier]=xw.Range(sheetNo,(1,1),(maxRow+1,maxCol+1)).value
                 
             sheetNo+=1
         except:
             wb.close()   
             print('Completed!\nBe noted maximum of %d rows and %d columns have been tested!!!' % (endRow,endCol))
             return Result
