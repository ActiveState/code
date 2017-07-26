###Ordered CSV read / write with colum based lookup

Originally published: 2011-12-24 19:44:13
Last updated: 2011-12-24 19:44:13
Author: __nero 

This allows you to hold on to your csv in a dict form, do lookups and modifications, and also write it in a preserved order. You can also change which column you want to be your lookup column (making sure that there is a unique id for every row of that column. In my example of usage, it assumes that both classes are contained withing the same file named 'CustomDictReader.py'