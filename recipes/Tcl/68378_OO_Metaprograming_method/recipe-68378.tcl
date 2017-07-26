# Based on code at http://mini.net/cgi-bin/wikit/401.html

package require XOTcl  ;# http://www.xotcl.org/


# We dynamically install this method for the "Class" meta-class. This
# means all classes will be provided with this method. One could
# also create a separate meta-class to do this and create classes from it
# instead.

@ Class instproc instFromTemplate {
    procName {Name of instproc to create.}
    object {Object containing template proc}
    template {Name of proc to use as template.}
    subList {
        Key-value substitution list where the key is a regexp and the value
        is a subSpec as in [regsub].
    }
} {
    description {
        Creates an instproc from a template proc by copying the template and
        replacing specified data. Extremely useful for meta-programming. 
    }
}

Class instproc instFromTemplate {procName object template subList} {
    set body [$object info body $template]
    foreach {regexp subSpec} $subList {
        regsub -all -- $regexp $body $subSpec body
    }
    [self] instproc $procName [$object info args $template] $body
}
