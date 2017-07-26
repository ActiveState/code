#!/usr/bin/env python

"""
wxKoch.py for wxPython/wxWindows 2
by Simon Foster, November 2001
based on wxKoch0.cpp
by Martin Bernreuther, Jan 2000
"""
from time import time
import math
import cPickle
import zlib

from wxPython.wx import *

[ ID_Quit, ID_About, ID_InpLevel ] = range(3)

ABOUT_TEXT = """\
Koch Snowflake for wxPython
by S. Foster, November 2001"""

PYTHON = """\
\x78\xDA\xAD\x94\x31\x6E\xC3\x30\x0C\x45\xF7\x9C\x82\x40\x07\x17\
\x20\xF0\xE1\xB4\x43\x33\x0A\x1D\x3C\xC6\x43\x16\xAE\x41\xD0\xA9\
\x41\xDD\xFB\x4F\xA5\x48\xC9\x96\x2C\xA5\x5D\x4A\x30\x76\xBE\xF5\
\x42\x52\xA4\x9C\xE7\xFB\xF7\xF1\x70\x19\x5E\x5F\x48\xFD\x8D\x8E\
\xC3\xE1\x7A\x19\x40\x37\x7A\xBF\x5F\x6F\x9F\xA6\x66\x55\x4F\xA3\
\xDA\x34\x99\x66\xD7\xD3\x34\x8E\xA6\x25\xEA\xD3\x78\x1A\x93\x0E\
\x51\xC7\xD5\xA4\x49\xF5\x79\xF9\xFA\x30\xB1\xF8\xE2\xFA\x63\x72\
\x03\xD4\x41\xAD\x15\x10\x44\xD4\x05\xBF\x41\x70\xEB\x51\x05\xB4\
\x2C\xEA\x0B\xFE\x80\x66\xF5\xF9\x5F\xA0\x9C\x0E\x0F\x21\x2B\xDA\
\x0A\x8F\x57\xF4\x20\x5B\xCC\xE6\x60\x03\x95\x88\x08\x9B\xC4\x0E\
\x2A\x19\x16\xE6\x3D\x95\xA0\xD4\x6D\x47\x1E\x41\x5B\x14\x20\x43\
\x1B\xE5\x10\xB3\x70\x4A\x04\xBD\xE9\xA7\x0B\xB9\xC5\x16\xE8\x55\
\xBF\xB5\x10\xC1\x23\xC1\xE3\x20\x26\x6E\xA1\xD8\xCA\x10\x52\x1C\
\x7A\x10\x89\x9C\xB1\xA2\xE2\xC1\xE2\xCE\xEE\xF4\x79\x08\xA9\x6E\
\x8A\x81\xA4\x0B\x29\x93\x91\x54\x50\xD3\x71\xB2\x7A\x6C\x5C\xB9\
\x1E\x69\x66\x17\x28\xAC\xC7\xBC\xC3\x20\xA7\xF3\xD3\x92\xC3\xD4\
\x0C\xEA\xB7\x45\x32\x93\x72\x7B\x91\x15\xB4\xC5\xF1\x60\x7E\xAE\
\xA4\x84\x6C\x36\x1B\xB3\xDE\x6A\x68\xCB\x56\x1B\xA8\x17\xA9\x58\
\x87\x8D\x60\x07\x71\x3A\x57\xEB\x1E\x6D\x03\xFB\xDD\x79\xE3\x39\
\xF7\xBF\xF9\xC3\xF0\xED\xF9\x6C\xEA\xB7\xAA\x84\xF6\x6B\x25\x84\
\x1F\x03\x50\x09\xE6"""

root3 = math.sqrt ( 3. )

def getIconData():
    return cPickle.loads( zlib.decompress( PYTHON ))

