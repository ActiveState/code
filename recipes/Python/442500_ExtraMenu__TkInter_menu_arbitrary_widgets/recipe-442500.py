# $Id: xmenu.py,v 1.20 2005/10/31 18:03:22 jes Exp jes $
# Copyright 2005 Jim Segrave < jes@jes-2.demon.nl>
from Tkinter import *
import re

EMPTY = """
#define empty_width 1
#define empty_height 1
static unsigned char empty_bits[] = {
   0x00};
"""

class ExtraMenu :
    """Class for creating a menu with optional sub-menus. Sub-menus can be
    instances of an ExtraMenu or any other widget.

    The topmost level is a Button which, when activated, drops down a
    menu containing any of Buttons, separators, Labels, Checkbuttons
    or RadioButtons.  A button can be used to create a sub-menu which
    will appear to the side of the main menu next to its invoking
    button. Sub-menus can be set to appear whenever the menu button is
    active, or only when the button is selected.

    If the sub-menu is a widget other than a Button, Label, separator,
    Checkbutton or Radiobutton, then there can be no other widgets in
    the sub-menu. However, complex widgets, such as Pmw.ComboBoxes are
    a single widget in this context. You could even put a canvas up as
    a sub-menu.

    An important difference between an ExtraMenu and other Menus is that the
    wigets compromising the menu are created only when the menu is post()ed
    and destroyed when the menu is unpost()ed
"""
    def __init__( self, master, root, **kw ) :
        """Construct an ExtraMenu widget with parent window 'master' to be
        displayed in the top-level window 'root'
        Arguments:
        master : the Frame in which the menu's main button is to
          be placed (for the top level menu), ignored for sub-menus
        root :  the toplevel window which contains 'master'
        args :  no other positional arguments
        kw : these values will be passed to construct a Frame object for the
             menu, except for the following, which are for the ExtraMenu
             object:
          is_submenu : True makes this is a sub-menu
              default = False
          cascade_side : LEFT/RIGHT - which side sub-menus will appear on.
              default = RIGHT. This only has effect in the top level menu
        """

        # id's for widgets in the menu
        self._button_no = -1
        # list of dictionaries for widgets (in order displayed)
        self._wdicts = []
        # set when this menu is posted
        self.is_posted = 0
        # if this is a sub-menu, and it's posted,
        # here's the ExtraMenu object of which it's a sub-menu (if any)
        self._parent = None
        # if there's a sub-menu posted from this menu, here's the
        # ExtraMenu object for the sub-menu
        self._child = None
        # the main menu button's window
        self._master = master
        # the root display (needed for placing menus)
        self._root = root

        # for sub-menus, determine which side to display it on
        self._cascade_side = kw.pop( 'cascade_side', RIGHT )
        # determines if this
        self._is_submenu = kw.pop( 'is_submenu', False )

        if not self._cascade_side :
            self._cascade_side = RIGHT

        # any left over keywords are for the menu frame
        self._menu_frame_kw = kw

        # a one pixel empty bitmap for use in separators
        self._empty = BitmapImage( data = EMPTY )

    def pack( self, master = None, **pkw ):
        """ create and post Button for opening menu. If this is a sub-menu,
        the pack method does nothing. Return and left-click will be bound
        to the Button , along with Alt-underline_letter if requested

        Arguments: master - not used, but makes the pack() call more
           uniform with other calls to pack for other object types
        Keyword args: same as for any other widget pack() call
        """

        # sub-menus are only ever posted in response to upper menu
        # actions
        if self._is_submenu :
            return

        # create the menu button for the menu and any eventual children
        self.button = Button( self._master, **self._mainbutton_kw )

        # change to a local command to run before the user supplied
        # command
        self.button.configure( command = self._main_button_select )

        # set up any hotkey for this menu
        kw = self._mainbutton_kw
        underline = kw.get( 'underline', None )
        text = kw.get( 'text', None )
        hotkey = None
        if underline is not None  and text is not None :
            try :    hotkey =  text[ underline ].lower()
            except : pass

        self.button.pack( **pkw )
        self.button.bind( '<Return>', self.post )
        if hotkey is not None :
            self._root.bind( "<Alt-%s>" % ( hotkey ), self.post, True )

    def post( self, event = None, activate_button = True ) :
        """ post the menu/submenu

        Arguments:
          event : supplied when post is activated from an event binding, the
              Event object is never used
          activate_button :  default True, ignored when the ExtraMenu
              object is not a menu (e.g. the menu is an arbitrary widget)
              When True, the topmost selectable widget in the menu which
              is not in state DISABLED will become Active and have focus set.
              If False, no button will be marked active or receive focus

        This method creates a Frame and calls the placer to put it:
        the Frame NW corner at the SW corner of the top level menu button
            for a top level menu with cascade_side RIGHT
        the Frame NE corner at the SE corner of the top level menu button
            for a top level menu with cascade_side LEFT
        the Frame NW corner at the NE corner of the parent menu Button for a
            sub-menu with cascade_side RIGHT
        the Frame NE corner at the NW corner of the parent menu button for a
            sub-menu with cascade_side LEFT
        It then packs all the widgets in the frame and (see above) may
        activate one of them
        """

        if self.is_posted :
            return

        # all the widgets in this menu
        self._menubuttons = []
        # all the widgets in this menu which can be ACTIVE and take focus
        self._selectables = []
        # all the bindings made when posting this object's menu
        self._bindings = []

        x, y, anchor = self._locate_place_point()

        # create and place the frame for this menu
        self._menu_frame = Frame( self._root, **self._menu_frame_kw )
        self._menu_frame.place( x = x, y = y, anchor = anchor)

        # the button we will make active, if there is one to choose
        self._active_button = None

        self.is_posted = True
        # we'll close all menus if the mouse is clicked outside of the
        # menu (or its child menus)
        if not self._is_submenu :
            self._add_binding( self._root, '<ButtonPress-1>',
                                self._close_event, '+' )
            self._add_binding( self._root, '<Configure>',
                               self._reconfigure, '+' )

        # go through the list of dictionaries for the widgets compromising
        # the menu and build the widgets
        for wdict in self._wdicts :
            # widget create arguments
            kw = wdict.get( 'kw', None )
            wtype = wdict[ 'type' ]
            if wtype == 'button' :
                w = Button( self._menu_frame, **kw )
                w.pack( side = TOP, expand = YES, fill = X )
                self._prepare_selectable( w, wdict )

            elif wtype == 'checkbutton' :
                w = Checkbutton( self._menu_frame, **kw )
                w.pack( side = TOP, expand = NO, fill = NONE, anchor = W )
                self._prepare_selectable( w, wdict )

            elif wtype == 'radiobutton' :
                w = Radiobutton( self._menu_frame, **kw )
                w.pack( side = TOP, expand = NO, fill = NONE, anchor = W )
                self._prepare_selectable( w, wdict )
                # set initial state of radio button
                x = kw.get( 'variable', None )
                v = kw.get( 'value', None )
                if ( v is not None ) and ( x is not None ) and x.get() == v :
                    w.select()
                else :
                    w.deselect()

            elif wtype == 'submenu' :
                w = Button( self._menu_frame, **kw )
                w.pack( side = TOP, expand = YES, fill = X )
                # run the child posting command before any command
                # configured for the widget itself
                command = lambda w = w : self._child_post( w )
                self._prepare_selectable( w, wdict, command )
                # bind return key to post sub-menu
                self._add_binding( w, '<Return>',
                                   self._child_post_and_activate, '+' )
                # arrange that mouse entering widget will auto-post
                # child when
                self._add_binding( w, '<Enter>', self._do_enter, '+'  )

                # allow use of an arrow key to move to the sub-menu
                if self._cascade_side ==  RIGHT :
                    self._add_binding(w, '<Right>',
                                      self._child_post_and_activate, '+' )
                else :
                    self._add_binding( w, '<Left>',
                                       self._child_post_and_activate, '+' )
            elif wtype == 'widget' :
                # we don't really know what this is, so we can't do a
                # few operations (passing focus for example)
                if len( wdict[ 'args' ] ) > 0 :
                    w = wdict[ 'widget_object' ]( self._menu_frame,
                                                *wdict[ 'args' ], **kw )
                else:
                    w = wdict[ 'widget_object' ]( self._menu_frame, **kw )

                w.pack( side = TOP, expand = NO, fill = X  )
                self._add_selectable( w, wdict )

            elif wtype == 'label' :
                w = Label( self._menu_frame, **kw )
                w.wdict = wdict
                w.pack( side = TOP, expand = NO, fill = X  )
                self._menubuttons.append( w )

            elif wtype == 'separator' :
                w = Label( self._menu_frame, relief = RIDGE, borderwidth = 1,
                           image = self._empty )
                w.wdict = wdict
                w.pack( side = TOP, expand = NO, fill = X  )
                self._menubuttons.append( w )

        # set up traversal using arrow keys
        self._link_arrows( True )
        # make a button in the new menu active if appropriate
        if activate_button and self._active_button :
            self._active_button.configure( state = ACTIVE )
            self._active_button.focus_set()

        # record the frame geometry for reconfiguraton
        self._frame_geom = self._menu_frame.winfo_geometry()

    def _reconfigure( self, event ) :

        sg = self.button.winfo_geometry()

        # if the button locating this menu hasn't moved,
        # then we don't have to do anything
        if  not self.is_posted or sg == self._self_geom :
            return

        # get the old button window co-ordinates and the current one
        old_b_x, old_b_y = re.match(
            r'\d+x\d+([+-]\d+)([+-]\d+)', self._self_geom ).groups()
        b_x, b_y = re.match(
            r'\d+x\d+([+-]\d+)([+-]\d+)',
            self.button.winfo_geometry() ).groups()
        # get the co_ordinates of our frame (these are relative to the
        # root window
        f_wh, f_x, f_y = re.match(
            r'(\d+x\d+)([+-]\d+)([+-]\d+)', self._frame_geom ).groups()
        # new placer locations are old x, y plus dx, dy
        dx = int( b_x ) - int( old_b_x )
        dy = int( b_y ) - int( old_b_y )
        # calculate where our frame will be now (needed for next config call)
        self._frame_geom = "%s%+d%+d" % (f_wh, int( f_x ) + dx,
                                            int( f_y ) + dy )

        x, y, anchor = self._locate_place_point()
        self._menu_frame.place_configure( x = x, y = y, anchor = anchor )

        if self._child is not None :
            self._child._child_reconfigure( dx, dy )

    def _child_reconfigure( self, dx, dy ) :
        """Parent menu has shifted, so move the child the same
         amount"""
        x, y, anchor = self._locate_place_point()
        self._menu_frame.place_configure( x = x + dx, y = y + dy,
                                          anchor = anchor )
        if self._child is not None :
            self._child._child_reconfigure( dx, dy )


    def _locate_place_point( self ) :
        """internal routine to calculate where to place a window
        returns a tuple( x, y, anchor ) where x, y are
        the window corner and anchor is the anchor"""
        # get the details of the button activating this menu
        bw = self.button.winfo_width()
        bh = self.button.winfo_height()
        bx = int( self.button.winfo_rootx() )
        by = int( self.button.winfo_rooty() )
        rx = int( self._root.winfo_rootx() )
        ry = int( self._root.winfo_rooty() )

        # work out the cumulative size of the borders of the menu to post
        # plus its parent menus
        border = self._menu_frame_kw.get( 'borderwidth', 0 )
        border += self._root.cget( 'borderwidth' )
        if self._parent is not None :
            border += self._parent._menu_frame_kw.get( 'borderwidth', 0 )

        if not self._is_submenu :
            # for the top level, the menu is aligned from the main
            # button and directly below
            y = bh + by - ry + border     # south
            if self._cascade_side == RIGHT :
                x = bx - rx - border      # west
                anchor = NW
            else :
                x = bx - rx + bw + border # east
                anchor = NE
        else :
            # submenu, build to one side of the button causing this
            # menu to be posted
            y = by - ry           # north
            if self._cascade_side == LEFT :
                x = bx - rx - border
                anchor = NE
            else :
                x = bw + bx - rx  + border
                anchor = NW

        # save root dimensions for later
        self._rx = rx
        self._ry = ry
        self._root_geom = root.winfo_geometry()
        self._self_geom = self.button.winfo_geometry()
        return ( x, y, anchor )


    def _link_arrows( self, do_binding ) :
        """Internal routine to set links for menu traversal"""

        # we won't bother if there's only one item in the menu
        if len( self._selectables ) < 1 :
            return

        for i in range( len( self._selectables ) ) :
            w = self._selectables[ i ]
            wtype =  w.wdict[ 'type' ]
            # skip over widgets with the arrow keys
            if wtype != 'widget' :
                w.wnext = self._selectables[ ( i + 1 ) %
                                            len( self._selectables ) ]
                w.wprev = self._selectables[ i - 1 ]
                if do_binding :
                    self._bind_traversal( w )

    def _bind_traversal( self, w ) :
        """Internal routine to bind arrow keys and focus for menu
        traversal"""
        self._add_binding( w, '<FocusIn>', self._do_focus_in, '+' )
        self._add_binding( w, '<Up>', self._menu_traverse, '+' )
        self._add_binding( w, '<Down>', self._menu_traverse, '+' )
        self._add_binding( w, '<Escape>', self._close_event, '+' )
        try :
            ul = w.cget( 'underline' )
            txt = w.cget( 'text' ).lower()
            if ul is not None and  ul >=  0 and txt is not None :
                self._add_binding(
                    root, "<Alt-%s>" % (txt[ ul ] ),
                    lambda e, w = w : self._do_hotkey( w, e ), '+' )
        except :
            pass

        # if we're a child menu, allow arrow keys to move back from
        # child to parent
        if self._is_submenu :
            if self._cascade_side == RIGHT :
                self._add_binding( w, '<Left>', self._activate_top, '+' )
            else :
                self._add_binding( w, '<Right>', self._activate_top, '+' )

    def _add_binding( self, w, event, command, *args ) :
        """internal command to bind an event to a widget and record it in the
        list of bindings"""
        self._bindings.append( ( w, event, w.bind( event, command, *args ) ) )

    def _prepare_selectable( self, w, wdict,
                              command = None,
                              allow_active = False ) :
        """internal command to set widget state to NORMAL and add it to
        the selectables list"""

        # reset the command to an internal one
        if command is None:
            command = lambda w = w : self._run_command( w )
        w.configure( command = command )
        self._add_selectable( w, wdict, allow_active )

        self._add_binding( w, '<Enter>', self._do_enter, '+' )

    def _add_selectable( self, w, wdict, allow_active = False ) :
        """Internal routine to add a widget to the list of selectable ones"""

        kw = wdict.get( 'kw', None )
        # override any attempt to set this widget active
        # remember the first selectable item in a menu
        try :
            state = w.cget( 'state' )
            if state == ACTIVE :
                w.configure( state = NORMAL )
            if state != DISABLED and self._active_button is None :
                self._active_button = w
        except :
            pass

        # run any user callbacks for post-creation of widget
        w.kw = kw
        w.wdict = wdict
        if wdict.get( 'pre_pack_command', None ) is not None :
            wdict[ 'pre_pack_command' ]( w )

        # ensure we see any selection before the user supplied command
        if kw.get( 'command', None) is not None :
            self._add_binding( w, '<Return>', self._enter_key, '+' )

        self._selectables.append( w )
        self._menubuttons.append( w )

    def _child_post_and_activate( self, event ) :
        """internal method - post sub-menu when an event occurs
        (mouse, Enter key)."""

        # figure out where we were called from, then post the child
        w = event.widget
        self._child_post( w, True )

    def _child_post( self, w, activate = True ) :
        """internal method - post sub-menu when button selected, passed
        the widget for the menu button which is associated with the sub-menu.

        If called with activate = True, then focus moves to the sub-menu
        """

        # find the child menu object
        wdict = w.wdict
        child = wdict.get( 'sub_menu', None )

        if child is None :
            return

        # if child is already posted, we've little to do
        if self._child == child and child.is_posted :
            w.configure( state = NORMAL )
            try :
                if child._active_button :
                    child._active_button.configure( state = ACTIVE )
                    child._active_button.focus_set()
            except:
                pass
            return

        # if we have some other child posted, get rid of it
        if self._child :
            self._child.unpost()

        w.configure( state = NORMAL )

        # link child object to us and vice-versa        child._parent = self
        self._child = child
        self._current_widget = w
        child._cascade_side = self._cascade_side
        child.button = w
        child.post( None, activate )

    def unpost( self, event = None ) :
        """remove a menu and all its children"""

        if not self.is_posted :
            return

        # kill children off first
        if self._child :
            self._child.unpost()

        self.is_posted = False

        # remove any bindings which apply to widgets in this menu
        for ( widget, event, id ) in self._bindings :
            widget.unbind( event, id )

        # then zap all the widgets in this menu
        for w in self._menubuttons :
            w.destroy()

        self._menu_frame.destroy()

        # remove any linkages if we're a child menu
        if self._parent :
            parent = self._parent
            self._parent._child = None
            self._parent = None

    def _activate_top( self, event ) :
        """internal routine to reset focus to menu button which
        opens sub-menu. Used when an arrow key is used in a sub-menu
        to return to the parent menu"""

        w = event.widget
        if self._parent is not None and self._parent._current_widget :
            w.configure( state = NORMAL )
            w = self._parent._current_widget
            w.configure( state =  ACTIVE )
            w.focus_set()

    def _main_button_select( self, event = None ) :
        """internal routine - posts the main menu then runs any associate
        command"""

        self.post( None, True )
        if self._mainbutton_kw.get( 'command', None ) is not None :
            self._mainbutton_kw[ 'command' ]()

    def _is_my_window( self, x, y ) :
        """internal method - return TRUE if x,y co-ordinates are in a posted
        menu for this object - used when deciding if a mouse click happened
        within a menu. The mouse-click event handler will chase down the
        chain of children, so the code isn't here"""

        if not self.is_posted :
            return False

        wh = self._menu_frame.winfo_height()
        ww = self._menu_frame.winfo_width()
        nwx = int( self._menu_frame.winfo_rootx() )
        nwy = int( self._menu_frame.winfo_rooty() )

        return x >= nwx and x <= ( nwx + ww ) and \
                   y >= nwy and y <= ( nwy + wh )

    def _close_event( self, event ) :
        """internal method - closes all menus of this object if event
        was mouse leftt click outside all menus or was Escape on any
        selectable menu widget. If it was Escape, only the current menu
        and any children are closed. If it was a mouse click,everything is
        closed
        """

        if event.keysym != 'Escape' :
           # mouse click - pass to highest level menu, so close will get
            # to everything
            if self._parent :
                self._parent._close_event( event )
                return
            # we're the top level menu and we've seen a mouse click, see if
            # it's within our frame or a child or ours'
            x = int( event.x_root )
            y = int( event.y_root )
            if self._is_my_window( x, y ) :
                return

            child = self._child
            while child :
                if child._is_my_window( x, y ) :
                    # bail out without action if mouse click was within a child
                    return
                child = child._child

        # in all other cases, close this menu and its children
        self.unpost()

    def _menu_traverse( self, event ) :
        """internal routine - handles arrow key navigation"""

        w = event.widget
        if event.keysym == 'Up' :
            tgt = w.wprev
        else :
            tgt = w.wnext

        w.configure( state = NORMAL )
        tgt.focus_set()

    def add_main_button( self, **kw ) :
        """Define the Main button for the menu (must be called before
        packing topmost ExtraMenu object
        Arguments: keyword arguments are the same as for any Button
        """
        self._mainbutton_kw = kw

    def add_command( self, **kw ) :
        """create a Button within a menu. When the menu is posted, it will
        be pack()ed with options side = TOP, expand = YES, fill = X
        Enter will be bound for the Button and will execute any command
        supplied as an argument.
        Escape will be bound for the Button and will close the menu
        containing the Button
        Arguments: same keyword arguments as for any Button object with the
            addition of:
          pre_pack_command - an optional callback which will be called with
              the Button object as an argument, just before packing the
              Button when posting a menu

        Returns: integer widget id, -1 on failure
        """
        return self._add_widget( 'button', None, **kw )

    def add_separator( self ) :
        """create a separator in a menu - uses a 1 pixel border
        around a one pixel bitmap
        it will be pack()ed with options side = TOP, expand = YES, fill = X
        Returns: integer widget number, -1 on failure"""
        return self._add_widget( 'separator', {} )

    def add_label( self, **kw ) :
        """create a label in a menu
        It will be pack()ed with options side = TOP, expand = YES, fill = X
        Arguments: same keyword agruments as for a Label
        Returns: integer widget id, -1 on failure"""
        return self._add_widget( 'label', None, **kw )

    def add_checkbutton( self, **kw ) :
        """Create a checkbutton button in the menu.
        It will be pack()ed with options
          expand = NO, fill = NONE, anchor = W
        Arguments: same keyword arguments as a Checkbutton with the
              addition of:
          pre_pack_command - an optional callback which will be called with
              the Checkbutton object as an argument, just before packing
              the Checkbutton when posting a menu

        Returns: integer widget id, -1 on failure"""
        return self._add_widget( 'checkbutton', None, **kw )

    def add_radiobutton( self, **kw ) :
        """Create a RadioButton in the menu.
        Arguments: same keyword arguments as a Radiobutton with the
              addition of:
          pre_pack_command - an optional callback which will be called with
              the Radiobutton object as an argument, just before packing
              the Radiobutton when posting a menu
        Returns: integer widget id, -1 on failure"""
        return self._add_widget( 'radiobutton', None, **kw )

    def add_special_widget( self, *args, **kw ) :
        """Create a one item menu with an arbitrary widget
        object
        Arguments: positional arguments will be passed to the widget
              constructor. Do not include a first agrument of a Frame,
              this is added at construction time
              keyword arguments are passed to the widget constructor,
              except for the following, removed and used by the ExtraMenu
              itself
          widget_object = The widget class name, used to construct
              the widget at pack() time.
          pre_pack_command - an optional callback which will be called
              with the widget as an argument, just before packing the
              widget when posting a menu

        There can be no other widgets in the same sub-menu.
        Returns: integer widget id, always 0 on OK
                 -1 on attempt to add anything to this menu
                 or if menu is currently posted"""

        return self._add_widget( 'widget', *args, **kw )

    def add_submenu( self, sub_menu_ref,  **kw ) :
        """Create a Button linked to an sub-menu
        The Button will have the appropriate arrow key bound to post the
        the sub-menu, as well as the Enter key. If a command keyword
        argument is supplied, the sub-menu will be posted, then the
        command will be executed.
        Every Button, CheckButton and RadioButton in the sub-menu will
        have the appropriate Arrow key bound to return to this Button.
        Every Button, CheckButton and RadioButton in the sub-menu will
        have Escape bound to unpost the sub-menu
        Arguments:
          sub_menu_ref = another-ExtraMenu-object : the submenu to post when
              this Button is selected (or to auto-post, see below)
          same keyword arguments as a Button with the addition of:
          auto_post =  if True, the sub-menu is posted whenever
              the button is Active (the user need not click on the menu).
              The sub-menu will be unpost()ed when any other widget in this
              ExtraMenu becomes active. When False, the user must actually
              select this button (with the mouse or Enter key) to post the
              sub-menu. The sub-menu will stay posted until closed by the
              user or if another sub-menu from this ExtraMenu is posted
              default = False
          pre_pack_command - an optional callback, called with the Button
              object as an argument, just before packing the widget when
              posting a menu
        Returns: integer widget id, -1 on failure"""
        kw[ 'sub_menu' ] = sub_menu_ref
        sub_menu_ref._is_submenu = True
        return self._add_widget( 'submenu', **kw )

    def _add_widget( self, wtype, *args, **kw ) :
        """internal routine to capture details of widget to add to menu."""

        # we never add widgets when the menu is posted
        if self.is_posted :
            return -1

        wdict = {}
        wdict[ 'type' ] = wtype
        self._button_no += 1
        wdict[ 'widget_id' ] =  self._button_no

        # process any options applicable to us rather than the widget
        # we remove these from the keywords dictionary, because we'll
        # be using the remaining keywords when we create the widget

        insert_before = kw.pop( 'insert_before', None )
        wdict[ 'auto_post' ] = kw.pop( 'auto_post', False)
        wdict[ 'sub_menu' ] = kw.pop( 'sub_menu', None )
        wdict[ 'pre_pack_command' ] = kw.pop( 'pre_pack_command', None )
        wclass = kw.pop( 'widget_object', None )

        # save the keywords and positional arguments
        wdict[ 'args'] = args
        wdict[ 'kw' ] = kw

        if  wtype != 'widget' :
            # refuse to mix random widgets with normal menu components
            if len( self._wdicts ) > 0 and \
                   self._wdicts[ 0 ][ 'type' ] == 'widget' :
                return -1
        else :
            if len( self._wdicts ) != 0 :
                return -1

            if wclass is None :
                return -1

            wdict[ 'widget_object' ] = wclass

        # add to list of widgets in the appropriate place
        if insert_before is None:
            self._wdicts.append( wdict )
        else :
            for i in range( len( self._wdicts ) ) :
                if self._wdicts[ i ][ 'widget_id' ] == insert_before :
                    self._wdicts = self._wdicts[ : i ] + [ wdict ] + \
                                  self._wdicts[ i : ]
                    return self._button_no

            self._wdicts.append( wdict )

        return self._button_no

    def delete_widget( self, widget_id ) :
        """Delete a widget from a menu. Menu must not be posted when
        this is called.
        Arguments: widget id
        Returns: 0 on failure, 1 on OK"""

        # don't delete anything from an active menu
        if self.is_posted :
            return 0

        # removing it from the list of dictionaries is sufficient
        for i in range( len( self._wdicts ) ) :
            if self._wdicts[ i ][ 'widget_id' ] == widget_id :
                self._wdicts[ i : i + 1 ] = []
                return 1

        return 0

    def enable_widget( self, widget_id ) :
        """Change state of a widget from DISABLED to NORMAL
        This call can be made while an ExtraMenu is posted
        Arguments: widget id (the number returned by add_xxx call)
        Returns: nothing"""

        # find which widget we're talking about
        for i in range( len( self._wdicts ) ) :
            if self._wdicts[ i ][ 'widget_id' ] == widget_id :
                break
        else :
            return

        # if not posted, simply adding to the keywords will be enough
        wdict = self._wdicts[ i ]
        if not self.is_posted :
            wdict[ 'kw' ].setdefault( 'state', ENABLE )
            return

        # find the widget itself
        for w in self._menubuttons :
            if w.wdict == wdict :
                break
        else :
            # this should never happen, it implies there is a dictionary
            # for a widget which was not created when posting the menu
            return

        if w.cget( 'state' ) != DISABLED :
            return

        w.configure( state = NORMAL )

        # add the widget in the appropriate place in selectables list
        self._selectables = [ sw for sw in self._selectables if
                             sw.wdict in self._wdicts[ : i ] ] + \
                             [ w ] + [ sw for sw in self._selectables if
                                   sw.wdict in self._wdicts[ i : ] ]
        self._link_arrows( False )
        self._bind_traversal( w )

    def disable_widget( self, widget_id ) :
        """Change state of a widget from NORMAL to DISABLED
        Widget must not be both currently be displayed and ACTIVE
        (NORMAL is OK even if the widget is displayed)
        Arguments: widget id (the number returned by add_xxx call)
        Returns: nothing"""
        for i in range( len( self._wdicts ) ) :
            if self._wdicts[ i ][ 'widget_id' ] == widget_id :
                break
        else :
            return

        wdict = self._wdicts[ i ]
        if not self.is_posted :
            wdict[ 'kw' ].setdefault( 'state', DISABLE )
            return

        # remove this widget from the selectables list and remove any
        # keybindings for it
        for w in self._menubuttons :
            if w.wdict == wdict :
                break
        else :
            # this should never happen, it implies there is a dictionary
            # for a widget which was not created when posting the menu
            return

        if w.cget( 'state' ) != NORMAL :
            return
        w.configure( state = DISABLED )

        for  sw, event, id in self._bindings :
            if sw != w :
                continue
                sw.unbind( event, id )

        self._bindings = [ x for x in self._bindings if x[ 0 ] != w ]
        self._selectables = [ x for x in self._selectables if x != w ]
        self._bind_traversal( w )
        self._link_arrows( False )

    def set_widget_options( self, widget_id, **kw ) :
        """Add or update the keyword options for a menu widget
        These should not be used to alter the displayed appearance of
        a widget that is currently posted, as the results are unpredictable
        Setting an option to None will remove it from the dictionary
        Arguments: widget_id - the number returned when the widget was added
            to the menu with an add_xxx command.
            kw = keyword/value pairs
        Returns: nothing
        """
        for i in range( len( self._wdicts ) ) :
            if self._wdicts[ i ][ 'widget_id' ] == widget_id :
                break
        else :
            return

        wdict = self._wdicts[ i ]

        if self.is_posted :
            for w in self._menubuttons :
                if w.wdict == wdict :
                    break
            else :
                # this should never happen, it implies there is a
                # dictionary for a widget which was not created when
                # posting the menu
                return

        # deal with options meant for this menu
        for key in [ 'auto_post', 'pre_pack_command', 'widget_object' ] :
            if kw.has_key( key ) :
               val = kw.pop( key )
               if val is None:
                   wdict.pop( key )
               else:
                   wdict[ key ] = val
        # then deal with options meant for the widget
        for ky in kw.keys() :
            val = kw[ ky ]
            if val is None :
                wdict[ 'kw' ].pop( ky )
            else :
                wdict[ 'kw'][ ky ] = val
                if self.is_posted :
                    w.configure( { ky: val } )

    def get_widget_from_id( self, widget_id ) :
        """Return a reference to the widget option in a posted menu
        This routine requires care, as widgets only exist while their menu
        is posted, unpost() calls widget.destroy()
        Arguments: widget_id
        Returns: reference to widget or None if no such widget exists at this
            time"""
        if not self.is_posted :
            return None

        for i in range( len( self._wdicts ) ) :
            if self._wdicts[ i ][ 'widget_id' ] == widget_id :
                break
        else :
            return None

        for w in self._menubuttons :
            if w.wdict == wdict :
                break
        else:
            return None

        return w

    def _do_focus_in( self, event ) :
        """internal event handler when focus hits a widget"""
        me = event.widget
        if me.cget( 'state' ) == DISABLED or  me.cget( 'state' ) == ACTIVE :
            return

        self._enter_or_focus( me )

    def _do_enter( self, event ) :
        """internal routine for mouse entering a widget"""
        me = event.widget
        if me.cget( 'state' ) == DISABLED :
            return

        if me.focus_get() != me :
            me.focus_set()

        self._enter_or_focus( me )

    def _do_hotkey( self, me, *args ) :
        if me.cget( 'state' ) == DISABLED :
            return

        if me.focus_get() != me :
            me.focus_set()

        self._enter_or_focus( me )

    def _enter_or_focus( self, me ) :
        """internal common code for a button being activated>"""
        # do any needed auto posting
        self._post_cascade( me )
        for w in self._selectables :
            if w != me :
                if w.cget( 'state' ) != ACTIVE :
                    continue
                else :
                    w.configure( state = NORMAL )
            else :
                me.configure( state = ACTIVE )

    def _post_cascade( self, w ) :
        """internal routine to post sub-menus when button is active. This also
        handles removing other sub-menus of the current menu"""

        wdict = w.wdict
        # close any other children that are up
        child = wdict.get( 'sub_menu', None )
        if self._child :
            if child is None or child != self._child :
                self._child.unpost()

        # then post our own children
        if wdict.get( 'auto_post', False ) and child is not None :
            self._child_post( w, False )

    def _enter_key( self, event ) :
        """internal routine to run the command associated with a button when
        the Enter key is pressed (used because we rebind this key for the
        widget). Otherwise, the original command might not expect an event"""
        w = event.widget
        self._run_command( w )

    def _run_command( self, w ) :
        """internal routine to run the command associated with a button when
        the mouse is clicked on it (we don't bind the mouse click ourselves,
        but we have over-ridden the original command binding"""

        kw = w.kw
        if  w.focus_get() != w :
            w.focus_set()

        if kw.get( 'command', None ) :
            kw[ 'command' ]()

