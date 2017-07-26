## Generate List of Numbers from Hyphenated and comma separeted string like "1-5,25-30,4,5"

Originally published: 2010-07-01 02:08:09
Last updated: 2010-07-01 02:08:09
Author: Siddhant Sanyam

This function takes a range in form of "a-b" and generate a list of numbers between a and b inclusive.\nAlso accepts comma separated ranges like "a-b,c-d,f" will build a list which will include numbers from a to b, a to d and f\nExample:\nhyphen_range('54-78')\nhyphen_range('57-78,454,45,1-10')\nhyphen_range('94-100,1052,2-50')