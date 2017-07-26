## Protect PHP File that must be include 
Originally published: 2003-06-24 17:41:18 
Last updated: 2003-06-24 17:41:18 
Author: imam ferianto 
 
This Section is describe how we can protect php module that can calling in with include function, but is not secure and its have big risk. For the solution is we can make this module file cannot execute or calling when it's not include, the code simple with test file name. Some study case: we hosting in sites that we cannot protection in dir, regulary we add .htacces\nin folder /inc/ I was putin .htacces so if we calling http://localhost/inc/ is displayed forbidden but if I try if we calling http://localhost/inc/connect-module.php it will be succesfull and maybe some accident will happen here