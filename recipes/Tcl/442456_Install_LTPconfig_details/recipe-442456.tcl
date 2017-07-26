# 
# Install LTPA Security.
#
####################################################################
# Patrick Finnegan 23/09/2004.  V1. 
####################################################################

#-------------------------------------------------------------------------------
# Install LTPA settings. 
#-------------------------------------------------------------------------------

proc getLTPAId {} {

   global AdminConfig 

   puts "\n## List LTPA Details ##\n" 

   if { [ catch { $AdminConfig list LTPA } r ] == 0 } {

       set ltpaId $r

       foreach e $r {

          puts [ format "\n%-10s %-50s\n"  "LTPA:" $e  ]
	 
          catch { $AdminConfig showAttribute $e OID } r
	  puts [ format "%-5s %-20s %-50s"  " " OID $r ]
          catch { $AdminConfig showAttribute $e authConfig  } r
	  puts [ format "%-5s %-20s %-50s"  " " authConfig $r ]
          catch { $AdminConfig showAttribute $e authContextImplClass    } r
	  puts [ format "%-5s %-20s %-50s"  " " authContextImplClass $r ]
          catch { $AdminConfig showAttribute $e authValidationConfig } r
	  puts [ format "%-5s %-20s %-50s"  " " authValidationConfig $r ]
          catch { $AdminConfig showAttribute $e isCredentialForwardable  } r
	  puts [ format "%-5s %-20s %-50s"  " " isCredentialForwardable $r ]
          catch { $AdminConfig showAttribute $e password } r
	  puts [ format "%-5s %-20s %-50s"  " " password $r ]
          catch { $AdminConfig showAttribute $e private } r
	  puts [ format "%-5s %-20s %-50s"  " " private $r ]
          catch { $AdminConfig showAttribute $e properties       } r
	  puts [ format "%-5s %-20s %-50s"  " " properties $r ]
          catch { $AdminConfig showAttribute $e public } r
	  puts [ format "%-5s %-20s %-50s"  " " public $r ]
          catch { $AdminConfig showAttribute $e shared } r
	  puts [ format "%-5s %-20s %-50s"  " " shared $r  ]
          catch { $AdminConfig showAttribute $e simpleAuthConfig } r
	  puts [ format "%-5s %-20s %-50s"  " " simpleAuthConfig $r ]
          catch { $AdminConfig showAttribute $e singleSignon    } r
	  puts [ format "%-5s %-20s %-50s"  " " singleSignon $r ]
          
	  # display SSO properties

          foreach { a b } [ $AdminConfig showall $r ] {

	     puts [ format "%-10s %-20s %-15s"  " " [ lindex $a 0 ] [ lindex $a 1 ] ]
	     puts [ format "%-10s %-20s %-15s"  " " [ lindex $b 0 ] [ lindex $b 1 ] ]
          }
	  
          catch { $AdminConfig showAttribute $e timeout } r
	  puts [ format "%-5s %-20s %-50s"  " " timeout $r ]
          catch { $AdminConfig showAttribute $e trustAssociation   } r
	  puts [ format "%-5s %-20s %-50s"  " " trustAssociation $r ]

       }	      

    } else {
 
        puts "\nproblem accessing LDAP user registry ID.\n"
        puts $r 
        puts "************************************\n"
        return -code error $r

    }

    return $ltpaId 
}

#-------------------------------------------------------------------------------
# generate ltpa keys. 
#-------------------------------------------------------------------------------

proc generateLtpaKeys { ltpaPassword } {

   global AdminConfig AdminControl

   puts "\n## generate ltpa keys"

   if { [ catch { $AdminControl queryNames WebSphere:type=SecurityAdmin,* } sb ] == 0 } {

      if { [ catch { $AdminControl invoke $sb generateKeys $ltpaPassword } r ] == 0 } {

          return $r

          } else {

          puts "\nproblem generating LTPA keys.\n"
          puts $r 
          puts "************************************\n"
          return -code error $r

      } else {

      puts "\nproblem getting security bean.\n"
      puts $r 
      puts "************************************\n"
      return -code error $r

      }

   }

}

#-------------------------------------------------------------------------------
# set LTPA properties. 
#-------------------------------------------------------------------------------

proc ltpaProperties { domainName password timeout ltpaId } { 

   global AdminConfig AdminControl

   puts "\n## set Ltpda properties"

   set password        [ list password $password ]
   set timeout         [ list timeout  $timeout  ]

   puts "\n## set SSO properties"

   set domain          [ list domainName  $domainName   ]
   set requiresSSL     [ list requiresSSL false         ]
   set enabled         [ list enabled     true          ]

   set propertiesList  [ list $domain $requiresSSL $enabled ]
   set singleSignon    [ list singleSignon $propertiesList  ]

   set attrs           [ list $password $timeout $singleSignon ]

   if { [ catch { $AdminConfig modify $ltpaId $attrs } r ] == 0 } {

      return $r

      } else {

      puts "\nproblem setting ltpa attributes.\n"
      puts $r 
      puts "************************************\n"
      return -code error $r

   }
}

####################################################################
# Main Control.
####################################################################

puts "\n argc = $argc \n"

if {$argc < 2} {
        return -code error "error - no arguments supplied.  Supply domainName and ltpa password"
}

set domainName   [ lindex $argv 0 ]
set ltpaPassword [ lindex $argv 1 ]
set timeout      [ lindex $argv 2 ]

puts "domainName   =  $domainName     "
puts "ltpaPassword =  $ltpaPassword   "

#######################################################################
# List servers and check if target server already exists.
# If so delete it and recreate.
#######################################################################

if { [ catch { getLTPAId } r ] == 0 } {

#    puts "\n $r \n"

    set ltpaId $r 

} else {
        return -code error $r 
}

if { [ catch { ltpaProperties $domainName $ltpaPassword $timeout $ltpaId  } r ] == 0 } {
    
    puts "\n## Admin Config Save ##\n"
    catch { $AdminConfig save } r
    puts $r

} else {
        return -code error $r 
}

####################################################################
# List ltpa details to verify install.
####################################################################

if { [ catch { getLTPAId } r ] == 0 } {

#    puts "\n $r \n"

    set ltpaId $r 

} else {
        return -code error $r 
}
