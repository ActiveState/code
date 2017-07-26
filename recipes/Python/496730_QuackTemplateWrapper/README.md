## QuackTemplate.Wrapper 
Originally published: 2006-05-22 09:21:16 
Last updated: 2006-05-22 09:21:16 
Author: Costas Malamas 
 
QuackTemplate.Wrapper is a template helper class: it takes arbitrary Python objects and uses__gettitem__ so that the wrapped object can be passed into the standard Python string substitution mechanism.  It can follow method calls, dict keys and list members (to some extent).