proc ParseString { variable_name string separators maximum } {
  # this routine makes parsing easy WHILE preserving
  # the "exactness" of the string by NOT treating it as a list...
  #
  # get ahold of an array to put results into
  upvar "1" $variable_name local_array

  # get a list of separators...
  set separator_list [split $separators ""]

  # get length in characters
  set count [string length $string]

  # start at first index (maybe make this variable later?)
  set index "0"

  # always start counting in result array from 1 
  # (should this really be zero?)
  set found_index "1"

  # how many "matches" did we find?
  #
  # NOTE: this will NOT be more than the parameter 
  #       maximum, if specified
  #
  set found_count "0"

  # current string that needs to be added when next 
  # separator is found...
  set found_string ""

  #
  # keep going until the end of the string is reached
  #
  while {$index < $count} {
    #
    # go through string on a character-by-character basis
    #
    set character [string index $string $index]
    #
    # if the character is in the separator list,
    # then we need to add to the array...
    #
    if {[lsearch -exact $separator_list $character] != "-1"} then {
      if {$maximum > "0"} then {
        #
        # we are limiting the number of "matches" to a certain amount
        # to allow for rather flexible argument parsing for callers...
        # (they can treat the first X arguments as separate, and the 
        # rest as one long argument)
        #
        if {$found_count == [expr {$maximum - "1"}]} then {
          # stop adding new after X matches... (last one is taken care 
          # of after loop)
          set do_add "0"
        } else {
          # we haven't reached the maximum yet
          set do_add "1"
        }
      } else {
        # there is no maximum
        set do_add "1"
      }
    } else {
      # we didn't find a separator yet
      set do_add "0"
    }

    if {$do_add != "0"} then {
      #
      # add string to found array...
      #
      set local_array($found_index) $found_string
      # next index in result array
      incr found_index
      # increase count of found arguments
      incr found_count
      # reset current string
      set found_string ""
    } else {
      #
      # otherwise, just keep appending to current string
      #
      if {$found_string != ""} then {
        # tack on the current character (this is not a separator)
        append found_string $character
      } else {
        # since no other characters in the current string yet, 
        # just set it
        set found_string $character
      }
    }

    incr index
  }

  #
  # don't forget last one... in case there is one...
  # (this should always happen if the string doesn't end in space...)
  #
  if {$found_string != ""} then {
    # add FINAL string to found array...
    set local_array($found_index) $found_string
    # next index in result array
    incr found_index
    # increase count to FINAL count of found arguments
    incr found_count
    # reset current string
    set found_string ""
  }

  #
  # pass back count always, even if no matches...
  #
  set local_array(count) $found_count

  #
  # NOTE: This should only return zero if there were 
  #       no characters in the string (because otherwise 
  #       we always found at least one element).
  #
  if {$found_count > "0"} then {
    # if we found anything, return non-zero
    set result "1"
  } else {
    # otherwise return zero
    set result "0"
  }

  return $result
}
