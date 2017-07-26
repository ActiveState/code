## Running 2Balls in Vpython by Flip-Flopping.  
Originally published: 2011-07-17 16:50:00  
Last updated: 2011-07-17 16:50:01  
Author: Dominic Innocent  
  
Getting Vpython to run 2 moving objects is tricky as it tends to focus on only one. The answer I have used is to 'Flip-Flop' between the 2 blocks of code running each object; Set up 2 values for the flip-flop K & P. At the end of each nested 'While' P will be incramented (p=p+1). K is the remainder of P/2 (k=p%2). If k = 0 Flip! If k != 0 Flop!. I haven't got it to recognise a 'collision' event yet; & that is very Frustrating!