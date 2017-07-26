#---------------------------------------------------------------------------
# 
# adp_compile --
#
# Parameters:
#     sourcetype -source|-filename
#     source 
# Returns:
#     Code to generate templated output
#
#---------------------------------------------------------------------------
proc adp_compile {sourcetype source} {

  # process parameters
  switch -exact -- $sourcetype {
    -source   { 
              set contents $source
              }

    -filename {
              
              set fileid [open $source r]
              set contents [read $fileid]
              close $fileid
              }
 
    default  { 
              return 
              }
  } 

  # really simple logic. 
  # 1. look for <%  %>
  # 2.   dump out contents preceeding <%
  # 3.   script contents preceeding %>
  # 4. repeat until run out of <% %> pairs
  # 5. dump contents after the last %> found.

  set outbuf {}

  set position 0
  set pstart [string first <% $contents $position]
  set pend   [string first %> $contents $pstart]

  while {[expr $pstart != -1 && $pend != -1 && $pstart < $pend]} {
     
      # Prevent script from adding unexpected blank lines to output:
      # if script is on a stand-alone line then 
      # don't add a newline to output
      set last_newline [string last \n $contents $pstart]
      zdebug "position=$position last_newline=$last_newline pstart=$pstart pend=$pend"
      if {[expr $last_newline != -1]} {
          set first_chars [string range $contents $last_newline [expr $pstart-1]]
          set last_char [string index $contents [expr $pend + 2]]      
          if {[string equal $last_char \n] && [string is space $first_chars]} {
              #
              # Replace <% %> tags with spaces
              #
              set contents [string replace $contents $pstart [expr $pstart + 1] {  }]
              set contents [string replace $contents $pend   [expr $pend   + 1] {  }]
              set pstart $last_newline+1
              incr pend
          }
      }

      # dump out contents preceeding <%
      adp_dump [string range $contents $position [expr $pstart-1]]

      # script out contents within the <% %>
      adp_script [string range $contents [expr $pstart+2] [expr $pend-1]]

      # if the next character is \n chomp it
      #if {[string equal [string index $contents [expr $pend + 2]] \n]} {
      #   incr pend 1 
      #}

      # search again
      set position [expr $pend + 2]
      set pstart [string first <% $contents $position]
      set pend   [string first %> $contents $pstart]
     
  }

  # dump out contents after %>
  adp_dump [string range $contents [expr $position] end]

  # insert pre and post conditions
  set precond "set __adp_output {}\n"
  set postcond ""
  set final ""
  append final $precond
  append final $outbuf
  append final $postcond
  return $final
}

#---------------------------------------------------------------------------
#
# adp_dump --
#
# Remarks:
#    generate code to output text to the output buffer
#
#---------------------------------------------------------------------------
proc adp_dump { text } {
  upvar outbuf outbuf

  # Protect double quotes, dollar signs, escapes
  regsub -all {[\]\[""\\$]} $text {\\&} quoted
  append outbuf "append __adp_output \"$quoted\""
}

#---------------------------------------------------------------------------
# 
# adp_eval --
#
# Parameters:
#     sourcetype -source|-filename
#     source 
#
# Returns:
#     Templated output
#
#---------------------------------------------------------------------------

proc adp_eval { sourcetype source } {

  set code [adp_compile $sourcetype $source]
  return [eval $code] 
}

#---------------------------------------------------------------------------
#
# adp_script --
#
# Remarks:
#   if <%= > tag, print the contents
#   else, dumps as tcl source
#
#---------------------------------------------------------------------------

proc adp_script { script } {

  # Protect double quotes, dollar signs, escapes
  # regsub -all {[\]\[""\\$]} $text {\\&} quoted

  upvar outbuf outbuf
  if {[string equal [string index $script 0] =]} {
     #
     # first character is equal sign:
     # handle the remainder as an expression
     #
     append outbuf "\n"
     set script [string range $script 1 end]
     append outbuf "append __adp_output $script"
     append outbuf "\n"
  } else {
     append outbuf "\n"
     append outbuf "  $script"
     append outbuf "\n"
  }
}

proc zdebug text { 
 #puts $text
}

#---------------------------------------------------------------------------
# 
#  test --
#
#  Remarks:
#     demonstration
#
#---------------------------------------------------------------------------

proc test {} {

  # If you have testhello.adp in current directory
  # set code [adp_compile -filename testhello.adp]
 
  set source [testprepare]
  set code [adp_compile -source $source]

  puts "--------------------------------------------"
  puts "The source"
  puts "--------------------------------------------"
  puts $source
  puts "--------------------------------------------"
  puts "The code generated"
  puts "--------------------------------------------"
  puts $code
  puts "--------------------------------------------"
  puts  "The result"
  puts "--------------------------------------------"
  eval $code
  puts $__adp_output
}

proc testprepare {} {

  return "
<html>
  <body>
    <h2>Hello World</h2>
       <% set name \"Peter\" %>
       Hello <%=\$name%> <br>
       Goodbye <%=\$name%>

       <% set mylist \[list Tom Dick Harry\]
          foreach name \$mylist {%>
          <p>Welcome <%=\$name%></p>
       <% }%>

       <a href=\"logoff\">log off</a>

  </body>
</html> "
}

# 1. Straight test --
#  test

# 2. Test for incorporation into subroutine
#  set source [testprepare]
#  set code [adp_compile -source $source]
#  return [eval $code]
