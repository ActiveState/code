"""
WSA - browser tool
Author: Robert Marchetti
Site: http://pamie.sourceforge.net
Date: July 1, 2004
Description: Allows user to find any "OPEN" browser window and automate it.
I make no warranties for cWSA.py
Tested against XP and Win2000 with Python 2.34 and Win32All
Use at your own risk!

"""

import win32com.client
import time

class WSA:

    def __init__(self):
        """ Constructor """

        clsid='{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'
        
        ## Set new instance of the shellwindow as sw
        self._sw = win32com.client.Dispatch(clsid)
        """ Create new instance """
        print 'Window Found:',self._sw

    def Navigate(self,wintext,url):
        """ This function Navigates to the url 
            parameters:
                wintext - title of the window
                url - url to go to
        """            
        self._ie.Navigate(url)

         
    def GetElemNames(self, wintext,formname):
        """ This function gets the element names from the form
            parameters:
                wintext - title of the window
                winnum - url to go to
                formname - Name or number of form
        """
        for i in range(self._sw.Count): ## Count windows
            if i is None:
                print 'No Open Windows Found'
                break
            time.sleep(.2) ## may have to play with this value
            print i
            wn = self._sw[i].LocationName ## Get the window Title
            print wn
            ## checks to see if location matches the name
            if wn == wintext:
                form = self._sw[i].Document.forms[formname]
                count = 0
                while count < form.elements.length:
                    elements = form.elements[count]
                    count +=1
                    name = elements.name
                    print 'Following elements found: ',name
                   
    # Works for List box also
    def SetText(self, wintext,element,value,frmname): #Win Title as Param
        """ This function sets the text in a textbox """
        for i in range(self._sw.Count): ## Count windows
            if i is None:
                print 'No Open Windows Found'
                break
            time.sleep(.2) ## may have to play with this value
            print i
            wn = self._sw[i].LocationName ## Get the window Title
            print wn
            ## checks to see if location matches the name
            if wn == wintext: 
                print "sw[", i, "]" ## print the win number
                win = self._sw[i].LocationName ## Get the window Title
                print "Window name: ", win 
    
                try:
                    self._sw[i].Document.forms[frmname].elements[element].value= value
                    print 'textbox value set to: ', value

                except:
                    print 'SetText Failed'
    
    def CloseWin(self, wintext):
        """ This function closes a window"""
        for i in range(self._sw.Count): ## Count windows
            if i is None:
                print 'No Open Windows Found'
                break
            time.sleep(.2) ## may have to play with this value
            wn = self._sw[i].LocationName ## Get the window Title
            
            ## checks to see if location matches the name
            if wn == wintext:
                try:
                    self._sw[i].quit()
                    print "Closed Window"
                except:
                    print 'CloseWin failed to close the window'
                
    
    def ClickButton(self,wintext,element,frmname): #Win Title as Param
        """ This function clicks a button"""
        for i in range(self._sw.Count): ## Count windows
            if i is None:
                print 'No Open Windows Found'
                break
            time.sleep(.2) ## may have to play with this value
            wn = self._sw[i].LocationName ## Get the window Title
            
            ## checks to see if location matches the name
            if wn == wintext: 
                print "sw[", i, "]" ## print the win number
                win = self._sw[i].LocationName ## Get the window Title
                print "Window name: ", win 
    
                ##Place TestCode goes below
                try:
                    self._sw[i].Document.forms[frmname].elements[element].click()
                except:
                    print 'ClickButton Failed'
    
    def SetListbox(self, wintext,element,value,frmname): #Win Title as Param
        """ This function select an item from a listbox"""
        for i in range(self._sw.Count): ## Count windows
            if i is None:
                print 'No Open Windows Found'
                break
            time.sleep(.2) ## may have to play with this value
            wn = self._sw[i].LocationName ## Get the window Title
            print wn
            
            ## checks to see if location matches the name
            if wn == wintext: 
                print "sw[", i, "]" ## print the win number
                win = self._sw[i].LocationName ## Get the window Title
                print "Window name: ", win 
                try:
                    self._sw[i].Document.forms[frmname].elements[element].value = value
                    print 'Selected item: ', value
                except:
                    print 'SetListBox failed'

 # -------------End of Method calls-------------------
if __name__ == "__main__":
    # Start test
    print 'starting test'
