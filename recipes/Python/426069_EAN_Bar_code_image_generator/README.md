## EAN Bar code image generator  
Originally published: 2005-06-18 04:07:13  
Last updated: 2005-06-18 04:07:13  
Author: remi inconnu  
  
This class generate EAN bar code, it required PIL (python imaging library)
installed.

If the code has not checksum (12 digits), it added automatically.

Create bar code sample :
   from EANBarCode import EanBarCode
   bar = EanBarCode()
   bar.getImage("9782212110708",50,"gif")