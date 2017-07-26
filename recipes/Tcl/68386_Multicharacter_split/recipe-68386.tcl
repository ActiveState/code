# mcsplit --
#
#   Splits a string based using another string
#
# Arguments:
#   str       string to split into pieces
#   splitStr  substring
#   mc        magic character that must not exist in the orignal string.
#             Defaults to the NULL character.  Must be a single character.
# Results:
#   Returns a list of strings
#
proc mcsplit "str splitStr {mc {\x00}}" {
    return [split [string map [list $splitStr $mc] $str] $mc]
}
