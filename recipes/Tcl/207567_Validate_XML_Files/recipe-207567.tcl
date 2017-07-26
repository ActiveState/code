# 
# Check xml files in target directory tree 
#
package require fileutil
package require tnc
package require tdom

######################################
# Proc for Parser
######################################
proc externalEntityRefHandler {base systemId publicId} {
    
    if {![regexp {^[a-zA-Z]+:/} $systemId]}  {
        regsub {^[a-zA-Z]+:} $base {} base
        set basedir [file dirname $base]
        set systemId "[set basedir]/[set systemId]"
    } else {
        regsub {^[a-zA-Z]+:} $systemId systemId
    }
    if {[catch {set fd [open $systemId]}]} {
        return -code error \
                -errorinfo "Failed to open external entity $systemId"
    }
    return [list channel $systemId $fd]
}
######################################
# Proc - checkxml 
######################################
proc checkXml {xmlfile} {

 set parser [expat -externalentitycommand externalEntityRefHandler \
                   -baseurl $xmlfile \
                   -paramentityparsing notstandalone]

 catch {$parser parsefile $xmlfile} result_var
 
 return $result_var

 $parser reset
 $parser free
}
######################################################
# Proc - check xmlfile syntax
######################################################
proc checkXmlFiles {xmlDir} {
   
    puts "\n Base dir is $xmlDir\n"

    set xmlFiles [::fileutil::find $xmlDir {string match *.xml*}] 
    
    foreach match $xmlFiles {
	set r [checkXml $match]
	if {$r == ""} {
	    continue
	} else {
	    puts $match
	    puts $r
	}
    }
}

checkXmlFiles d:\\xmlDirectory1
checkXmlFiles d:\\xmlDirectory2
