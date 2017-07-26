### NOTE: this assumes list data does not contain the , (comma) char...
proc unique { list } {
    array set a [split "[join $list {,,}]," {,}]
    return [array names a]
}
