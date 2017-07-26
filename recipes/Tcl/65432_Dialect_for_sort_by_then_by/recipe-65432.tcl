set list {{12 11} {12 13} {12 12} {11 14} {13 12}}

    puts [lsort -index 1 $list]
    puts [lsort -index 0 [lsort -index 1 $list]]

{12 11} {12 12} {13 12} {12 13} {11 14}
{11 14} {12 11} {12 12} {12 13} {13 12}
