package require MegaWidget
package provide XYText 1.0

namespace eval XYText {

#-----------------------------------------------------------------------------
#
#   XYText::Create
#
#   Creates an mega-widget with a contained text widget and X and Y
#   scrollbars.
#
#   Returns     :   Name of the main frame containing the XYText widget
#
#   Parameters  :
#       hWnd    :   Name of the main frame of the XYText widget
#       args    :   Options for the text widget (not currently used)
#
#   Side Effects:   Creates a frame containing text and scrollbar widget.
#
#----------------------------------------------------------------------------

    proc XYText { hWnd args } {

        frame $hWnd -bd 1 -relief sunken

        set hWndTxt \
            [text $hWnd.txt                             \
                -bd         0                           \
                -relief     flat                        \
                -xscroll    "$hWnd.scrX set"            \
                -yscroll    "$hWnd.scrY set"            \
                -wrap       none                        \
            ]

        set hWndXScr \
            [scrollbar $hWnd.scrX                       \
                -orient     horizontal                  \
                -command    "$hWndTxt xview"            \
            ]

        set hWndYScr \
            [scrollbar $hWnd.scrY                       \
                -orient     vertical                    \
                -command    "$hWndTxt yview"            \
            ]

        set hWndBox \
            [frame $hWnd.frBox                          \
                -bd         1                           \
                -relief     raised                      \
            ]

        grid rowconfig $hWnd 0 -weight 1 -minsize 0
        grid rowconfig $hWnd 1 -weight 0 -minsize 0
        grid columnconfig $hWnd 0 -weight 1 -minsize 0
        grid columnconfig $hWnd 1 -weight 0 -minsize 0

        grid $hWndTxt -row 0 -column 0 -sticky news
        grid $hWndYScr -row 0 -column 1 -sticky ns
        grid $hWndXScr -row 1 -column 0 -sticky ew
        grid $hWndBox -row 1 -column 1 -sticky news

        MegaWidget $hWnd

        return $hWnd
    }

    # Create XYText MegaWidget commands to be passed on to the text widget.

    foreach textCmd [list bbox cget compare configure debug delete \
        dlineinfo dump get image index insert mark scan search see \
        tag window xview yview] {

        proc $textCmd { hWnd args } "
            return \[eval \$hWnd.txt $textCmd \$args\]
        "
    }
}