class wxKochFrame( wxFrame ):
    def __init__( self, title, pos, size ):
        wxFrame.__init__( self, None, -1,
                            title, pos = pos, size = size )
        
        icon = wxIconFromXPMData( getIconData() )
        self.SetIcon( icon )

        self.menuBar = wxMenuBar()

        self.menuFile = wxMenu()
        self.menuFile.Append( ID_InpLevel, "Input &Level...\tCtrl-D" )
        self.menuFile.AppendSeparator()
        self.menuFile.Append( ID_Quit, "E&xit...\tCtrl-X" )
        self.menuBar.Append( self.menuFile, "&File" ) ;

        self.menuHelp = wxMenu()
        self.menuHelp.Append( ID_About, "&About..." )
        self.menuBar.Append( self.menuHelp, "&Help" )

        self.SetMenuBar( self.menuBar )
        EVT_MENU( self, ID_Quit, self.OnQuit )
        EVT_MENU( self, ID_About, self.OnAbout )
        EVT_MENU( self, ID_InpLevel, self.OnInpLevel )

        EVT_SIZE( self, self.OnSize )
        EVT_PAINT( self, self.OnPaint )

        self.level = -1
        self.mdc = None

        self.CreateStatusBar()
        self.SetStatusText( 'Enter Level' )

    def OnQuit ( self, event ):
        self.Close( true )
        
    def OnAbout( self, event ):
        wxMessageBox ( __doc__, 
            "About wxKoch", wxOK|wxICON_INFORMATION, self )
            
    def OnInpLevel( self, event ):
        self.level = wxGetNumberFromUser( "", "Level: ", "Input Level",
                                        4, 0, 10, self )
        if self.level == -1:
            msg = "Invalid number entered or dialog cancelled."
            self.SetStatusText( msg )
        else:
            self.mdc = None
            self.Refresh()

    def OnSize( self, event ):
        self.mdc = None
        self.Refresh()
        
    def DrawEdge ( self, dc, n, x1, y1, x2, y2 ):
        if n > 0 :
            x3 = 2. * x1/3. + x2/3.
            y3 = 2. * y1/3. + y2/3.
            self.DrawEdge( dc, n-1, x1, y1, x3, y3 )
            x4 = x1/3. + 2. * x2/3.
            y4 = y1/3. + 2. * y2/3.
            x5 = .5 * ( x1+x2 ) - ( y2-y1 ) * root3 / 6.
            y5 = .5 * ( y1+y2 ) + ( x2-x1 ) * root3 / 6.
            self.DrawEdge( dc, n-1, x3, y3, x5, y5 )
            self.DrawEdge( dc, n-1, x5, y5, x4, y4 )
            self.DrawEdge( dc, n-1, x4, y4, x2, y2 )
        else:
            dc.DrawLine( x1, y1, x2, y2 )

    def OnPaint( self, event ):
        print '.',
        pdc = wxPaintDC( self )
        if self.level != -1:
            msg = ''
            start = time()
            width, height = self.GetClientSize()

            if not self.mdc:
                msg = 'Draw:'
                n = self.level
                d = height

                if width < height: d = width

                y1 = .5 * height + .25 * d
                y3 = .5 * height - .5 * d
                x1 = .5 * width - .25 * d * root3
                x2 = .5 * width + .25 * d * root3
                x3 = .5 * width

                self.mdc = wxMemoryDC()
                self.mdc.SelectObject( wxEmptyBitmap( width, height ))
                self.mdc.Clear()
                self.mdc.SetPen( wxPen( wxNamedColour( 'CADET BLUE' ), 1, wxSOLID ))
                self.mdc.BeginDrawing()

                self.DrawEdge( self.mdc, n, x1, y1, x2, y1 )
                self.DrawEdge( self.mdc, n, x2, y1, x3, y3 )
                self.DrawEdge( self.mdc, n, x3, y3, x1, y1 )

                self.mdc.EndDrawing()

            pdc.Blit( 0, 0, width, height, self.mdc, 0, 0 )
            msg += 'level %s in %s seconds' % ( self.level, time() - start )
            self.SetStatusText( msg )
        
class wxKochApp( wxApp ):

    def OnInit( self ):
        self.pframe = wxKochFrame(
                        "Koch Snowflake for wxPython", 
                        wxPoint( 50, 50 ),
                        wxSize( 200, 200 ))
        self.pframe.Show( true )
        self.SetTopWindow( self.pframe )
        return true

app = wxKochApp(0)
app.MainLoop()
