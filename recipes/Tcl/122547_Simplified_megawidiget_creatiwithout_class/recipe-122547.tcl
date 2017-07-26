package provide MegaWidget 1.0

proc MegaWidget { hWnd } {
    variable widgetClasses

    # Get the namespace for the mega-widget from the caller

    set NS [uplevel namespace current]

    # If the widget has already been turned into a mega-widget, just insert
    # the new namespace into the top of the search list and return.

    if {[info exist widgetClasses($hWnd)]} {
        set widgetClasses($hWnd) [linsert $widgetClasses($hWnd) 0 $NS]
        return
    }

    # The widget has yet been turned into a mega-widget.  Store the
    # caller's namespace as the first in the search list.

    set widgetClasses($hWnd) $NS

    # Rename the widget command to something in this procedure's namespace
    # so that calls to the widget command are not sent to the widget directly.

    rename ::$hWnd [namespace current]::mega$hWnd

    # Set up binding to clear the search list for the widget and delete
    # the replacement procedure for the widget command.  Make sure that
    # the widget generating the event is the same as the widget that was
    # turned into a mega-widget: this allows a toplevel to be turned
    # into mega-widget too (otherwise, it will get <Destroy> events from
    # child windows).

    set template {
        if {[string match %W @HWND@]} {
            namespace eval @MYNS@ array unset widgetClasses %W
            rename %W {}
        }
    }

    regsub -all {@HWND@} $template $hWnd template
    regsub -all {@MYNS@} $template [namespace current] template

    bind $hWnd <Destroy> $template

    # Create a new top-level procedure with the same name as the widget.
    # This procedure will scan through the search list for a namespace
    # containing a procedure by the same name as the first argument passed
    # to this new procedure.

    set template {
        global errorInfo errorCode
        variable widgetClasses

        set hWnd @HWND@

        foreach NS $@MYNS@::widgetClasses($hWnd) {
            if {[namespace inscope $NS info proc $command] == $command} {
                set rc [catch { uplevel [set NS]::$command $hWnd $args } result]
                set ei $errorInfo
                set ec $errorCode
                break
            }
        }

        if {![info exist rc]} {
            set rc [catch { uplevel @MYNS@::mega$hWnd $command $args } result]
            set ei $errorInfo
            set ec $errorCode
        }
        return -code $rc -errorinfo $ei -errorcode $ec $result
    }

    regsub -all {@HWND@} $template $hWnd template
    regsub -all {@MYNS@} $template [namespace current] template

    proc ::$hWnd { command args } $template
}

# Example:
#
# namespace eval MyWidget {
#     proc MyWidget { hWnd args } [
#
#         # Main frame for the mega-widget
#
#         frame $hWnd
#
#         # ... other widgets created/packed in the main frame
#
#         # Turn created frame into a mega-widget.
#
#         MegaWidget $hWnd
#         return $hWnd
#     }
#
#     proc dosomething { hWnd args } {
#         # ...
#     }
#
#     proc dosomethingelse { hWnd args } {
#         # ...
#     }
# }
#
# MyWidget::MyWidget .mw
# .mw dosomething -option value ...
# .mw dosomethingelse -option value ...
