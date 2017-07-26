## DBF reader and writer -- selective fields and nullreplace  
Originally published: 2016-09-18 20:39:19  
Last updated: 2016-09-18 20:39:20  
Author: Tomas Nordin  
  
This fork assumes a desire for limited selection of field names. With\nhuge files this might be necessary on some machines.\n\nAlso, assuming that the meaning of null in a dbf file means zero might\nbe a mistake, so the fork adds an argument nullreplace as way to\nchoose what to replace null with. Null is sometimes used to mean\nmissing value. This change is decoupled from the selective names\nfeature.