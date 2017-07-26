## Secure Password Generator  
Originally published: 2011-06-17 15:00:30  
Last updated: 2011-06-17 15:25:20  
Author: amir naghavi  
  
A password generator that uses OS facilities to generate none pseudo random numbers.\nthe SystemRandom uses  CryptGenRandom in Windows and  /dev/random in linux and it is so better to use this to create random numbers in cryptography or any other security areas.