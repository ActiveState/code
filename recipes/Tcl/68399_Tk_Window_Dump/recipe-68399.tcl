proc dumpWidget {window filename args} {
    # What is the X id of the window to dump?
    set id [winfo id $window]

    # We'll use xwd to do the actual dump...
    set cmd [list exec xwd -quiet -id $id]

    # ...and ImageMagick to convert to whatever...
    lappend cmd | convert

    # ...but we need to be a little careful when inserting the
    # arguments and handling the filenames since they are
    # not guaranteed to be well-behaved words...
    eval $cmd $args [list - $filename]
}
