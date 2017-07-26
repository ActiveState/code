## "Safe" Eval 
Originally published: 2005-01-25 10:41:01 
Last updated: 2006-03-26 18:13:43 
Author: Michael Spencer 
 
Evaluate constant expressions, including list, dict and tuple using the abstract syntax tree created by compiler.parse. Since compiler does the work, handling arbitratily nested structures is transparent, and the implemenation is very straightforward.