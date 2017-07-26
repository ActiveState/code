package require TclCurl

proc getUrl {curlHandle url} {

   puts                "\n ### getUrl using $url\n"

   set userAgent "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)" 

   puts                "\nuserAgent = $userAgent\n" 

   $curlHandle configure   -url               $url \
			   -bodyvar           body \
			   -headervar         headers \
			   -failonerror       1 \
			   -followlocation    1 \
			   -sslverifypeer     0  \
			   -useragent         $userAgent \
			   -errorbuffer       errorBuffer   

   if { [ catch {$curlHandle perform } r ] == 0} {

	set  httpCode      [$curlHandle getinfo httpcode]
	set  contentType   [$curlHandle getinfo contenttype]   
	set  redirectCount [$curlHandle getinfo redirectcount]
	set  fileTime      [$curlHandle getinfo filetime]      
	set  effUrl        [$curlHandle getinfo effectiveurl] 
	set  totalTime     [$curlHandle getinfo totaltime]     

	foreach { 1 2 } [ array get headers ] {
	    puts                [ format "%-20s = %-20s" $1 $2 ]
	    if { [ regexp -nocase "location" $1 ] == 1 }   { set url $2 }
	    if { [ regexp -nocase "Set-Cookie" $1 ] == 1 } { set cookie $2 }
	}

	puts                "\nLast effective URL = $url"

	puts                "\nCookie returned    = $cookie"
  
	return $cookie

      } else {
	  puts "ERROR1"
	  return -code error $errorBuffer
   }
}

proc postUrl {curlHandle url postString cookie} {

   puts                "\n postString is $postString"

   puts                "\n ### postUrl using $url\n"

   puts                "\n ### cookie  is    $cookie\n"

   set userAgent "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)" 

   puts "userAgent = $userAgent" 

   $curlHandle configure -url               $url \
          		 -cookie            $cookie \
          		 -bodyvar           body \
          		 -headervar         headers \
          		 -postfields        $postString \
          		 -useragent         $userAgent \
          		 -failonerror       1 \
          		 -errorbuffer       errorBuffer   

   if { [ catch {$curlHandle perform } r ] == 0} {

	set  httpCode      [$curlHandle getinfo httpcode]
	set  contentType   [$curlHandle getinfo contenttype]   
	set  redirectCount [$curlHandle getinfo redirectcount]
	set  fileTime      [$curlHandle getinfo filetime]      
	set  effUrl        [$curlHandle getinfo effectiveurl] 
	set  totalTime     [$curlHandle getinfo totaltime]     

	foreach { 1 2 } [ array get headers ] {
	    puts                [ format "%-20s = %-20s" $1 $2 ]
	    if { [ regexp -nocase "location" $1 ] == 1 }   { set url $2 }
	    if { [ regexp -nocase "Set-Cookie" $1 ] == 1 } { set cookie $2 }
	}

	puts                "\nLast effective URL = $url"

	puts                "\nCookie returned    = $cookie"
  
	return $cookie

      } else {
	  puts "ERROR1"
	  return -code error $errorBuffer
      }

}

proc getUrlCookie {curlHandle url cookie} {

   puts "\n ### getUrl using $url\n"
   puts "\n ### cookie  is    $cookie\n"

   set userAgent "Mozilla/4.0 (compatible; MSIE 5.5; Windows 98; Win 9x 4.90)" 

   puts "\nuserAgent = $userAgent\n" 

   $curlHandle configure   -url               $url \
			   -bodyvar           body \
			   -headervar         headers \
			   -failonerror       1 \
			   -followlocation    1 \
			   -sslverifypeer     0  \
          		   -cookie            $cookie \
			   -useragent         $userAgent \
			   -errorbuffer       errorBuffer   

   if { [ catch {$curlHandle perform } r ] == 0} {

	set  httpCode      [$curlHandle getinfo httpcode]
	set  contentType   [$curlHandle getinfo contenttype]   
	set  redirectCount [$curlHandle getinfo redirectcount]
	set  fileTime      [$curlHandle getinfo filetime]      
	set  effUrl        [$curlHandle getinfo effectiveurl] 
	set  totalTime     [$curlHandle getinfo totaltime]     

	foreach { 1 2 } [ array get headers ] {
	    puts                [ format "%-20s = %-20s" $1 $2 ]
	    if { [ regexp -nocase "location" $1 ] == 1 }   { set url $2 }
	    if { [ regexp -nocase "Set-Cookie" $1 ] == 1 } { set cookie $2 }
	}

	puts                "\nLast effective URL = $url"

	puts                "\nCookie returned    = $cookie"

  
	return $body

      } else {
	  set  httpCode      [$curlHandle getinfo httpcode]

	  puts "ERROR: $httpCode"

	  puts $errorBuffer
	  return -code error $errorBuffer
   }
}

######################################
# Set Variables
######################################

set curlHandle [curl::init]

#####################################################
# get initial url(login page) and return cookie.
# set url https://www.yoursite.com/yoursite/login.jsp
#####################################################

set url https://www.yoursite.com/yoursite/login.jsp

if {[catch {getUrl $curlHandle $url} r] == 0} {
     set cookie $r
     } else {
        puts "ERROR:"
        puts $r 
        $curlHandle cleanup
	exit 1
}

#######################################################################
#post userid and password with sessionid to login page 
#set url https://www.yoursite.com/yoursite/j_security_check 
#######################################################################

set url https://www.yoursite.com/yoursite/j_security_check 
set postString "j_username=abcde&j_password=12345&submit=logon" 

if {[catch {postUrl $curlHandle $url $postString $cookie} r] == 0} {
     set cookie $r
     } else {
        puts "ERROR:"
        puts $r 

        $curlHandle cleanup
	exit 1
}

#######################################################################
#get protected url(page)
#set url https://www.yoursite.com/yoursite/member/
#######################################################################

set url https://www.yoursite.com/yoursite/member/

if {[catch {getUrlCookie $curlHandle $url $cookie} r] == 0} {
     set body $r
     if {[regexp -nocase {\<title\>Members Area\<\/title\>} $body] ==1} {
	 set continue true 
     } else {
	    puts "ERROR:"
	    puts $r 

	    $curlHandle cleanup
	    exit 1
     }
} else {
	puts "ERROR:"
	puts $r 

	$curlHandle cleanup
	exit 1
}

$curlHandle cleanup
