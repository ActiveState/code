## Get user's IP address even when they're behind a proxy  
Originally published: 2011-07-15 21:19:16  
Last updated: 2011-07-15 21:19:17  
Author: Ben Hoyt  
  
Function to get the user's IP address in a web app or CGI script, even when they're behind a web proxy.

We use web.py as our web framework, but change web.ctx.env and web.ctx.get('ip') to whatever the equivalents are for the CGI environment variables and REMOTE_ADDR are in your framework.