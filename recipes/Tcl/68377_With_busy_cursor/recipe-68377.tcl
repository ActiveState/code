# Usage: withBusyCursor { script ... }
#
proc withBusyCursor {body} {
    global errorInfo errorCode
    set busy {}
    set list {.}
    # Traverse the widget hierarchy to locate widgets with 
    # a nondefault -cursor setting.
    #
    while {$list != ""} {
        set next {}
        foreach w $list {
            catch {set cursor [$w cget -cursor]}
            if {[winfo toplevel $w] == $w || $cursor != ""} {
                lappend busy $w $cursor
                set cursor {}
            }
            set next [concat $next [winfo children $w]]
        }
        set list $next
    }

    # Change the cursor:
    #
    foreach {w _} $busy {
        catch {$w configure -cursor watch}
    }
    update idletasks

    # Execute the script body.
    #
    set rc [catch {uplevel 1 $body} result]
    set ei $errorInfo
    set ec $errorCode

    # Restore the original cursor settings.
    #
    foreach {w cursor} $busy {
        catch {$w configure -cursor $cursor}
    }

    # Return script result to caller.
    #
    return -code $rc -errorinfo $ei -errorcode $ec $result
}
