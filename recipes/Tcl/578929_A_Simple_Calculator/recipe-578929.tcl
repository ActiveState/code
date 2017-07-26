set result 0
set express {0 +}
 
entry .result -justify right -textvariable result
grid .result -padx 2m -pady 2m -row 0 -column 0 -columnspan 4
for {set row 0} {$row < 4} {incr row} {
    for {set column 0} {$column < 4} {incr column} {
        set value [lindex {
            {7 8 9 /} {4 5 6 *} {1 2 3 -} {. 0 = +}
        } $row $column]
        set name ".btn[regsub {\.} $value dot]"
        button $name -text $value -command [list handle $value]
        grid $name -ipadx 1m -pady 1m -row [expr $row + 1] -column $column
    }
}
 
proc handle {value} {
    global result express
    switch -regexp $value {
        [0-9] {
            if {$result == 0} {
                set result $value
            } else {
                append result $value
            }
        }
        [-+*/] {
            lappend express $result $value
            set result 0
        }
        [.] {
            if {[string first . $result] < 0} {
                append result .
            }
        }
        = {
            lappend express $result
            set result [expr $express]
            set express {0 +}
        }
    }
}
