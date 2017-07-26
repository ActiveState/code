"""
Demonstrates the use of the ProgressMeter class.

Author: Tucker Beck
Last Tested: 3/2/2009
Verified with: Python 2.6, Tkinter 8.4
"""

from __future__ import division
from Tkinter import *
from random import randint
from time import sleep

class ProgressMeter( Frame ):
    """
    The ProgressMeter is-a Frame widget provides a progress bar and
    accompanying information to a user regarding a long, computationaly
    intensive process.  A ProgressMetar can control any generator function
    that returns string message or None after each iteration.  Furthermore,
    the ProgressMeter can interrupt the process at any time.
    """
    def __init__( self, parent, height=30 ):
        """
        Initializes this ProgressMeter
        
        Arguments:
          parent:   The master widget for this ProgressMeter
          height:   The desired height of the progress bar
        """
        self.parent = parent
        Frame.__init__( self, parent )
        self.columnconfigure( 0, weight=1 )                                     # Forces the canv object to resize any time this widget is resized 
        self.rowconfigure( 0, weight=1 )
        self.statusMessage = 'Normal'
        self.w = 0
        self.h = 0
        self.canv = Canvas( self, height=height)                                # This canvas will display the progress bar and accompanying percentage text
        self.canv.grid( row=1, column=0, sticky=N+S+E+W )
        self.canv.bind( '<Configure>', lambda e:
                        self.resize( e.width, e.height ) )                      # When the canvas is resized the progress bar should be redrawn.
        self.killVar = IntVar()                                                 # The killBtn can cancel execution
        self.killVar.set( 0 )
        self.killBtn = Button( self, text='Cancel',
                               command=lambda: self.killVar.set(1) )
        self.killBtn.configure( state=DISABLED )
        self.killBtn.grid( row=1, column=1 )
        self.targetGen = None                                                   # Placekeeper for the generator function that will be metered
        self.targetArgs = []                                                    # Argument list for the generator function
        self.targetKwds = {}                                                    # Keyword dictionary for the generator funciton
        self.targetIdx = 0                                                      # Keeps track of which step in iteration is currently being executed
        self.targetLen = 0                                                      # Total number of steps in exectuion
    
    
    def resize( self, w, h ):
        """
        Handles resize events for the canv widget.  Adjusts the height and width
        of the canvas for the progress bar calculations.
        
        Arguments:
          w: The new width
          h: The new height
        """
        self.w = w
        self.h = h
        self.canv.delete( 'frame' )
        self.canv.create_rectangle( 1, 1, self.w, self.h, outline='black',
                                    fill='gray75', tag='frame' )

    def reset( self ):
        """
        Resets the control values or the generator function and also clears the
        progress bar
        """
        self.canv.delete( 'bar' )
        self.canv.delete( 'text' )
        self.killBtn.configure( state=DISABLED )
        self.targetGen = None
        self.targetArgs = []
        self.targetKwds = []
        self.killVar.set( 0 )
        self.targetIdx = 0
        self.targetLen = 0
        
    def clearStatus( self ):
        """"
        Clears the statusMessage member.  Might be used by parent GUI that
        reports child status.
        """
        self.statusMessage = 'Normal'

    def drawBar( self ):
        """
        Updates the status bar for the percentage of completion.
        """
        pct = self.targetIdx / self.targetLen                                   # The percentage of completion
        x0 = 2                                                                  # The bar is inset by 2 pixels
        x1 = pct * ( self.w - 3 ) + 2
        y0 = 2
        y1 = self.h
        self.canv.delete( 'bar' )
        self.canv.create_rectangle( x0, y0, x1, y1, fill='SteelBlue3',
                                    outline='', tag='bar' )
        self.canv.delete( 'text' )
        pctTxt = '%02.2f%%' % ( pct*100, )
        self.canv.create_text( self.w/2, self.h/2, text=pctTxt,
                               anchor=CENTER, tag='text' )
        
    def startGen( self, targetGen, targetLen, targetArgs=[], targetKwds={} ):
        """
        Initializes the target generator function with supplied arguments and
        keyword.  Requests Tk to call iterGen after all idle events have been
        handled.
        
        Arguments:
          targetGen:  The target generator function
          targetLen:  The number of iterations in the target generator
          targetArgs: The arguments for the generator function
          targetKwds: The keyword arguments fo the generator function
        Note:
          Having iterGen called by Tk ensures that redraws and other sorts of
          normal Tkinter events can be processed.  Results in the status bar
          updating real-time with execution while allowing the GUI to function
          normally.
        """
        self.targetGen = targetGen( *targetArgs, **targetKwds )
        self.targetLen = targetLen
        self.killBtn.configure( state=NORMAL )
        self.after_idle( self.iterGen )
        
    def iterGen( self ):
        """
        Iterates through the target generator using delayed self referencing
        funcition calls to allow GUI updates between iterations
        """
        try:
            msg = self.targetGen.next()                                         # Execute the next iteration of the genrator
        except StopIteration:
            self.reset()                                                        # When the generator is finished, a StopIteration exception is raised.  This signals a normal finish in the generator
            self.statusMessage = 'Completed'
            self.event_generate( '<<Finished>>' )                               # A <<Finished>> virtual event signals the GUI that the progress meter is finished
            return
        self.targetIdx += 1
        self.drawBar()
        if msg == None:
            pass
        elif msg.startswith( 'AbortIteration' ):                                # The target generator can signal that something irrevocable has happend by yielding a value of 'AbortIteration'
            self.reset()
            self.statusMessage = msg
            self.event_generate( '<<Finished>>' )
            return
        else:
            self.statusMessage = msg                                            # If the generator yields a value other than None or 'AbortIteration', this message will be sent out to the controlling gui
            self.event_generate( '<<StatusRequest>>' )
        if self.killVar.get() == 1:                                             # Occurs if the user clicks the killBtn
            self.reset()
            self.statusMessage = 'Canceled'
            self.event_generate( '<<Finished>>' )
            return
        self.update_idletasks()
        self.after_idle( self.iterGen )
        
def dummy_gen( alices, bobs ):
    """
    A simple, stupid example of a ProgressMeter iterable generator function
    """
    for alice in alices:
        for bob in bobs:
            if bob==alice:
                yield 'Match: %s==%s' % ( str(alice), str(bob) )
            else:
                yield 'No Match: %s!=%s' % ( str(alice), str(bob) )

def main():
    root = Tk()
    root.title( 'ProgressMeter Demo' )
    pgress = ProgressMeter( root )                                              # Initialize the ProgressMeter with default arguments
    pgress.grid( row=1 )
    alices = range( 53 )
    bobs = [ randint( 0,53 ) for i in range( 53 ) ]
    btn = Button( root, text="Go!", command=lambda:
         pgress.startGen( dummy_gen, len(alices) * len(bobs), [alices, bobs] ) )# Starts the ProgressMeter going when the button is clicked
    btn.grid( row=0 )
    statusVar = StringVar( root, 'None' )
    status = Label( root, textvariable=statusVar )
    status.grid( row=2 )                                                        # This label will be used to display status messages from the ProgressMeter
    root.bind( '<<StatusRequest>>', lambda event:
               statusVar.set(pgress.statusMessage) )
    root.bind( '<<Finished>>', lambda event:
               statusVar.set( pgress.statusMessage ) )
    root.mainloop()

if __name__=='__main__':
    main()
