#!/usr/bin/env python

"""
The Towers of Hanoi for wxPython
by S. Foster, Jan. 2004

    based on wxHanoi.cpp
    by Martin Bernreuther
"""

from wxPython.wx import *

import cPickle
import zlib

COLOURS = [ 'RED', 'CORAL', 'YELLOW', 'GREEN', 'BLUE', 'MAGENTA', 'PURPLE' ]

ICON = """\
\x78\x9c\x9d\x91\xbd\x0a\xc2\x30\x00\x84\xf7\x3c\x45\xc0\x21\x42\
\x21\xe4\xa7\xad\xba\x3a\x74\xb4\x43\x97\xac\xa1\x88\x83\xc5\xf4\
\xfd\x27\xef\x4c\x83\x20\x18\xc1\xa3\x3d\x9a\x8f\xef\xb2\x74\xbf\
\xac\x56\x4c\xca\x3b\x89\xa7\x97\x56\x89\xd5\x89\x38\x29\x2d\x67\
\x79\x5e\xe2\x7c\x07\xf0\x04\x0d\xc0\x6e\x18\x0c\x02\xd4\x12\x8d\
\x44\xc6\x10\x02\x75\x44\x21\x5b\x1b\xea\x89\x52\xb6\xe8\x01\x1d\
\x88\x24\xd0\x25\x3d\xae\x38\x1f\xf3\xb9\x1e\x78\x27\x11\x6f\x7f\
\xbe\xdb\xfd\xfa\x7d\x9f\xfe\xf8\xc2\xfd\xd6\x40\x66\x65\x3b\x84\
\x50\xb5\x2d\xed\x52\xaf\x49\x62\x6a\x13\x47\xbb\x14\x27\x63\x4e\
\x65\xe2\x69\x97\xc2\xa4\x29\xf9\x3e\x69\x69\x97\xc2\x6f\xfc\x11\
\x4e\x3a\xda\xa5\xf4\x13\x8d\x92\x69\x2c"""

def getIconData():
    return cPickle.loads( zlib.decompress( ICON ))

class wxHanoiDisc:
    def __init__( self, n, width, height ):
        self.width = ( n + 1 ) * width
        self.height = height
        self.n = n
        self.brush = wxBrush( wxNamedColour( COLOURS[ n % len( COLOURS )] ))

