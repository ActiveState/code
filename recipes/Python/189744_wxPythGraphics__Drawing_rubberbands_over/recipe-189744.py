# This class describes a generic method of drawing rubberbands
# on a wxPython canvas object (wxStaticBitmap, wxPanel etc) when
# the user presses the left mouse button and drags it over a rectangular
# area. It has methods to return the selected area by the user as 
# a rectangular 4 tuple / Clear the selected area.

# Beginning of code

class wxPyRubberBander:
    """ A class to manage mouse events/ rubberbanding of a wxPython
        canvas object """

    def __init__(self, canvas):
        
        # canvas object
        self._canvas = canvas
        # mouse selection start point
        self.m_stpoint=wxPoint(0,0)
        # mouse selection end point
        self.m_endpoint=wxPoint(0,0)
        # mouse selection cache point
        self.m_savepoint=wxPoint(0,0)
        
        # flags for left click/ selection
        self._leftclicked=false
        self._selected=false

        # Register event handlers for mouse
        self.RegisterEventHandlers()

    def RegisterEventHandlers(self):
        """ Register event handlers for this object """

        EVT_LEFT_DOWN(self._canvas, self.OnMouseEvent)
        EVT_LEFT_UP(self._canvas, self.OnMouseEvent)
        EVT_MOTION(self._canvas, self.OnMouseEvent)

    
    def OnMouseEvent(self, event):
        """ This function manages mouse events """


        if event:
            
            # set mouse cursor
            self._canvas.SetCursor(wxStockCursor(wxCURSOR_ARROW))
            # get device context of canvas
            dc= wxClientDC(self._canvas)
            
            # Set logical function to XOR for rubberbanding
            dc.SetLogicalFunction(wxXOR)
            
            # Set dc brush and pen
            # Here I set brush and pen to white and grey respectively
            # You can set it to your own choices
            
            # The brush setting is not really needed since we
            # dont do any filling of the dc. It is set just for 
            # the sake of completion.

            wbrush = wxBrush(wxColour(255,255,255), wxTRANSPARENT)
            wpen = wxPen(wxColour(200, 200, 200), 1, wxSOLID)
            dc.SetBrush(wbrush)
            dc.SetPen(wpen)

            
        if event.LeftDown():
 
           # Left mouse button down, change cursor to
           # something else to denote event capture
           self.m_stpoint = event.GetPosition()
           cur = wxStockCursor(wxCURSOR_CROSS)  
           self._canvas.SetCursor(cur)
        
           # invalidate current canvas
           self._canvas.Refresh()
           # cache current position
           self.m_savepoint = self.m_stpoint
           self._selected = false
           self._leftclicked = true

        elif event.Dragging():   
           
            # User is dragging the mouse, check if
            # left button is down
            
            if self._leftclicked:

                # reset dc bounding box
                dc.ResetBoundingBox()
                dc.BeginDrawing()
                w = (self.m_savepoint.x - self.m_stpoint.x)
                h = (self.m_savepoint.y - self.m_stpoint.y)
                
                # To erase previous rectangle
                dc.DrawRectangle(self.m_stpoint.x, self.m_stpoint.y, w, h)
                
                # Draw new rectangle
                self.m_endpoint =  event.GetPosition()
                
                w = (self.m_endpoint.x - self.m_stpoint.x)
                h = (self.m_endpoint.y - self.m_stpoint.y)
                
                # Set clipping region to rectangle corners
                dc.SetClippingRegion(self.m_stpoint.x, self.m_stpoint.y, w,h)
                dc.DrawRectangle(self.m_stpoint.x, self.m_stpoint.y, w, h) 
                dc.EndDrawing()
               
                self.m_savepoint = self.m_endpoint # cache current endpoint

        elif event.LeftUp():

            # User released left button, change cursor back
            self._canvas.SetCursor(wxSTOCK_CURSOR(wxCURSOR_ARROW))       
            self._selected = true  #selection is done
            self._leftclicked = false # end of clicking  
            
            
    def GetCurrentSelection(self):
        """ Return the current selected rectangle """
        
        # if there is no selection, selection defaults to
        # current viewport
        
        left = wxPoint(0,0)
        right = wxPoint(0,0)
        
        # user dragged mouse to right
        if self.m_endpoint.y > self.m_stpoint.y:
            right = self.m_endpoint
            left = self.m_stpoint
        # user dragged mouse to left
        elif self.m_endpoint.y < self.m_stpoint.y:
            right = self.m_stpoint
            left = self.m_endpoint
   
        return (left.x, left.y, right.x, right.y)


    def ClearCurrentSelection(self):
        """ Clear the current selected rectangle """
        
        box = self.GetCurrentSelection()
        
        dc=wxClientDC(self._canvas)
        
        w = box[2] - box[0]
        h = box[3] - box[1]
        dc.SetClippingRegion(box[0], box[1], w, h)
        dc.SetLogicalFunction(wxXOR)
        
        # The brush is not really needed since we
        # dont do any filling of the dc. It is set for 
        # sake of completion.
        
        wbrush = wxBrush(wxColour(255,255,255), wxTRANSPARENT)
        wpen = wxPen(wxColour(200, 200, 200), 1, wxSOLID)
        dc.SetBrush(wbrush)
        dc.SetPen(wpen)
        dc.DrawRectangle(box[0], box[1], w,h)
        self._selected = false 
        
        # reset selection to canvas size
        self.ResetSelection()    

    def ResetSelection(self):
        """ Resets the mouse selection to entire canvas """
    
        self.m_stpoint = wxPoint(0,0)
        sz=self._canvas.GetSize()
        w,h=sz.GetWidth(), sz.GetHeight()
        self.m_endpoint = wxPoint(w,h)
