from win32com.client import Dispatch
class ExcelTable:
    """
    display a data structure in Excel
    """
    def __init__(self):
        self.xlApp = Dispatch("Excel.Application")
        self.xlApp.Visible = 1
        self.xlApp.Workbooks.Add()

    def Display(self,InputList,StartRow=1,StartColumn=1):
        """
        Display a Grid of data in excel
        Input list = List of (row,col,value)  to describe your data 
        StartRow,StartColumn - the place where to start to draw you table in excel. 

        """
        self.List=InputList
        for x in self.List:
            self.xlApp.ActiveSheet.Cells(x[0]+StartRow,x[1]+StartColumn).Value =str(x[2])
    
    def __del__(self):
        self.xlApp.ActiveWorkbook.Close(SaveChanges=0)
        self.xlApp.Quit()
        del self.xlApp
