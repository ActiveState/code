package require mime 1.0
package require smtp 1.0

# create an image
set imageT [mime::initialize -canonical image/gif -file logo.gif]

# parse a message
set messageT [mime::initialize -file example.msg]

# recursively traverse a message looking for primary recipients

proc traverse {token} {
    set result ""

    # depth-first search
    if {![catch { mime::getproperty $token parts } parts]} {
	foreach part $parts {
	    set result [concat $result [traverse $part]]
	}
    }

    # one value for each line occuring in the header
    foreach value [mime::getheader $token To] {
	foreach addr [mime::parseaddress $value] {
	    catch { unset aprops }
	    array set aprops $addr
	    lappend result $aprops(address)
	}
    }

    return $result
}

# create a multipart containing both, and a timestamp
set multiT [mime::initialize \
                -canonical multipart/mixed \
                -parts [list $imageT $messageT]]

# send it to some friends
smtp::sendmessage $multiT \
	-header [list From "Marshall Rose <mrose@dbc.mtview.ca.us>"] \
	-header [list To "Andreas Kupries <a.kupries@westend.com>"] \
	-header [list cc "dnew@messagemedia.com (Darren New)"] \
	-header [list Subject "test message..."]

# clean everything up
mime::finalize $multiT -subordinates all
