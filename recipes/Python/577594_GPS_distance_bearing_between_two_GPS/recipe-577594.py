#-------------------------------------------------------------------------------
#Copyright (C) <2011> by <James Dyson>
#Contact dyson.james10@gmail.com
#Python 3

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this code to use this code without restriction, including without limitation 
#the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
#sell copies of the code, and to permit persons to whom the code is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the code.

#THE CODE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE CODE OR THE USE OR OTHER DEALINGS IN
#THE CODE.
#-------------------------------------------------------------------------------

from math import *

#Two Example GPS Locations
lat1 = 53.32055555555556
lat2 = 53.31861111111111
lon1 = -1.7297222222222221
lon2 = -1.6997222222222223
Aaltitude = 2000
Oppsite  = 20000

#Haversine Formuala to find vertical angle and distance
lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

dlon = lon2 - lon1
dlat = lat2 - lat1
a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
c = 2 * atan2(sqrt(a), sqrt(1-a))
Base = 6371 * c

#Horisontal Bearing
def calcBearing(lat1, lon1, lat2, lon2):
    dLon = lon2 - lon1
    y = sin(dLon) * cos(lat2)
    x = cos(lat1) * sin(lat2) \
        - sin(lat1) * cos(lat2) * cos(dLon)
    return atan2(y, x)

Bearing = calcBearing(lat1, lon1, lat2, lon2)
Bearing = degrees(Bearing)

Base2 = Base * 1000
distance = Base * 2 + Oppsite * 2 / 2
Caltitude = Oppsite - Aaltitude


#Convertion from radians to decimals
a = Oppsite/Base
b = atan(a)
c = degrees(b)


#Convert meters into Kilometers
distance = distance / 1000


#Output the data
print("---------------------------------------")
print(":::::Auto Aim Directional Anntenna:::::")
print("---------------------------------------")
print("Horizontial Distance:", Base,"km")
print("   Vertical Distance:", distance,"km")
print("    Vertical Bearing:",c)
print(" Horizontial Bearing:",Bearing)
print("---------------------------------------")
input("Press <enter> to Exit")
