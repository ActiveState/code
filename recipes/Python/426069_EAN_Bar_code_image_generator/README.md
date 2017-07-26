## EAN Bar code image generator  
Originally published: 2005-06-18 04:07:13  
Last updated: 2005-06-18 04:07:13  
Author: remi inconnu  
  
This class generate EAN bar code, it required PIL (python imaging library)\ninstalled.\n\nIf the code has not checksum (12 digits), it added automatically.\n\nCreate bar code sample :\n   from EANBarCode import EanBarCode\n   bar = EanBarCode()\n   bar.getImage("9782212110708",50,"gif")