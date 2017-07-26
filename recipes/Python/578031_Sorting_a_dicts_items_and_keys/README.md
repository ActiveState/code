## Sorting a dict's items and keys  
Originally published: 2012-02-03 23:08:25  
Last updated: 2012-02-04 04:23:01  
Author: George V. Reilly  
  
[icalendar](https://github.com/collective/icalendar) uses its own CaselessDict as the base of many classes. I needed to produce the keys and items in a canonical order, so that certain keys would appear first.