# commify --
#   puts commas into a decimal number
# Arguments:
#   num		number in acceptable decimal format
#   sep		separator char (defaults to English format ",")
# Returns:
#   number with commas in the appropriate place
#

proc commify {num {sep ,}} {
    while {[regsub {^([-+]?\d+)(\d\d\d)} $num "\\1$sep\\2" num]} {}
    return $num
}
