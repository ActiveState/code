## simplest useful HTTPS with basic proxy authentication  
Originally published: 2004-08-24 07:01:07  
Last updated: 2005-12-28 17:27:47  
Author: John Nielsen  
  
This is just about the most simple snippet of how to do proxy authentication with SSL using python. The current httplib only supports ssl through a proxy _without_ authentication. This example does basic proxy auth that a lot of proxy servers can support. This will at least give someone an idea of how to do it and then improve it and incorporate it however they want.