if __name__ == '__main__' :

    import Pmw
    import os
    import re
    root = Tk()

    Pmw.initialise( root )

    root.geometry( "600x600" )

    # frame for the menu bars

    menu_frame = Frame( root, relief = RIDGE, borderwidth = 2 )
    menu_frame.pack( side = TOP, expand = NO, fill = X )    # a combo box allowing you to choose a directory
    # the files in the directory will be the options in an OptionMenu

    directory = '.'
    dirs = []

    file_entry = StringVar()
    file_entry.set( "no choice" )
    files = [ "no choice " ]
    fileindex = 0

    caseless = IntVar()
    caseless.set(True )
    sort_dirs = IntVar()
    sort_dirs.set( True )
    sort_files = IntVar()
    sort_files.set(True )

    # command to be run after creating the ComboBox widget ( e.g. everytime the
    # combo box is posted )
    def dir_setup ( w ):
        global dirs, directory, caseless, sort_dirs
        # get the dirs
        dirs = [ '.', '..' ] + [ f for f in os.listdir( directory ) if
                                 os.path.isdir( os.path.join( directory, f )) ]
        # kill off the leading path
        dirs = [ re.sub( '.*%s' % os.path.sep, '', x ) for x in dirs ]
        # sort as requested
        if sort_dirs.get() :
            if not caseless.get() :
                dirs.sort( lambda x, y : cmp( len( x ), len( y ) ) or
                           cmp( x, y ) )
            else :
                dirs.sort( lambda x, y : cmp( x.lower(), y.lower() ) )

        w.setlist( dirs )
        w.selectitem( '.', 0 )
        w.component( 'entry' ).config( background = "#ffffff" )

    def set_dir( dir_entry ) :
        global dirs, directory
        directory = os.path.normpath( os.path.join( directory, dir_entry ) )
        # remove the popup menu
        emrcmb.unpost()

    # similar command to run before posting OptionMenu
    def files_setup( w ) :
        global directory, files, fileindex, sort_files, caseless, file_entry
        files = [ f for f in os.listdir( directory ) if
                  os.path.isfile( os.path.join( directory, f ) ) ]

        if sort_files.get() :
            if not caseless.get() :
                files.sort()
            else :
                files.sort( lambda x, y : cmp( len( x ), len( y ) ) or\
                           cmp( x, y ) )
        files = [ "no choice" ] + files
        try :
            fileindex = files.index( file_entry.get() )
        except ValueError :
            fileindex = files.index( "no choice" )
        w.setitems( files[ : fileindex ] + files[ fileindex + 1: ] )
        w.setvalue( files[ fileindex ] )

    def select_file( entry ) :
        global file_entry
        file_entry.set( entry )

    emrcmb = ExtraMenu( None, root, relief = RAISED, borderwidth = 2,
                       is_submenu = True  )
    emrcmb.add_special_widget( label_text='Directory', labelpos='wn',
                              listbox_width = 64, dropdown = 1,
                              scrolledlist_items = dirs,
                              selectioncommand = set_dir,
                              # options special to ExtraMenus:
                              pre_pack_command = dir_setup,
                              widget_object = Pmw.ComboBox)

    # an option menu with a list of files for the selected directory

    emropt = ExtraMenu( None, root, relief = RAISED, borderwidth = 2,
                       is_submenu = True  )

    emropt.add_special_widget(
        label_text = 'File', labelpos = W,
        menubutton_textvariable = "no choice",
        items = [], command = select_file,
        # options related to an ExtraMenu:
        widget_object = Pmw.OptionMenu,
        pre_pack_command = files_setup )

    # a sample cascade menu
    sub_cbvar = IntVar()
    sub_cbvar.set( False )
    sub_rbvar = IntVar()
    sub_rbvar.set( 6 )

    def create_items (menu, itemlist ) :
        for item in itemlist :
            if item[ 1 ] == "add_command" :
                cmd = "%s.%s( text = '%s', relief = RAISED,"\
                      "borderwidth = 0 %s )" \
                      % tuple( [ menu] + item[ 1 :  ] )
            if item[ 1 ] == "add_label" :
                cmd = "%s.%s( text = '%s', relief = RAISED,"\
                      "borderwidth = 0 %s )" \
                      % tuple( [ menu] + item[ 1 :  ] )
            elif item[ 1 ] == "add_separator" :
                cmd = "%s.%s()" % tuple( [ menu] + item[ 1 : ] )
            elif item[ 1 ] == "add_checkbutton" :
                cmd = "%s.%s( text = '%s', relief = RAISED, "\
                      "borderwidth = 0, variable = %s %s )" \
                      % tuple( [ menu] + item[ 1 : ] )
            elif item[ 1 ] == "add_radiobutton" :
                cmd = "%s.%s( text = '%s', relief = RAISED, "\
                      "borderwidth = 0, variable = %s, value = %s %s )" \
                      % tuple( [ menu] + item[ 1 : ] )
            elif item[ 1 ] == "add_submenu" :
                cmd = "%s.%s( %s, text = '%s', relief = RAISED, "\
                          "borderwidth = 0, auto_post = %s %s ) " \
                          % tuple( [ menu] + item[ 1 : ] )
            # store the widget id
            item[ 0 ] = eval( cmd )

    submenu_items = [
        #     command, text, relief, borderwidth, variable, value
        [ 0, "add_command", 'Sub One', '' ],
        [ 0, "add_command", 'Sub Two', '' ],
        [ 0, "add_separator" ],
        [ 0, "add_command", 'Sub Three', '' ],
        [ 0, "add_command", 'Sub Four' , '' ],
        [ 0, "add_separator" ],
        [ 0, "add_checkbutton", 'Sub Enabled', 'sub_cbvar', '' ],
        [ 0, "add_separator" ],
        [ 0, "add_radiobutton", 'Sub Choice 1', 'sub_rbvar', '2', '' ],
        [ 0, "add_radiobutton", 'Sub Choice 2', 'sub_rbvar', '4', '' ],
        [ 0, "add_radiobutton", 'Sub Choice 3', 'sub_rbvar', '6', '' ],
        ]

    emrsub = ExtraMenu( None, root, relief = RAISED, borderwidth = 2,
                       is_submenu = True  )
    create_items( "emrsub", submenu_items )

    # main menu

    enable_dir = IntVar()
    enable_dir.set( True )

    auto_post_sub = IntVar()
    auto_post_sub.set( 0 )

    def toggle_dir_choice() :
        global enable_dir, r_menu_items
        entry = enable_dir.get()
        if entry :
            emr.enable_widget( r_menu_items[ 1 ][ 0 ] )
        else :
            emr.disable_widget( r_menu_items[ 1 ][ 0 ] )

    def toggle_sub_auto() :
        global auto_post_sub, r_menu_items
        if auto_post_sub.get():
            txt = "AutoMenu"
        else :
            txt = "Sub Menu"

        emr.set_widget_options( r_menu_items[ 4 ][ 0 ],
                                text = txt, auto_post = auto_post_sub.get() )
    r_menu_items = [
        #     command, [submenu], text, auto_post/var, val, extra args
        [ 0, "add_command", 'One', '' ],
        [ 0, "add_submenu", 'emrcmb', 'Choose Dir', 'True',
          ', underline = 7' ],
        [ 0, "add_submenu", 'emropt', 'Choose File', 'True',
          ', underline = 7' ],
        [ 0, "add_separator" ],
        [ 0, "add_submenu", 'emrsub', 'Sub Menu', 'False', '' ],
        [ 0, "add_command", 'Four', '' ],
        [ 0, "add_separator" ],
        [ 0, "add_radiobutton", 'Sort Caseless', 'caseless', '1',
          ', underline = 5' ],
        [ 0, "add_radiobutton", 'Sort by Len', 'caseless', '0', ''],
        [ 0, "add_separator" ],
        [ 0, "add_checkbutton", 'Sort Dirs',  'sort_dirs', ''   ],
        [ 0, "add_checkbutton", 'Sort Files', 'sort_files', ''  ],
        [ 0, "add_checkbutton", 'Enable Dirs', 'enable_dir',
          ', command = toggle_dir_choice' ],
        [ 0, "add_checkbutton", 'AutoPost',    'auto_post_sub', '' ]
        ]

    emr = ExtraMenu( menu_frame, root, cascade_side = LEFT,
                    relief = RAISED, borderwidth = 2  )
    emr.add_main_button( text = 'Right', relief = FLAT, underline = 0 )
    create_items( "emr", r_menu_items )

    # we can use set_widget_options as well
    emr.set_widget_options( r_menu_items[ 13 ][0], command = toggle_sub_auto )

    emr.pack( menu_frame, expand = NO, fill = None, side = RIGHT )

    # a two deep left hand menu
    subl2_cbvar = IntVar()
    subl2_cbvar.set( False )
    subl2_rbvar = IntVar()
    subl2_rbvar.set( 6 )

    subl2_menu_items = [
        #     command, text, relief, borderwidth, variable, value
        [ 0, "add_command", 'Left-2 One', '' ],
        [ 0, "add_command", 'Left-2 Two', '' ],
        [ 0, "add_separator" ],
        [ 0, "add_command", 'Left-2 Three', '' ],
        [ 0, "add_command", 'Left-2 Four' , '' ],
        [ 0, "add_separator" ],
        [ 0, "add_checkbutton", 'Left-2 Enabled', 'subl2_cbvar', '' ],
        [ 0, "add_separator" ],
        [ 0, "add_radiobutton", 'Left-2 Choice 1', 'subl2_rbvar', '2', '' ],
        [ 0, "add_radiobutton", 'Left-2 Choice 2', 'subl2_rbvar', '4', '' ],
        [ 0, "add_radiobutton", 'Left-2 Choice 3', 'subl2_rbvar', '6', '' ],
        ]

    em_l2sub = ExtraMenu( None, root, relief = RAISED, borderwidth = 2,
                          is_submenu = True  )
    create_items( "em_l2sub", subl2_menu_items )

    subl1_cbvar = IntVar()
    subl1_cbvar.set( False )
    subl1_rbvar = IntVar()
    subl1_rbvar.set( 6 )

    subl1_menu_items = [
        #     command, text, relief, borderwidth, variable, value
        [ 0, "add_command", 'Left-1 One', '' ],
        [ 0, "add_submenu", 'em_l2sub', 'Left- SubMenu', 'True', '' ],
        [ 0, "add_separator" ],
        [ 0, "add_command", 'Left-1 Three', '' ],
        [ 0, "add_command", 'Left-1 Four' , '' ],
        [ 0, "add_separator" ],
        [ 0, "add_checkbutton", 'Left-1 Enabled', 'subl1_cbvar', '' ],
        [ 0, "add_separator" ],
        [ 0, "add_radiobutton", 'Left-1 Choice 1', 'subl1_rbvar', '2', '' ],
        [ 0, "add_radiobutton", 'Left-1 Choice 2', 'subl1_rbvar', '4', '' ],
        [ 0, "add_radiobutton", 'Left-1 Choice 3', 'subl1_rbvar', '6', '' ],
        ]

    em_l1sub = ExtraMenu( None, root, relief = RAISED, borderwidth = 2,
                          is_submenu = True  )
    create_items( "em_l1sub", subl1_menu_items )


    button5 = 0

    # button to add an extra button to right menu
    def add_button_5() :
        global emr, r_menu_items, button5

        print "add_button5 ",
        # put it after the 'Four' button, before the separator
        ind = r_menu_items[ 6 ][ 0 ]
        if button5 > 0 :
            print "failed"
            return

        button5 = emr.add_command( text = 'Five', relief = RAISED,
                                   borderwidth = 0, insert_before = ind )
        print button5
    # button to delete the extra button from right menu
    def del_button_5() :
        global emr, button5

        if button5 <= 0 :
            print "not there"
            return

        if emr.delete_widget( button5 ) :
            button5 = 0
            return


    lmain_menu_items = [
        [ 0, "add_command", 'One', '' ],
        [ 0, "add_label", 'A label', '' ],
        [ 0, "add_submenu", 'em_l1sub', 'Left-SubMenu', 'True', '' ],
        [ 0, "add_separator" ],
        [ 0, "add_command", 'Add Button', ', command = add_button_5' ],
        [ 0, "add_command", 'Del Button' , ', command = del_button_5' ],
        [ 0, "add_separator" ],
        [ 0, "add_command", 'Quit',
          ', command = lambda e = 0 : sys.exit( e ) ' ]
        ]

    eml = ExtraMenu( menu_frame, root, cascade_side = RIGHT,
                    relief = RAISED, borderwidth = 2  )
    eml.add_main_button( text = 'Left', relief = FLAT, underline = 0 )
    create_items( "eml", lmain_menu_items )
    eml.pack( menu_frame, expand = NO, fill = None, side = LEFT )

    root.mainloop()
