##========================================================================
##  generic proc that ask for input to the user
##  accepts a list in ther format:
##  {
##      {"text to show 1" "default value 1"}
##      {"text to show 2" "default value 2"}
##      {"..." "..."}
##      {"text to show N" "default value N"}
##  }
##  return a list of each field value
##  {"returnValue1" "returnValue2" "..."}
##  or "_CANCEL" if the cancel button has been pressed
##========================================================================
proc inputBox {{entryTexts {{"Insert a value" ""}}}} {
    global _ok

    set _ok ""
    set t ".inputBox"
    if {[winfo exists $t]} {destroy $t}
    toplevel $t
    wm geometry . +250+116
    wm title . "InputBox"
    wm transient $t .
    wm protocol $t WM_DELETE_WINDOW "set _ok 0"
    set f1 [frame $t.f1]
    set f2 [frame $t.f2]
    pack $f1 -side top -expand 1 -fill both
    pack $f2 -side top -expand 1 -fill both

    set pos 0
    foreach entryText $entryTexts {
        set f [frame $f1.f$pos]
        label $f.l$pos -text [lindex $entryText 0]
        entry $f.e$pos
        $f.e$pos insert end [lindex $entryText 1]
        pack $f -side top -expand 1 -fill both
        pack $f.l$pos $f.e$pos -side left -expand 1 -fill both
        incr pos
    }

    button $f2.bOk -text "OK" -command "set _ok 1"
    button $f2.bCancel -text "Cancel" -command "set _ok 0"

    pack $f2.bOk $f2.bCancel -side left
    focus $f1.f0.e0

    #wait for button
    vwait _ok
    if {$_ok==0} {
        set tmp "_CANCEL"
    } else {
        set tmp [list]
        set pos 0
        foreach entryText $entryTexts {
            lappend tmp [$f1.f$pos.e$pos get]
            incr pos
        }
    }
    destroy $t
    unset _ok
    return $tmp
}

## usage example
set buttons {
    {"Insert a string 1" "a1"}
    {"Insert a string 2" "b2"}
    {"Insert a string 3" "c3"}
}

set returnValues [inputBox $buttons]
puts stderr "you have inserted \{$returnValues\}"
