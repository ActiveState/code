## php backwards compatibility porting tips  
Originally published: 2013-02-10 00:38:31  
Last updated: 2013-02-10 00:40:26  
Author: imam ferianto  
  
Hello again, on december 2012, I was porting my old php code (php4) to new php 5.4.3.
There are to many errors within code, especially for session, eregi, global variables and others.
This some pieces step for compatibility porting:

1. add global variable definiton on some function that need outside variable
 <code>
   function getuser(){
       global $loginid,$password;
   }
  </code>

2. replace eregi(/find/,str) with preg_match(//,str)

3. add function exists for function that not exists in php5.4.3.
   for example:
   <code>
   if(!function_exists("session_is_registered")){
     function session_is_registered($var){
         return isset($_SESSION[$var]);
     }
   }
   if(!function_exists("session_register")){
     function session_register($var){
        $_SESSION[$var]=$_GLOBALS[$var];
     }
   }
   </code>



Ok there is my tips, how about you?  