class wxHanoiFrame( wxFrame ):
    def __init__( self, title, pos, size ):
        wxFrame.__init__( self, None, -1,
                            title, pos = pos, size = size )

        icon = wxIconFromXPMData( getIconData() )
        self.SetIcon( icon )

        self.CreateMenu()
        self.CreateStatusBar();

        self.sleepTime = 3
        self.numDiscs = 4

        self.pen = wxPen( wxNamedColour( 'BLACK' ), 1, wxSOLID )

        self.Initialize()

        EVT_CLOSE( self, self.OnCloseWindow )
        EVT_PAINT( self, self.OnPaint )

    def CreateMenu( self ):

        def MenuCallback( menu, item, callback ):
            id = wxNewId()
            menu.Append( id, item )
            EVT_MENU( self, id, callback )

        menuBar = wxMenuBar()

        menuFile = wxMenu()
        MenuCallback( menuFile, 'E&xit...\tCtrl-X', self.OnQuit )
        menuBar.Append( menuFile, '&File' )

        menuPlay = wxMenu()
        MenuCallback( menuPlay, '&Number of Discs...', self.OnInpNumDiscs )
        MenuCallback( menuPlay, '&Time between Moves...', self.OnInpSleepTime )
        menuPlay.AppendSeparator()
        MenuCallback( menuPlay, '&Play', self.OnPlay )
        MenuCallback( menuPlay, '&Reset', self.OnReset )
        menuBar.Append( menuPlay, '&Play' )

        menuHelp = wxMenu()
        MenuCallback( menuHelp, '&About...', self.OnAbout )
        menuBar.Append( menuHelp, '&Help' )

        self.SetMenuBar( menuBar )

    def Initialize( self ):
        self.width, self.height = self.GetClientSize()
        maxwidth = self.width / 3
        w = self.width / 6
        self.xpos = [ i * w for i in [ 1, 3, 5 ]]

        height = self.height / self.numDiscs
        width = maxwidth / self.numDiscs
        if height > width:
            height = width
        self.discheight = height
        self.discwidthfac = width
        
        discs = range( self.numDiscs )
        discs.reverse()

        self.pegs = [[ wxHanoiDisc( i, width, height ) for i in discs ], [], []]
        self.moves = 0

        width, height = self.GetClientSize()
        self.Draw( wxClientDC( self ), width, height )

    def OnQuit( self, _event ):
        self.Close( true );

    def OnCloseWindow( self, event ):
        self.Destroy()

    def OnAbout( self, event ):
        wxMessageBox( __doc__, 'About wxHanoi', wxOK|wxICON_INFORMATION, self )

    def OnInpNumDiscs( self, _event ):
        self.numDiscs = wxGetNumberFromUser( '', 'Discs:', 'Number of Discs', 
                                                self.numDiscs, 1, 25, self )
        if self.numDiscs == -1:
            self.SetStatusText( "Invalid number entered or dialog cancelled." )
        else:
            self.Initialize()
        
    def OnInpSleepTime( self, _event ):
        self.sleepTime = wxGetNumberFromUser( '', 'Wait [sec/10]:', 'Time between Moves', 
                                                self.sleepTime, 0, 10, self )
        if self.sleepTime == -1:
            self.SetStatusText( "Invalid number entered or dialog cancelled." )
        else:
            self.Initialize()

    def OnPlay( self, _event ):
        self.Initialize()
        self.SetStatusText( 'Playing' )
        self.Move( 0, 2, 1, self.numDiscs )
        self.SetStatusText( 'Finished: %s Moves' % self.moves )
    
    def OnReset( self, event ):
        self.Initialize()

    def DrawDisc( self, dc, disc, x, y ):
        assert x <= 2
        dc.SetPen( self.pen )
        dc.SetBrush( disc.brush )
        dc.DrawRectangle(
            self.xpos[x] - ( disc.width / 2 ),
            self.height - ( y * self.discheight ),
            disc.width,
            disc.height )

    def Draw( self, dc, width, height ):
        mdc = wxMemoryDC()
        mdc.SelectObject( wxEmptyBitmap( width, height ))
        mdc.BeginDrawing()
        for x, peg in enumerate( self.pegs ):
            for y, disc in enumerate( peg ):
                self.DrawDisc( mdc, disc, x, y+1 )
        mdc.EndDrawing()
        dc.Blit( 0, 0, width, height, mdc, 0, 0 )
        
    def OnPaint( self, event ):
        width, height = self.GetClientSize()
        self.Draw( wxPaintDC( self ), width, height )

    def MoveDisc( self, src, dst ):
        disc = self.pegs[src].pop()
        self.pegs[dst].append( disc )
        self.moves += 1
        self.SetStatusText( 'Move %s' % self.moves )
        width, height = self.GetClientSize()
        self.Draw( wxClientDC( self ), width, height )
        wxUsleep( 100 * self.sleepTime )

    def Move( self, src, dst, temp, n ):
        if n == 1:
            self.MoveDisc( src, dst )
        else:
            self.Move( src, temp, dst, n-1 )
            self.MoveDisc( src, dst )
            self.Move( temp, dst, src, n-1 )

class wxHanoiApp( wxApp ):
    def OnInit( self ):
        self.frame = wxHanoiFrame(
                        'Towers of Hanoi for wxPython',
                        wxPoint( 50, 50 ),
                        wxSize( 450, 350 ))
        self.frame.Show( True )
        self.SetTopWindow( self.frame )

        return True

app = wxHanoiApp(0)
app.MainLoop()
