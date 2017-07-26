# Convert to MB
proc toMB {n} {
    return [expr {$n / (1024*1024)}]
}
