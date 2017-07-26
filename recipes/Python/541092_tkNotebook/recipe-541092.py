#!usr/bin/env python
#tkNotebook
#Created By: Patrick T. Cossette <cold_soul79078@yahoo.com>

#tkNotebook allows users to make notebook widgets in Tk

#This software may be modified and redistributed, as long as any and all changes made
#From here on are stated, and ("Created By: Patrick T. Cossette <cold_soul79078@yahoo.com>") still remains somewhere
#In the code.

#This software is opensource, and free in hopes that it may be useful, and comes AS IS
#With no warrenty.

"""
    Defines a Notebook class to be used with Tkinter. A Notebook instance
    has the attributes change_tab, add_tab, destroy_tab, and focus_on.

    change_tab:  Internal Function, I don't suggest you call this directly.
    add_tab:     Creates a tab
    destroy_tab: destroys the given tab
    focus_on:    Focuses on the given tab

    The __init__ function creates three frames. One to hold the tabs together,
    one to create the base to parent each tab's children, and one to hold the
    base frame and the tab frame together.

    Each tab is a Label with a default relief of "GROOVE". Each label uses
    event bindings so that change_tab is called with the tab's ID Number as
    an argument. Each tab relief, when selected is set by default to "RAISED"
    
    For an exampe, view the source code, and run the module.

    Created By: Patrick T. Cossette <cold_soul79078@yahoo.com>    

"""

from Tkinter import *

class Notebook(Frame):
    """Notebook Widget"""
    def __init__(self, parent, activerelief = RAISED, inactiverelief = RIDGE, xpad = 4, ypad = 6, activefg = 'black', inactivefg = 'black', **kw):
        """Construct a Notebook Widget

        Notebook(self, parent, activerelief = RAISED, inactiverelief = RIDGE, xpad = 4, ypad = 6, activefg = 'black', inactivefg = 'black', **kw)        
    
        Valid resource names: background, bd, bg, borderwidth, class,
        colormap, container, cursor, height, highlightbackground,
        highlightcolor, highlightthickness, relief, takefocus, visual, width, activerelief,
        inactiverelief, xpad, ypad.

        xpad and ypad are values to be used as ipady and ipadx
        with the Label widgets that make up the tabs. activefg and inactivefg define what
        color the text on the tabs when they are selected, and when they are not

        """
                                                                                           #Make various argument available to the rest of the class
        self.activefg = activefg                                                           
        self.inactivefg = inactivefg
        self.deletedTabs = []        
        self.xpad = xpad
        self.ypad = ypad
        self.activerelief = activerelief
        self.inactiverelief = inactiverelief                                               
        self.kwargs = kw                                                                   
        self.tabVars = {}                                                                  #This dictionary holds the label and frame instances of each tab
        self.tabs = 0                                                                      #Keep track of the number of tabs                                                                             
        self.noteBookFrame = Frame(parent)                                                 #Create a frame to hold everything together
        self.BFrame = Frame(self.noteBookFrame)                                            #Create a frame to put the "tabs" in
        self.noteBook = Frame(self.noteBookFrame, relief = RAISED, bd = 2, **kw)           #Create the frame that will parent the frames for each tab
        self.noteBook.grid_propagate(0)                                                    #self.noteBook has a bad habit of resizing itself, this line prevents that
        Frame.__init__(self)
        self.noteBookFrame.grid()
        self.BFrame.grid(row =0, sticky = W)
        self.noteBook.grid(row = 1, column = 0, columnspan = 27)

    def change_tab(self, IDNum):
        """Internal Function"""
        
        for i in (a for a in range(0, len(self.tabVars.keys()))):
            if not i in self.deletedTabs:                                                  #Make sure tab hasen't been deleted
                if i <> IDNum:                                                             #Check to see if the tab is the one that is currently selected
                    self.tabVars[i][1].grid_remove()                                       #Remove the Frame corresponding to each tab that is not selected
                    self.tabVars[i][0]['relief'] = self.inactiverelief                     #Change the relief of all tabs that are not selected to "Groove"
                    self.tabVars[i][0]['fg'] = self.inactivefg                             #Set the fg of the tab, showing it is selected, default is black
                else:                                                                      #When on the tab that is currently selected...
                    self.tabVars[i][1].grid()                                              #Re-grid the frame that corresponds to the tab                      
                    self.tabVars[IDNum][0]['relief'] = self.activerelief                   #Change the relief to "Raised" to show the tab is selected
                    self.tabVars[i][0]['fg'] = self.activefg                               #Set the fg of the tab, showing it is not selected, default is black

    def add_tab(self, width = 2, **kw):
        """Creates a new tab, and returns it's corresponding frame

        """
        
        temp = self.tabs                                                                   #Temp is used so that the value of self.tabs will not throw off the argument sent by the label's event binding
        self.tabVars[self.tabs] = [Label(self.BFrame, relief = RIDGE, **kw)]               #Create the tab
        self.tabVars[self.tabs][0].bind("<Button-1>", lambda Event:self.change_tab(temp))  #Makes the tab "clickable"
        self.tabVars[self.tabs][0].pack(side = LEFT, ipady = self.ypad, ipadx = self.xpad) #Packs the tab as far to the left as possible
        self.tabVars[self.tabs].append(Frame(self.noteBook, **self.kwargs))                #Create Frame, and append it to the dictionary of tabs
        self.tabVars[self.tabs][1].grid(row = 0, column = 0)                               #Grid the frame ontop of any other already existing frames
        self.change_tab(0)                                                                 #Set focus to the first tab
        self.tabs += 1                                                                     #Update the tab count
        return self.tabVars[temp][1]                                                       #Return a frame to be used as a parent to other widgets

    def destroy_tab(self, tab):
        """Delete a tab from the notebook, as well as it's corresponding frame

        """
        
        self.iteratedTabs = 0                                                              #Keep track of the number of loops made
        for b in self.tabVars.values():                                                    #Iterate through the dictionary of tabs
            if b[1] == tab:                                                                #Find the NumID of the given tab
                b[0].destroy()                                                             #Destroy the tab's frame, along with all child widgets
                self.tabs -= 1                                                             #Subtract one from the tab count
                self.deletedTabs.append(self.iteratedTabs)                                 #Apend the NumID of the given tab to the list of deleted tabs
                break                                                                      #Job is done, exit the loop
            self.iteratedTabs += 1                                                         #Add one to the loop count
    
    def focus_on(self, tab):
        """Locate the IDNum of the given tab and use
        change_tab to give it focus

        """
        
        self.iteratedTabs = 0                                                              #Keep track of the number of loops made
        for b in self.tabVars.values():                                                    #Iterate through the dictionary of tabs
            if b[1] == tab:                                                                #Find the NumID of the given tab
                self.change_tab(self.iteratedTabs)                                         #send the tab's NumID to change_tab to set focus, mimicking that of each tab's event bindings
                break                                                                      #Job is done, exit the loop
            self.iteratedTabs += 1                                                         #Add one to the loop count

