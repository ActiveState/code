## Returns data from file when there is something that can be read.
## Starts the event loop while waiting.

proc readWithEventLoop {file} {
    global ReadableStatus

    # See that index is unique and does not conflict with other eventReads
    set i 0
    while {[info exists ::ReadableStatus($file,$i)]} {
	incr i
    }
    
    set ReadableStatus($file,$i) 0
    set oldScript [fileevent $file readable]
    
    fileevent $file readable [list set ::ReadableStatus($file,$i) 1]
    
    vwait ::ReadableStatus($file,$i)
    unset ::ReadableStatus($file,$i)
    set r [read $file]

    # Make sure an old event handler is returned.
    fileevent $file readable $oldScript

    return $r
}
