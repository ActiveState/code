#####################################################
# Proc - Get URL 
#####################################################
proc getUrl {url proxyHost proxyport userid password receiveFile } {

   package require TclCurl

   puts "\n get url $url\n"

   puts "proxyhost    = $proxyHost   " 
   puts "proxyport    = $proxyport   " 

   set curlHandle [ ::curl::init ]
   
   $curlHandle configure -url               $url \
         	         -userpwd           $userid:$password \
                         -verbose           1 \
         	         -proxy             $proxyHost \
         	         -proxyport         $proxyport \
         	         -proxytype         http \
			 -errorbuffer       errorBuffer \
			 -file              $receiveFile \
			 -failonerror       1 \
         	         -followlocation    1 

                         # -verbose           1 \

   if { [ catch { $curlHandle perform } r ] == 0 } {

           set continue true

       } else {

           $curlHandle cleanup 
           return -code error "$r $errorBuffer"

   }

   set totalTime    [ $curlHandle getinfo totaltime     ] 
   set connectTime  [ $curlHandle getinfo connecttime   ] 
   set sizeDownload [ $curlHandle getinfo sizedownload  ] 
   set speedDownoad [ $curlHandle getinfo speeddownload ] 

   puts " totalTime    = $totalTime    "
   puts " connectTime  = $connectTime  "
   puts " sizeDownload = $sizeDownload "
   puts " speedDownoad = $speedDownoad "

   set details [ list $totalTime $connectTime $sizeDownload $speedDownoad ]

   $curlHandle cleanup 
 
   return [ list $r $details ]

}
