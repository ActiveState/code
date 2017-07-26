 # -*- tcl -*-
 # Lexing C

 package provide clex 1.0
 namespace eval  clex {}

 # Most tokens can be recognized and separated from the others via
 # [string map].  The remainder are identifiers.  Except for strings,
 # and comments. These may contain any other token, and we may not act
 # upon them. And both may contain sequences reminiscent of the
 # other. Because of that a first step is to identify and parse out
 # comments and strings, where 'parsing out' means that these tokens
 # are replaced with special char sequences which refer the lexer to a
 # small database. In the final output they are placed back.

 proc clex::SCextract {code mapvar} {
     # Extract strings and comments from the code and place them in mapvar.
     # Replace them with ids

     upvar $mapvar map

     set tmp   ""
     set count 0

     while {1} {
 	set comment [string first "/*" $code]
 	set string  [string first "\"" $code]

 	if {($comment < 0) && ($string < 0)} {
 	    # No comments nor strings to extract anymore.
 	    break
 	}

 	# Debug out
 	#puts "$string | $comment | [string length $code]"

	if {
	    (($string >= 0) && ($comment >= 0) && ($string < $comment)) ||
	    (($string >= 0) && ($comment < 0))
	} {
	    # The next vari-sized thing is a "-quoted string.
	    # Finding its end is bit more difficult, because we have
	    # to accept \" as one character inside of the string.

	    set from $string
	    while 1 {
		incr from
		set stop  [string first "\""   $code $from]
		set stopb [string first "\\\"" $code $from]
		incr stopb
		if {$stop == $stopb} {set from $stopb ; incr from ; continue}
		break
	    }

	    set id \000@$count\000
	    incr count
	    lappend map $id [set sub [string range $code $string $stop]]

	    incr stop ; incr string -1
	    append tmp [string range $code 0 $string] $id
	    set  code  [string range $code $stop end]

	    # Debug out
	    #puts "\tSTR $id <$sub>"
	    continue
	}

	if {
	    (($string >= 0) && ($comment >= 0) && ($comment < $string)) ||
	    (($comment >= 0) && ($string < 0))
	} {
	    # The next vari-sized thing is a comment.
	    # We ignore comments.

	    set  stop [string first "*/" $code $comment]
	    incr stop 2
	    incr comment -1
	    append tmp [string range $code 0 $comment]
	    set  code  [string range $code $stop  end]
	    continue
	}
	return -code error "Panic, string and comment at some location"
    }
    append  tmp $code
    return $tmp
 }

 proc clex::DefStart {} {
    variable tokens [list]
    #puts "== <$tokens>"
    return
 }

 proc clex::Key {string {replacement {}}} {
    variable tokens
    if {$replacement == {}} {
	set replacement \000\001[string toupper $string]\000
    } else {
	set replacement \000\001$replacement\000
    }
    lappend tokens $string $replacement
    #puts "== <$tokens>"
    return
 }

 proc clex::DefEnd {} {
    variable       tokens
    array set tmp $tokens
    set res [list]
    foreach key [lsort -decreasing [array names tmp]] {
	lappend res $key $tmp($key)
    }
    set tokens $res
    #puts "== <$tokens>"
    return
 }

 proc clex::lex {code} {
    variable tokens

    # Phase I ... Extract strings and comments so that they don't interfere
    #             with the remaining phases.

    # Phase II ... Separate all constant-sized tokens (keywords and
    #              punctuation) from each other.

    # Phase III ... Separate whitespace from the useful text.
    #               Actually converts whitespace into separator characters.

    # Phase IV ... Reinsert extracted tokens and cleanup multi-separator sequences

    set scmap [list]
    if 0 {
	# Minimal number of commands for all phases

	regsub -all -- "\[\t\n \]+" [string map $tokens \
		[SCextract $code scmap]] \
		\000 tmp

	set code [split \
		[string trim \
		[string map "\000\000\000 \000 \000\000 \000" \
		[string map $scmap \
		$tmp]] \000] \000]
    }
    if 1 {
	# Each phase spelled out explicitly ...

	set code [SCextract          $code scmap]    ; # I
	set code [string map $tokens $code]          ; # II
	regsub -all -- "\[\t\n \]+"  $code \000 code ; # III
	set code [string map $scmap  $code]          ; # IV/a
	set code [string map "\000\000\000 \000 \000\000 \000" $code]  ; # IV/b
	set code [string trim $code \000]
	set code [split $code \000]
    }

    # Run through the list and create something useable by the parser.
    #
    # A list of pairs (pairs being lists of 2 elements), where each
    # pair contains the symbol to give to the parser, and associated
    # data, if any.

    set tmp [list]
    foreach lex $code {
	switch -glob -- [string index $lex 0] {
	    \001 {
		# Keyword, no data.
		lappend tmp [list [string range $lex 1 end] {}]
	    }
	    ' - [0-9] {
		# Character or numeric constant.
		lappend tmp [list CONSTANT $lex]
	    }
	    \" {
		# String literal. Strip the double-quotes.
		lappend tmp [list STRING_LITERAL [string range $lex 1 end-1]]
	    }
	    default {
		# Identifier. This code does not distinguish
		# identifiers and type-names yet. This is defered to
		# the 'scanner', i.e. the glue code feeding the lexer
		# symbols into the parser.

		lappend tmp [list IDENTIFIER $lex]
	    }
	}
    }
    set code $tmp

    return $code
 }

 namespace eval clex {
    DefStart

    Key (   LPAREN      ; Key )  RPAREN    ; Key ->  DEREF
    Key <   LT          ; Key <= LE        ; Key ==  EQ
    Key >   GT          ; Key >= GE        ; Key !=  NE
    Key \[  LBRACKET    ; Key \] RBRACKET  ; Key =   ASSIGN
    Key \{  LBRACE      ; Key \} RBRACE    ; Key *=  MUL_ASSIGN
    Key .   DOT         ; Key ,  COMMA     ; Key /=  DIV_ASSIGN
    Key ++  INCR_OP     ; Key -- DECR_OP   ; Key %=  REM_ASSIGN
    Key &   ADDR_BITAND ; Key *  MULT_STAR ; Key +=  PLUS_ASSIGN
    Key +   PLUS        ; Key -  MINUS     ; Key -=  MINUS_ASSIGN
    Key ~   BITNOT      ; Key !  LOGNOT    ; Key <<= LSHIFT_ASSIGN
    Key /   DIV         ; Key %  REM       ; Key >>= RSHIFT_ASSIGN
    Key <<  LSHIFT      ; Key >> RSHIFT    ; Key &=  BITAND_ASSIGN
    Key ^   BITEOR      ; Key && LOGAND    ; Key ^=  BITEOR_ASSIGN
    Key |   BITOR       ; Key || LOGOR     ; Key |=  BITOR_ASSIGN
    Key ?   QUERY       ; Key :  COLON     ; Key \;  SEMICOLON
    Key ... ELLIPSIS

    Key typedef ; Key extern   ; Key static ; Key auto ; Key register
    Key void    ; Key char     ; Key short  ; Key int  ; Key long
    Key float   ; Key double   ; Key signed ; Key unsigned
    Key goto    ; Key continue ; Key break  ; Key return
    Key case    ; Key default  ; Key switch
    Key struct  ; Key union    ; Key enum
    Key while   ; Key do       ; Key for
    Key const   ; Key volatile
    Key if      ; Key else
    Key sizeof

    DefEnd
 }
