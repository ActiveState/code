#!/bin/sh
# the next line restarts using tclsh \
exec tclsh "$0" ${1+"$@"}

package require Tcl 8.6.0

array set categories [list \
  highCard 0 \
  onePair 1 \
  twoPair 2 \
  threeOfAKind 3 \
  straight 4 \
  flush 5 \
  fullHouse 6 \
  fourOfAKind 7 \
  straightFlush 8 \
]
array set groupings [list \
  {1 1 1 1 1} $categories(highCard) \
  {2 1 1 1} $categories(onePair) \
  {2 2 1} $categories(twoPair) \
  {3 1 1} $categories(threeOfAKind) \
  {3 2} $categories(fullHouse) \
  {4 1} $categories(fourOfAKind) \
]
set nValues 13

oo::class create card {
  constructor {withSuit withValue} {
    my variable suit value
    set suit $withSuit
    set value $withValue
  }
  method suit {} {
    my variable suit
    return $suit
  }
  method value {} {
    my variable value
    return $value
  }
  destructor {
    my variable suit value
    $suit destroy
    $value destroy
  }
}

oo::class create category {
  constructor {withNr} {
    my variable nr
    set nr $withNr
  }
  method cmp {other} {
    my variable nr
    return [numCmp $nr [$other nr]]
  }
  method nr {} {
    my variable nr
    return $nr
  }
}

oo::class create hand {
  constructor {withCards} {
    global categories groupings
    my variable cards category kickers
    set cards $withCards
    set sortedValues [lsort -command {apply {{a b} {$a cmp $b}}} [lmap card $cards {$card value}]]
    set typeOfStraight [my TypeOfStraight $sortedValues]
    set isFlush [my IsFlush]
    if {$typeOfStraight} {
      set category [category new [expr {$isFlush ? $categories(straightFlush) : $categories(straight)}]]
      set kickers [list [lindex $sortedValues [expr {$typeOfStraight == 1 ? "end" : "end-1"}]]]
      return
    }
    if {$isFlush} {
      set category [category new $categories(flush)]
      set kickers [lreverse $sortedValues]
      return
    }
    set nEquals {}
    set kickers {}
    while {[llength $sortedValues]} {
      lassign [longestSeq $sortedValues {apply {{a b} {$a cmp $b}}} 1] i n
      lappend nEquals $n
      lappend kickers [lindex $sortedValues $i]
      set sortedValues [lreplace $sortedValues $i [expr {$i + $n - 1}]]
    }
    set category [category new $groupings($nEquals)]
  }
  method category {} {
    my variable category
    return $category
  }
  method cmp {other} {
    my variable category kickers
    if {[set cmpRes [$category cmp [$other category]]] != 0} {
      return $cmpRes
    }
    foreach kicker $kickers otherKicker [$other kickers] {
      if {[set cmpRes [$kicker cmp $otherKicker]] != 0} {
        return $cmpRes
      }
    }
    return 0
  }
  method kickers {} {
    my variable kickers
    return $kickers
  }
  method IsFlush {} {
    my variable cards
    set firstSuit [[lindex $cards 0] suit]
    foreach card $cards {
      if {[[$card suit] cmp $firstSuit] != 0} {
        return 0
      }
    }
    return 1
  }
  method TypeOfStraight {sortedValues} {
    set sVLen [llength $sortedValues]
    set prevValue [lindex $sortedValues 0]
    for {set i 1} {$i < $sVLen} {incr i} {
      set value [lindex $sortedValues $i]
      if {![$value isSeqTo $prevValue]} {
        return [expr {$i == $sVLen - 1 && [[lindex $sortedValues 0] isLowest] && [[lindex $sortedValues end] isHighest] ? 2 : 0}]
      }
      set prevValue $value
    }
    return 1
  }
  destructor {
    my variable cards category
    foreach card $cards {
      $card destroy
    }
    $category destroy
  }
}

oo::class create suit {
  constructor {withNr} {
    my variable nr
    set nr $withNr
  }
  method cmp {other} {
    my variable nr
    return [numCmp $nr [$other nr]]
  }
  method nr {} {
    my variable nr
    return $nr
  }
}

oo::class create value {
  constructor {withNr} {
    my variable nr
    set nr $withNr
  }
  method cmp {other} {
    my variable nr
    return [numCmp $nr [$other nr]]
  }
  method isHighest {} {
    global nValues
    my variable nr
    return [expr {$nr == $nValues - 1}]
  }
  method isLowest {} {
    my variable nr
    return [expr {$nr == 0}]
  }
  method isSeqTo {other} {
    my variable nr
    return [expr {$nr == [$other nr] + 1}]
  }
  method nr {} {
    my variable nr
    return $nr
  }
}

proc longestSeq {list cmpCmd firstOrLast} {
  set bestI 0
  set bestN 0
  set i 0
  set listLen [llength $list]
  while {$i < $listLen} {
    set n [seqLen $list $i $cmpCmd]
    if {($firstOrLast == 0 && $n > $bestN) || ($firstOrLast == 1 && $n >= $bestN)} {
      set bestI $i
      set bestN $n
    }
    incr i $n
  }
  return [list $bestI $bestN]
}

proc numCmp {a b} {
  return [expr {$a < $b ? -1 : ($a == $b ? 0 : 1)}]
}

proc seqLen {list index cmpCmd} {
  set i $index
  set listLen [llength $list]
  while {$i < $listLen && [{*}$cmpCmd [lindex $list $i] [lindex $list $index]] == 0} {
    incr i
  }
  return [expr {$i - $index}]
}

# ================ Project Euler Problem 54 ================

array set suitStrings {C 0 D 1 H 2 S 3}
array set valueStrings {T 8 J 9 Q 10 K 11 A 12}

proc str2Card {str} {
  lassign [split $str ""] valueStr suitStr
  return [card new [str2Suit $suitStr] [str2Value $valueStr]]
}

proc str2Hands {str} {
  set cards [lmap cardStr [split $str] {str2Card $cardStr}]
  set hands {}
  set i 0
  set cardsLen [llength $cards]
  while {$i < $cardsLen} {
    lappend hands [hand new [lrange $cards $i [expr {$i + 5 - 1}]]]
    incr i 5
  }
  return $hands
}

proc str2Suit {str} {
  global suitStrings
  return [suit new $suitStrings($str)]
}

proc str2Value {str} {
  global valueStrings
  if {[info exists valueStrings($str)]} {
    set n $valueStrings($str)
  } else {
    set n [expr {$str - 2}]
  }
  return [value new $n]
}

set count 0
while {[gets stdin line] >= 0} {
  lassign [str2Hands $line] hand1 hand2
  if {[$hand1 cmp $hand2] > 0} {
    incr count
  }
  $hand1 destroy
  $hand2 destroy
}
puts $count
