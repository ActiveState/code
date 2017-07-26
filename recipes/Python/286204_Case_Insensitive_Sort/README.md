## Case Insensitive Sort  
Originally published: 2004-07-07 06:09:12  
Last updated: 2004-07-07 06:09:12  
Author: Michael Foord  
  
This is a recipe that does a case insensitive sort. The normal sort methods of lists has 'B'<'a', which means that it would sort 'Pear' to come before 'apple' in a list. You can pass in a function to the sort method to change this... but this can be slow. This is a function that transforms the list, uses the sort method and then transforms it back.