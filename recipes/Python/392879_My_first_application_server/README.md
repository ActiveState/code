## My first application server  
Originally published: 2005-03-26 00:26:10  
Last updated: 2009-02-23 11:53:57  
Author: Pierre Quentel  
  
For those who want to start dynamic web programming, but don't know what to choose among the many Python web frameworks, this program might be a good starting point\n\nScriptServer is a minimalist application server, handling both GET and POST requests, including multipart/form-data for file uploads, HTTP redirections, and with an in-memory session management. It can run Python scripts and template files using the standard string substitution format\n\nThe scripts are run in the same process as the server, avoiding the CGI overhead. The environment variables are provided in the namespace where the script runs\n\nTo start the server, run \n\n    python ScriptServer.py\n\nIn your web browser, enter http://localhost, this will show you a listing of the directory. Add the scripts in the same directory as ScriptServer\n