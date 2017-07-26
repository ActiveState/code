#!/usr/bin/python

# gListLatLong.py - X.Jacobs (xiancobs@gmail.com) - 05/11/2012
# ------------------------------------------------------
# Get lat/long coordinates of an address list from Google Maps

import urllib, urllib2

address_list    = [    "106 S. Main Street, North East, MD",
                        "241 Market Street Charlestown MD 21914",
                        "64 South Main Street Port Deposit, Maryland 21904",
                        "1 E Main St Rising Sun, MD 21911",
                        "107 Chesapeake Blvd Elkton, MD 21921-6313, US",   
                        ]

def coordinate(address_list):
    if len(address_list) > 25:
        print "25 records maximum per request"
        raise

    url =   "http://maps.google.com/maps?f=d&hl=en&%s&ie=UTF8&0&om=0&output=html"\
            % ( "saddr=" + "%20to:".join(   [   urllib.quote(record)
                                                for record in address_list
                                                ]
                                            )
                )

    opener      = urllib2.build_opener()
    page        = opener.open(url).read()
    list_mark   = page.split(",latlng:{")[1:]
        
    list_coordinate = [ mark[0:mark.find('},image:')].replace("lat:","").replace("lng:","")
                        for mark in list_mark
                        ]
   
    return list_coordinate

print coordinate(address_list)
