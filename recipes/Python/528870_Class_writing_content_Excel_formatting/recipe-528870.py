from win32com.client import Dispatch
import os

STYLE_HEADING1 = "style_heading1"
STYLE_HEADING2 = "style_heading2"
STYLE_BORDER_BOTTOM = "style_border_bottom"
STYLE_GREY_CELL = "style_grey_cell"
STYLE_PALE_YELLOW_CELL = "style_pale_yellow_cell"
STYLE_ITALICS = "style_italics"

#these are the constant values in one particular version of EXCEL - if having problems, check your own
XL_CONST_EDGE_LEFT = 7
XL_CONST_EDGE_BOTTOM = 9
XL_CONST_CONTINUOUS = 1
XL_CONST_AUTOMATIC = -4105
XL_CONST_THIN = 2
XL_CONST_GRAY16 = 17
XL_CONST_SOLID = 1

RGB_PALE_GREY = 15132390 #Debug.Print RGB(230,230,230) in Excel Immediate window
RGB_PALE_YELLOW = 13565951 # RGB(255,255,206)

class ExcelWriter(object):
    """Excel class for creating spreadsheets - esp writing data and formatting them
    Based in part on #http://snippets.dzone.com/posts/show/2036,
    and http://www.markcarter.me.uk/computing/python/excel.html
    """
    def __init__(self, file_name, default_sheet_name, make_visible=False):
        """Open spreadsheet"""
        self.excelapp = Dispatch("Excel.Application")
        if make_visible:
            self.excelapp.Visible = 1 #fun to watch!
        self.excelapp.Workbooks.Add()
        self.workbook = self.excelapp.ActiveWorkbook
        self.file_name = file_name
        self.default_sheet = self.excelapp.ActiveSheet
        self.default_sheet.Name = default_sheet_name
    
    def getExcelApp(self):
        """Get Excel App for use"""
        return self.excelapp
    
    def addSheetAfter(self, sheet_name, index_or_name):
        """
        Add new sheet to workbook after index_or_name (indexing starts at 1).
        """
        sheets = self.workbook.Sheets
        sheets.Add(None, sheets(index_or_name)).Name = sheet_name #Sheets.Add(Before, After, Count, Type) - http://www.functionx.com/vbaexcel/Lesson07.htm
    
    def deleteSheet(self, sheet_name):
        """Delete named sheet"""
        #http://www.exceltip.com/st/Delete_sheets_without_confirmation_prompts_using_VBA_in_Microsoft_Excel/483.html
        sheets = self.workbook.Sheets
        self.excelapp.DisplayAlerts = False        
        sheets(sheet_name).Delete()        
        self.excelapp.DisplayAlerts = True
        
    def getSheet(self, sheet_name):
        """
        Get sheet by name.
        """
        return self.workbook.Sheets(sheet_name)
    
    def activateSheet(self, sheet_name):
        """
        Activate named sheet.
        """
        sheets = self.workbook.Sheets
        sheets(sheet_name).Activate() #http://mail.python.org/pipermail/python-win32/2002-February/000249.html
    
    def add2cell(self, row, col, content, sheet=None):
        """
        Add content to cell at row,col location.  
        NB only recommended for small amounts of data http://support.microsoft.com/kb/247412.
        """
        if sheet == None:
            sheet = self.default_sheet
        sheet.Cells(row,col).Value = content

    def addRow(self, row_i, data_tuple, start_col=1, sheet=None):
        """
        Add row in a single operation.  Takes a tuple per row.
        Much more efficient than cell by cell. http://support.microsoft.com/kb/247412.
        """
        if sheet == None:
            sheet = self.default_sheet  
        col_n = len(data_tuple)
        last_col = start_col + col_n - 1
        insert_range = self.getRangeByCells((row_i, start_col), (row_i, last_col), sheet)
        insert_range.Value = data_tuple
        
    def addMultipleRows(self, start_row, list_data_tuples, start_col=1, sheet=None):
        """
        Adds data multiple rows at a time, not cell by cell. Takes list of tuples
        e.g. cursor.fetchall() after running a query
        One tuple per row.
        Much more efficient than cell by cell or row by row. 
        http://support.microsoft.com/kb/247412.
        Returns next available row.
        """
        if sheet == None:
            sheet = self.default_sheet
        row_n = len(list_data_tuples)
        last_row = start_row + row_n - 1
        col_n = len(list_data_tuples[0])
        last_col = start_col + col_n - 1        
        insert_range = self.getRangeByCells((start_row, start_col), (last_row, last_col), sheet)
        insert_range.Value = list_data_tuples
        next_available_row = last_row + 1
        return next_available_row

    def getRangeByCells(self, (cell_start_row, cell_start_col), (cell_end_row, cell_end_col), sheet=None):
        """Get a range defined by cell start and cell end e.g. (1,1) A1 and (7,2) B7"""
        if sheet == None:
            sheet = self.default_sheet
        return sheet.Range(sheet.Cells(cell_start_row, cell_start_col), 
            sheet.Cells(cell_end_row, cell_end_col))
    
    def fitCols(self, col_start, col_end, sheet=None):
        """
        Fit colums to contents.
        """
        if sheet == None:
            sheet = self.default_sheet
        col_n = col_start
        while col_n <= col_end:
            self.fitCol(col_n, sheet)
            col_n = col_n + 1
    
    def fitCol(self, col_n, sheet=None):
        """
        Fit column to contents.
        """
        if sheet == None:
            sheet = self.default_sheet
        sheet.Range(sheet.Cells(1, col_n), sheet.Cells(1, col_n)).EntireColumn.AutoFit()
    
    def setColWidth(self, col_n, width, sheet=None):
        """
        Set column width.
        """
        if sheet == None:
            sheet = self.default_sheet
        sheet.Range(sheet.Cells(1, col_n), sheet.Cells(1, col_n)).ColumnWidth = width        
        
    def formatRange(self, range, style):
        """
        Add formatting to a cell/group of cells.
        To get methods etc record a macro in EXCEL and look at it.
        To get the value of Excel Constants such as xlEdgeLeft (7) or xlThin (2)
        type e.g. Debug.Print xlEdgeLeft in the Immediate window of the VBA editor and press enter.
        http://www.ureader.com/message/33389340.aspx
        For changing the pallete of 56 colours ref: http://www.cpearson.com/excel/colors.htm    
        """
        if style == STYLE_HEADING1:
            range.Font.Bold = True
            range.Font.Name = "Arial"
            range.Font.Size = 12
        elif style == STYLE_HEADING2:
            range.Font.Bold = True
            range.Font.Name = "Arial"
            range.Font.Size = 10.5
        elif style == STYLE_BORDER_BOTTOM:
            range.Borders(XL_CONST_EDGE_BOTTOM).LineStyle = XL_CONST_CONTINUOUS
            range.Borders(XL_CONST_EDGE_BOTTOM).Weight = XL_CONST_THIN
            range.Borders(XL_CONST_EDGE_BOTTOM).ColorIndex = XL_CONST_AUTOMATIC
        elif style == STYLE_GREY_CELL:
            self.resetColorPallet(1, RGB_PALE_GREY)
            range.Interior.ColorIndex = 1
            range.Interior.Pattern = XL_CONST_SOLID
        elif style == STYLE_PALE_YELLOW_CELL:
            self.resetColorPallet(1, RGB_PALE_YELLOW)
            range.Interior.ColorIndex = 1
            range.Interior.Pattern = XL_CONST_SOLID
        elif style == STYLE_ITALICS:
            range.Font.Italic = True
        else:
            raise Exception, "Style '%s' has not been defined" % style        

    def resetColorPallet(self, color_index, color):
        """
        Reset indexed color in pallet (limited to 1-56).
        Get color values by Debug.Print RGB(230,230,230) in Excel Immediate window
        """
        if color_index < 1 or color_index > 56:
            raise Exception, "Only indexes between 1 and 56 are available in the Excel color pallet."
        colors_tup = self.workbook.Colors #immutable of course
        colors_list = list(colors_tup)
        colors_list[color_index-1] = RGB_PALE_GREY #zero-based in list but not Excel pallet
        new_colors_tup = tuple(colors_list)
        self.workbook.Colors = new_colors_tup

    def mergeRange(self, range):
        """Merge range"""
        range.Merge()

    def save(self):
        """Save spreadsheet as filename - wipes if existing"""
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
        self.workbook.SaveAs(self.file_name)

    def close(self):
        """Close spreadsheet resources"""
        self.workbook.Saved = 0 #p.248 Using VBA 5
        self.workbook.Close(SaveChanges=0) #to avoid prompt
        self.excelapp.Quit()
        self.excelapp.Visible = 0 #must make Visible=0 before del self.excelapp or EXCEL.EXE remains in memory.
        del self.excelapp
