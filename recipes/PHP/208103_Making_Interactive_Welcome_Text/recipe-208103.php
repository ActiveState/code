function sayhello(){
 $hours=date("G")+0;
 ### you can set own criteria in your country
 ### whats time we must say good morning and etc
 if( $hours>=0 &&  $hours<=14) $hellowords="Good Morning";
 elseif( $hours<=18) $hellowords="Good Afternoon";
 else $hellowords="Good Night";
 return $hellowords;
}


### calling in your script with
### echo "Hello user, ".sayhello();
