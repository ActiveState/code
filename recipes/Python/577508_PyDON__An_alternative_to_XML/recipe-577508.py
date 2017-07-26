#pydon file - configure.pdn
configuration = {
   "Username" : "lostp",
   "Password" : "password",
   "Address" : { 
                 "HouseNumber" : 158,
                 "Place" : "Bangalore",
                 "IsOwner?" : True
               }
  }
#equivalent in XML would be 
# <configuration>
#    <Username>lostp</Username>
#    <Password>password</Password>
#    <Address>
#        <HouseNumber type="int">158</HouseNumber>
#        <Place>Bangalore</HouseNumber>
#        <IsOwner type="bool">True</IsOwner>
#    </Address>
# </configuration>

#And the file can be used as so> 
#demo.py

#!/usr/bin/python
execfile("configure.pdn")
username = configure["Username"]
passwd = configure["Password"]
houseno = configure["Address"]["HouseNumber"]
place = configure["Address"]["Place"]
isowner = configure["Address"]["IsOwner?"]

#and done. This can be used wherever you intend to use "XML" such as in CLIENT-SERVER communication
#You can get rid of the XMLRPC altogether between PythonClient-PythonServer using PyDON
#enjoy.
