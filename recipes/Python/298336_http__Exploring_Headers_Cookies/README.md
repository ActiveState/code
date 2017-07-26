###http - Exploring Headers and Cookies from Servers

Originally published: 2004-08-02 02:19:23
Last updated: 2004-08-18 10:23:52
Author: Michael Foord

This CGI script allows you to specify a URL. It fetches the URL and displays all the headers sent by the server.\nIt is based on approx.py the CGI-proxy I'm building. It includes authentication circuitry and I'm using it to understand http authentication.\n\nThis script demostrates using urllib2 to fetch a URL - using a request object with User-Agent header. It also demostrates basic authentication and shows the possible http errors - using a dictionary 'borrowed' from BaseHTTPServer.\n\nIt will also save cookies using the ClientCookie module, if it's available.