def demo():
    def adjustCanvas(someVariable = None):
        fontLabel["font"] = ("arial", var.get())
    
    root = Tk()
    root.title("tkNotebook Example")
    note = Notebook(root, width= 400, height =400, activefg = 'red', inactivefg = 'blue')  #Create a Note book Instance
    note.grid()
    tab1 = note.add_tab(text = "Tab One")                                                  #Create a tab with the text "Tab One"
    tab2 = note.add_tab(text = "Tab Two")                                                  #Create a tab with the text "Tab Two"
    tab3 = note.add_tab(text = "Tab Three")                                                #Create a tab with the text "Tab Three"
    tab4 = note.add_tab(text = "Tab Four")                                                 #Create a tab with the text "Tab Four"
    tab5 = note.add_tab(text = "Tab Five")                                                 #Create a tab with the text "Tab Five"
    Label(tab1, text = 'Tab one').grid(row = 0, column = 0)                                #Use each created tab as a parent, etc etc...
    Label(tab1, text = "When something is changed on a tab,\ngoing to a different tab and back\nwill not reset, or effect it in any way.", font = ("Comic Sans MS", 12, "italic")).grid()
    var = IntVar()
    var.set(10)
    scale = Scale(tab1, font = ("arial", 10), orient = 'horizontal', command = adjustCanvas, variable =var).grid()
    fontLabel = Label(tab1, text = "TEXT", font = ("Arial", 10))
    fontLabel.grid()
    Label(tab2, text = 'Tab Two\n\n(Has focus first by using the focus_on attribute)\n\nThe tabs are colored red and blue via\nthe Notebook options. The default\nvalues are black on black :P', font = ("Comic Sans MS", 12, "italic")).grid()
    Button(tab3, text = 'Destroy Tab Four!', command = lambda:note.destroy_tab(tab4)).grid()
    Label(tab3, text = "Destroying a tab will remove it,\nand competely destoy all child widgets.\nOnce you destroy a tab, you have to recreate it\ncompletely in order to get it back.", font = ("Comic Sans MS", 12, "italic")).grid()
    Label(tab4, text = 'Tab 4').grid()
    Button(tab5, text = 'Tab One', command = lambda:note.focus_on(tab1)).grid(pady = 3)
    Button(tab5, text = 'EXIT', width = 23, command = root.destroy).grid()
    note.focus_on(tab2)
    root.mainloop()

if __name__ == "__main__":
    demo()
