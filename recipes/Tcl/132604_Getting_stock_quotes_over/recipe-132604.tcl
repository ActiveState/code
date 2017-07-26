#!/bin/sh
 #
 # Portfolio tracking by Vince Darley
 #
 # This file may be freely modified, sold, changed, etc.  If you do make
 # useful changes, I would like a copy, although you aren't obligated to
 # send me anything.
 #
 # Ideas for future improvements: auto-update every N minutes, graphs of
 # total portfolio value over time, ability to record changes in portfolio
 # over time...
 #
 #\
 exec wish "$0"

 package require http

 namespace eval portfolio {}

 set shares(AAPL) 550
 set shares(ORCL) 100
 set shares(INKT) 100
 set cash 3285.74

 ##
  # -------------------------------------------------------------------------
  #
  # "portfolio::getInformation" --
  #
  #  Takes a list of symbols, from Nasdaq, NYSE or even mutual funds etc,
  #  and returns a list of results, one for each symbol given.  Each returned
  #  result is a string containing comma separated values, in the order
  #
  #  symbol, price, date, ...
  #
  #  We use a quote server from yahoo.
  # -------------------------------------------------------------------------
  ##
 proc portfolio::getInformation {symbols} {
     set query "http://quote.yahoo.com"
     append query "/d/quotes.csv?s=[join $symbols +]&f=sl1d1t1c1ohgv&e=.csv"
     set token [http::geturl $query]

     set actual {}
     foreach res [split [string trim [http::data $token]] "\r\n"] {
	 if {$res != ""} {
	     set res [split $res ,]
	     lappend actual [lreplace $res 0 0 [string trim [lindex $res 0] {{}""}]]
	 }
     }
     return $actual
 }

 proc portfolio::dumpData {data} {
     foreach result $data {
	 set items [split $result ","]
	 puts stdout $items
     }
 }

 proc portfolio::createWindow {portfolio} {
     foreach {s q} $portfolio {
	 set w [symbolToWin $s]
	 label ${w}symb -text $s
	 label ${w}price -text ""
	 label ${w}change -text ""
	 label ${w}quantity -text $q
	 label ${w}value -text ""
	 grid ${w}symb ${w}price ${w}change ${w}quantity ${w}value
     }
     button .update -text "Update" -command portfolio::updateAll
     label .total -text ""
     grid .update .total
     wm title . "Portfolio"
     wm withdraw .
     portfolio::updateAll
     wm deiconify .
 }

 proc portfolio::symbolToWin {symbol} {
     return ".[join [string tolower $symbol]]"
 }

 proc portfolio::updateWindow {data} {
     global cash
     if {[info exists cash]} {
	 set total $cash
     } else {
	 set total 0.0
     }
     foreach items $data {
	 set w [symbolToWin [lindex $items 0]]
	 set price [lindex $items 1]
	 set change [lindex $items 4]
	 ${w}price configure -text $price
	 ${w}change configure -text $change
	 set val [expr {[${w}quantity cget -text] * $price}]
	 ${w}value configure -text $val
	 set total [expr {$total + $val}]
     }
     .total configure -text $total
 }

 proc portfolio::updateAll {} {
     global shares
     updateWindow [getInformation [array names shares]]
 }

 portfolio::createWindow [array get shares]
