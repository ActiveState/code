## Format number function  
Originally published: 2007-01-03 04:07:33  
Last updated: 2007-01-03 18:54:35  
Author: Clodoaldo Pinto Neto  
  
For many languages it is possible to use the locale module to format numbers. But there are at least three languages for which the locale.localeconv()['thousands_sep'] is empty: brazilian portuguese - 'pt_br', portuguese - 'pt' and spanish - 'es'.

The first function, format_positive_integer() will return the passed integer number as a string with the thousands group separator added.

The second function, format_number() much more generic, will accept any number, integer or float, positive or negative, and return a string with the thousands group separator and the desired precision.