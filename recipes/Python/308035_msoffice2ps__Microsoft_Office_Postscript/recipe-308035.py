import win32com.client, time, pythoncom

"""
Makes a Postscriptfile from Word-, Excel- or Powerpoint-Files.

usage:
* make_ps.word(wordfilename, psfilename, ps_printername)
* make_ps.excel(excelfilename, psfilename, ps_printername)
* make_ps.powerpoint(powerpointfilename, psfilename, ps_printername)

http://win32com.goermezer.de/content/view/156/192/
"""

def word(wordfile, psfile, printer):
    pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)
    myWord = win32com.client.DispatchEx('Word.Application')
    myWord.Application.ActivePrinter = printer
    myDoc = myWord.Documents.Open(wordfile, False, False, False)
    myDoc.Saved=1
    myWord.Application.NormalTemplate.Saved = 1
    myWord.PrintOut(True, False, 0, psfile)
    while myWord.BackgroundPrintingStatus > 0:
        time.sleep(0.1)
    myDoc.Close()
    myWord.Quit()
    del myDoc
    del myWord
    pythoncom.CoUninitialize()

def excel(excelfile, psfile, printer):
    pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)
    myExcel = win32com.client.DispatchEx('Excel.Application')
    myExcel.Application.AskToUpdateLinks = 0
    Excel = myExcel.Workbooks.Open(excelfile, 0, False, 2)
    Excel.Saved = 1
    Excel.PrintOut(1, 5000, 1, False, printer, True, False, psfile)
    Excel.Close()
    myExcel.Quit()
    del myExcel
    del Excel
    pythoncom.CoUninitialize()

def powerpoint(powerpointfile, psfile, printer):
    pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)
    myPowerpoint = win32com.client.DispatchEx('Powerpoint.Application')
    # myPowerpoint.Visible = 0 # doesn`t work for PowerPoint
    myPpt = myPowerpoint.Presentations.Open(powerpointfile, False, False, False)
    myPpt.PrintOptions.PrintInBackground = 0
    myPpt.PrintOptions.ActivePrinter = printer
    myPpt.Saved = 1
    myPpt.PrintOut(1, 5000, psfile, 0, False)
    myPpt.Close()
    #myPowerpoint.Quit()
    del myPpt
    del myPowerpoint
    pythoncom.CoUninitialize()
