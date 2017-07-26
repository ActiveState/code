## Formats current exception with stack trace so that it fits in single line and has known encoding. 
Originally published: 2005-11-04 03:07:54 
Last updated: 2005-12-01 07:43:44 
Author: Dmitry Dvoinikov 
 
Have you ever tried to log an exception of unknown type ? What's in it ? How to fetch stack trace ? Will str(e) return plain ascii or international chars ? Is logger ready for it ? This recipe provides a formatting function.