def GetOLVColClicked(event):

    # DevPlayer@gmail.com  2011-01 Jan-13
    # For use with a 3rd party module named ObjectListView
    # used with wxPython.

    """
    GetColClicked( event ) -> int Column number of mouse click.

    Get ObjectListView() column the user single-left-clicked the mouse in.

    You can use the column number to set the modelObject's attributes 
    without removing, re-adding, resorting the items in the OVL.

    This event handler is often bound to the event handler of the 
    wx.EVT_LIST_ITEM_SELECTED event. Other events may be needed for 
    the column's labels - the labels visually naming a column.

    This assumes the OLV.LayoutDirection() is LTR.
    """

    # ----------------------------------------------------------
    # Get the mouse position. Determine which column the user 
    # clicked in.
    # This could probably all be done in some list hit test event.
    # Not all OS platforms set all events m_...atributes. This is a 
    # work around.

    # Get point user clicked, here in screen coordinates. 
    # Then convert the point to OVL control coordinates.

    spt = wx.GetMousePosition()
    fpt = folv.ScreenToClient(spt)    # USE THIS ONE
    x, y = fpt

    #log( o, "GetOLVColClicked()                                   event.m_col: %d "% event.m_col)
    #log( o, "GetOLVColClicked()    folv.ScreenToClient(wx.GetMousePosition()): %d "% x)

    # Get all column widths, individually, of the OLV control .
    # Then compare if the mouse clicked in that column. 

    # Make this a per-click calculation as column widths can 
    # change often by the user and dynammically by different 
    # lengths of data strings in rows.

    last_col = 0
    for col in range(folv.GetColumnCount()) :

        # Get this OLV column's width in pixels.

        col_width = folv.GetColumnWidth(col)

        # Calculate the left and right vertical pixel positions
        # of this current column.

        left_pxl_col = last_col
        right_pxl_col = last_col + col_width - 1

        # Compare mouse click point in control coordinates,
        # (verse screen coordinates) to left and right coordinate of
        # each column consecutively until found.
        
        if left_pxl_col <= x <= right_pxl_col :

            # Mouse was clicked in the current column "col"; done

            col_selected = col
            break

        col_selected = None

        # prep for next calculation of next column

        last_col = last_col + col_width

    #log( o, 'GetOLVColClicked()    clicked in COLUMN %d' % col_selected)

    return col_selected
