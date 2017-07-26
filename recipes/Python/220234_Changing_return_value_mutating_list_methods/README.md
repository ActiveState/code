## Changing return value for mutating list methods (meta programming)  
Originally published: 2003-09-07 06:08:19  
Last updated: 2003-09-13 16:16:51  
Author: Stephan Diehl  
  
Mutating list methods such as 'append' or 'extend' return None instead of the (mutated) list itself. Sometimes, this is not the desired behaviour.\nThe <a href="http://groups.google.de/groups?dq=&hl=de&lr=&ie=UTF-8&oe=UTF-8&threadm=I706b.17723%24hE5.626547%40news1.tin.it&prev=/groups%3Fdq%3D%26num%3D25%26hl%3Dde%26lr%3D%26ie%3DUTF-8%26oe%3DUTF-8%26group%3Dcomp.lang.python%26start%3D75"> Discussion</a> on comp.lang.python resulted in the following solution.\nThe shown code is my own, while two other solutions are presented in the discussion.