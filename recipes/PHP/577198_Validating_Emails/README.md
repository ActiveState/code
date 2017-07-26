## Validating Emails  
Originally published: 2010-04-17 13:35:37  
Last updated: 2011-06-13 15:10:47  
Author: Jonathan Fenech  
  
a small script that can be used for Validating Emails on 
 - Login pages
 - forums 



changed to preg_match from eregi function. now scripted validates everything typed in input boxes 

Old Code = 


           foreach($Email as $Emails)
	   { // checks Emails - .net , .com , .au  & etc
	   if(eregi("[a-zA-Z0-9]@+[a-z].{1,}com$",trim($Emails))|| eregi(            
           "[a-zA-Z0-9]@+[a-z].{1,}net$",trim($Emails)))












New Code = 




           foreach($Email as $Emails)
	   { // checks Emails - .net , .com , .au  & etc
	   if(!preg_match("/^[_\.0-9a-zA-Z-]+@([0-9a-zA-Z]
	   [0-9a-zA-Z-]+\.)+[a-zA-Z]{2,6}$/i", $Emails))

i changed from eregi function to preg_match function because eregi was taking out of PHP version 5.3.0 and 5.3.5.