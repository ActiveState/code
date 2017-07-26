#!/usr/bin/python
#
# Author:    Kevin T. Ryan, kevryan0701@yahoo.com
# Date:      03/29/2005
#
# dist computes the distance between two points on the earth, as identified by their
# longitude and latitude identifications in MILES.  If you would like to change the 
# distance (to, perhaps, calculate the distance in km) you should change the last line
# of the function.  For example, for km, use 6399 instead of 3956 (the approximate
# distance of the earth).
#
# Obtained distance formula from "http://www.census.gov/cgi-bin/geo/gisfaq?Q5.1" and 
# more information is available at "http://en.wikipedia.org/wiki/Great_circle_distance".
#
# Zip code data obtained from 'http://www.census.gov/tiger/tms/gazetteer/zips.txt'
#
# Changes:
#   04/09/2006: Added a class (Zip_Codes) to cache the zip data in memory for fast lookups and
#               a convenience class _Zip_Code_Record that gives us named access to zipcode
#               properties (e.g., longitude).  Can also instantiate a Zip_Codes object and then
#               have access to the zips like zipcode_obj['08083'].city (== SOMERDALE) which gives
#               fast access to attributes and distance calculations

import math

class _Zip_Code_Record:

    def __init__(self, zip, state, city, longitude, latitude, perform_transformation=True):
        self.zip       = zip
        self.state     = state
        self.city      = city
        if perform_transformation:
            self.longitude = math.radians(float(longitude))
            self.latitude  = math.radians(float(latitude))
        else:
            self.longitude = longitude
            self.latitude  = latitude

class Zip_Codes:

    def __init__(self, zip_file="zips.txt"):
        '''Load the zip dB into memory and initialize our object.'''
        self.zips = {}

        lines = [line.rstrip().replace('"', '') for line in open(zip_file)] # Do some cleanup on the lines before setting up our "db"
        for line in lines:
            # Default layout is:
            # The 1990 Zip Code by State file is comma separated values, ASCII text, one 
            # record per line. The field/record layout is as follows: 

                # Field 1 - State Fips Code 
                # Field 2 - 5-digit Zipcode 
                # Field 3 - State Abbreviation 
                # Field 4 - Zipcode Name 
                # Field 5 - Longitude in Decimal Degrees (West is assumed, no minus sign) 
                # Field 6 - Latitude in Decimal Degrees (North is assumed, no plus sign) 
                # Field 7 - 1990 Population (100%) 
                # Field 8 - Allocation Factor (decimal portion of state within zipcode) 

            # (see http://www.census.gov/tiger/tms/gazetteer/zip90r.txt)

            zip, city, state, lon, lat = line.split(",")[1:-2]
            self.zips[zip] = _Zip_Code_Record(zip, city, state, lon, lat)

    def get_distance(self, zip1, zip2):
        '''Returns the distance between two points on the earth.
        
        Inputs used are:
            Longitude (in radians) of the first location,
            Latitude (in radians) of the first location,
            Longitude (in radians) of the second location, and
            Latitude (in radians) of the second location.
        To convert to radians (from degrees), use pythons math.radian function (Note: already done 
        for you in the constructor above).  Returns the distance in miles.'''

        long_1 = self.zips[zip1].longitude
        lat_1  = self.zips[zip1].latitude

        long_2 = self.zips[zip2].longitude
        lat_2  = self.zips[zip2].latitude

        dlong = long_2 - long_1
        dlat = lat_2 - lat_1
        a = (math.sin(dlat / 2))**2 + math.cos(lat_1) * math.cos(lat_2) * (math.sin(dlong / 2))**2
        c = 2 * math.asin(min(1, math.sqrt(a)))
        dist = 3956 * c
        return dist

    def close_zips(self, starting_zip, radius):
        '''For any given zip code (assuming it's valid), returns any zip codes within a 'radius' mile radius.'''

        zip_long = self.zips[starting_zip].longitude
        zip_lat  = self.zips[starting_zip].latitude

        close_zips = [self.zips[record].zip for record in self.zips if self.get_distance(self.zips[record].zip, starting_zip) < radius]
        return close_zips

    def __getitem__(self, zip):
        '''allows convenient 'dictionary' access to the zips'''
        return self.zips[str(zip)]

if __name__ == "__main__":
    # First, we check if the user wants to download the zip file
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "-d":
        if len(sys.argv) == 2:
            filename = 'zips.txt'
        else:
            filename = sys.argv[2]

        import urllib2
        zip_url = 'http://www.census.gov/tiger/tms/gazetteer/zips.txt'

        print "Downloading %s from the internet to %s on your local machine." % (zip_url, filename)
        f = open(filename, 'w')
        f.write(urllib2.urlopen(zip_url).read())
        f.close()
        print "Successfully downloaded zip file.  Use %s %s to run unittests." % (sys.argv[0], filename)

        sys.exit(1)

    # Otherwise, we do some unit testing
    if len(sys.argv) > 1:
        zip_code_filename = sys.argv[1]
        # The following is a hack b/c unittest seems to use sys.argv to grab arguments - which we don't want :)
        del sys.argv[1:]
    else:
        zip_code_filename = None

    import unittest

    class TestDistances(unittest.TestCase):
        def setUp(self):
            if len(sys.argv) > 1:
                self._zc = Zip_Codes(sys.argv[1])
            else:
                self._zc = Zip_Codes()

        def test_dist_measurement(self):
            zips = [
                    ('57350', '58368', 286.182054428), # HURON, SD ... PLEASANT LAKE, ND
                    ('75217', '11366', 1376.21109349), # DALLAS, TX ... FRESH MEADOWS, NY 
                    ('67431', '64631', 227.366924671), # CHAPMAN, KS ... BUCKLIN, MO 
                    ('57106', '27812', 1158.00278947), # SIOUX FALLS, SD ... BETHEL, NC 
                    ('54460', '50518', 254.522422855), # OWEN, WI ... BARNUM, IA 
                    ('54451', '28756', 802.75909488),  # MEDFORD, WI ... MILL SPRING, NC 
                    ('32615', '65624', 794.942194475), # SANTA FE, FL ... CAPE FAIR, MO 
                    ('67054', '71827', 439.965551049), # GREENSBURG, KS ... BUCKNER, AR 
                    ('45686', '36879', 463.978723078), # VINTON, OH ... WAVERLY, AL 
                    ('37845', '30506', 121.411082293), # PETROS, TN ... GAINESVILLE, GA 
                    ('49440', '29847', 699.897793808), # MUSKEGON, MI ... TRENTON, SC 
                    ('41331', '12046', 606.944002949), # HADDIX, KY ... COEYMANS HOLLOW, NY 
                    ('05083', '65244', 1093.97636115), # WEST FAIRLEE, VT ... CLIFTON HILL, MO 
                    ('84069', '70374', 1451.94104395), # RUSH VALLEY, UT ... LOCKPORT, LA 
                    ('95821', '55760', 1520.98809123)  # SACRAMENTO, CA ... MC GREGOR, MN 
                ]

            for zip in zips:
                self.assertAlmostEqual(zip[2], self._zc.get_distance(zip[0], zip[1]), 7, "%s distance from %s failed" % (zip[0], zip[1]))

        def test_getitem(self):
            self.assertEqual('PILGRIM GARDENS', self._zc['19026'].city)
            self.assertEqual('PILGRIM GARDENS', self._zc[19026].city)

        def test_closezips(self):
            close_zips = ['90210', '90212', '90035', '90211', '90067', '90069', '90046', '90048', '90077', '90024']
            self.assertEqual(close_zips, self._zc.close_zips('90210', 3))

    unittest.main()
