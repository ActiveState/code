/*code for session compatibility*/

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
