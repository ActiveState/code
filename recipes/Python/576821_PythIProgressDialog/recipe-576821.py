import win32gui

class COMprogressDialog(object):
    _trace = False
    def __init__(self, title='Progress Dialog', animation_res=161):
        '''
        COMprogressDialog - Windows COM object that shows progress of task.
                            This dialog runs in a separate thread so it can be
                            run from virtually any program without adding
                            threading complexity to that program.

        title         - Dialog window title
        animation_res - animation resource .AVI for interesting
                        progress display

                        animation_res=160 (move)
                        animation_res=161 (copy) [DEFAULT]

        COMprogressDialog.dialog class methods -

          StartProgressDialog(hwndParent, lEnableModeless, dwFlags, pvReserved)
          StopProgressDialog()
          SetTitle(sTitle)
          SetAnimation(hInstAnimation, idAnimation)
          HasUserCancelled()
          SetProgress(completed, total)
          SetProgress64(completed64, total64)
          SetLine(lineNum, sText, lCompactPath, pvReserved)
          SetCancelMsg(sCancelMsg, pvReserved)
          Timer() - Reset timer
          Release() - Close dialog, release resources

        Animation resource in shell32.dll that points to .AVIs

        Written by: Larry Bates (with substantial help from Thomas Heller and
                    Tim Golden on COM interfacing to IProgressDialog),
                    February 2008

                    Updated February 2011 - Added close() method to gracefully
                    close the dialog.
                    
        License: GPL
        Requires: ctypes, comtypes, win32gui
        '''
        LM = "COMprogressDialog.__init__"
        if self._trace:
            print "%s-Entering" % LM

        #
        # Save title so I can update it with % completed as I progress
        #
        self.title = title
        #
        # Get a list of topWindows
        #
        topWindows = list()
        win32gui.EnumWindows(self._windowEnumerationHandler, topWindows)
        #
        # Isolate Program Manager window from all the other topWindows,
        # this will be used as the parent window for the dialog.
        #
        hwndParent = [w[0] for w in topWindows if w[1] == 'Program Manager'][0]
        import comtypes.client
        try:
            import comtypes.gen.VBProgressDialog
            
        except ImportError:
            #
            # Create object from the progress tlb file for the COM Progress
            # Dialog
            #
            comtypes.client.GetModule('progdlg.tlb')
            
        vbpd = comtypes.gen.VBProgressDialog
        #
        # Create instance of progress dialog
        #
        if self._trace:
            print "%s-creating instance of progress dialog" % LM

        self.dialog = comtypes.client.CreateObject(vbpd.ProgressDialog)
        #
        # Set the animation for the dialog (default=copy) from shell32.dll
        #
        import ctypes
        #
        # Pointer to shell32.dll
        #
        shell32 = ctypes.windll.shell32
        #
        # Get handle for this
        #
        m_hLibShell32 = shell32._handle
        #
        # Set the animation based on animation_res number (default animation
        # is copy animation).
        #
        self.dialog.SetAnimation(m_hLibShell32, animation_res)
        #
        # Insert title into top of dialog
        #
        self.dialog.SetTitle(title)
        #
        # Start the dialog
        #
        self.dialog.StartProgressDialog(hwndParent, None, 0, 0)
        if self._trace:
            print "%s-Leaving" % LM
        
    def _windowEnumerationHandler(self, hwnd, resultList):
        #
        # Get a list of the top level windows so I can find Program Manager
        #
        resultList.append((hwnd, win32gui.GetWindowText(hwnd)))

    def close(self):
        self.dialog.StopProgressDialog()

if __name__ == "__main__":
    import time
    compactPath = 1
    total = 100
    filenames = ['C:/pagefile.sys',
                 'C:/Documents and Settings/All Users/Start Menu/' \
                 'Programs/Administrative Tools/Computer Management'
                ]

    for i in xrange(3):
        title = "COMprogressDialot Unit Test %i" % (i+1)
        #
        # Create instance of the COMprogressDialog class
        #
        DLGobj = COMprogressDialog(title=title)
        #
        # Set the first line of the dialog to the filename
        #
        DLGobj.dialog.SetLine(1, filenames[0], compactPath, 0)
        for j in xrange(total):
            completed = int(100.0 / total * j)
            completed = "%s (%i%%)" % (title, completed)
            #
            # Update title to include (xx%) completed
            #
            DLGobj.dialog.SetTitle(completed)
            #
            # Update the progress gauge
            #
            DLGobj.dialog.SetProgress(j, total)
            #
            # Set second line to ##### of ##### bytes uploaded
            #
            line2 = "%i of %i bytes uploaded" % (j, total)
            DLGobj.dialog.SetLine(2, line2, 0, 0)
            #
            # See if user pushed cancel button
            #
            if DLGobj.dialog.HasUserCancelled():
                break

            #
            # Simulate uploading two equal sized files
            #
            if j == 50:
                compactPath = 1
                DLGobj.dialog.SetLine(1, filenames[1], compactPath, 0)
                
            time.sleep(0.1)

##        #
##        # Only necessary because of nested loops
##        #
##        if DLGobj.dialog.HasUserCancelled():
##            break
        #
        # Have the COM dialog close and release it's resources
        #
        DLGobj.close()
