## Change line endings 
Originally published: 2001-07-26 08:33:02 
Last updated: 2001-11-18 22:26:53 
Author: Gordon Worley 
 
When working between platforms, it is often necessary to convert the line endings on files for them to work, especially when it comes to code.  Pass Unix Python code with \\r and it goes nowhere.  Same on Mac Python with \\n.  This code simply and easily fixes the problem.