## How to add cookies/headers to SOAPpy callsOriginally published: 2005-11-07 07:58:10 
Last updated: 2005-11-07 16:22:30 
Author: Gopal Vijayaraghavan 
 
This hack allows you to add a cookie/header to a SOAPpy request. It uses a keyword args all-through to pass your own transports down to the SOAPpy core. It uses the ClientCookie module to store the cookies generated and/or to send the cookies.