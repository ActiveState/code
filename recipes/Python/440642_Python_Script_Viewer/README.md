## Python Script Viewer  
Originally published: 2005-10-03 18:17:11  
Last updated: 2005-10-03 18:17:11  
Author: Stephen Chappell  
  
First of all, this code was written to take advantage of the custom CGI module that I wrote. The purpose for this script is to allow someone to view a CGI script through a server. I have the problem that when I click on a python (*.py) file while viewed through my browser, the script is run so that it cannot be viewed. Unless the script is using "cgi.execute(function, exception)", then there is no way of getting around the problem. Therefore, this CGI application was written so that python files (and only *.py files) can be viewed if the user knows either the filename of a file in the same directory as this script or the full path of a file somewhere on the host computer. WARNING: do not use this script if you do not want someone to view any and all python scripts on your computer!