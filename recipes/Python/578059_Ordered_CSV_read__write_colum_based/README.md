## Ordered CSV read / write with colum based lookup 
Originally published: 2012-03-02 12:45:29 
Last updated: 2012-03-02 12:45:29 
Author: Gregory Nicholas 
 
This allows you to hold on to your csv in a dict form, do lookups and modifications, and also write it in a preserved order. You can also change which column you want to be your lookup column (making sure that there is a unique id for every row of that column. In my example of usage, it assumes that both classes are contained withing the same file named 'CustomDictReader.py'