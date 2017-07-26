## use __getattr__ to fake unlimited depth of attributes.methods 
Originally published: 2005-06-29 14:18:12 
Last updated: 2005-06-29 21:19:15 
Author: Bartlomiej Górny 
 
This recipe allows for calling an unlimited chain of nonexistent attributes - every call is forwarded to a default method with attribute chain as argument.