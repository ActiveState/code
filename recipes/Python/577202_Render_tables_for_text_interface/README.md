## Render tables for text interface  
Originally published: 2010-04-20 18:02:02  
Last updated: 2010-04-20 18:02:51  
Author: Denis Barmenkov  
  
Sometime pprint module is not enough for formatting data for console or log file output.
This module provide function which fill the gap.

**Sample function call:**

    nums = [ '1', '2', '3', '4' ]
    speeds = [ '100', '10000', '1500', '12' ]
    desc = [ '', 'label 1', 'none', 'very long description' ]
    lines = format_table( [(nums, ALIGN_RIGHT|PADDING_ALL, 'NUM'), 
                           (speeds, ALIGN_RIGHT|PADDING_ALL, 'SPEED'), 
                           (desc, ALIGN_LEFT|PADDING_ALL, 'DESC')] )

**Output:**

    =======================================
    | NUM | SPEED | DESC                  |
    =======================================
    |   1 |   100 |                       |
    |   2 | 10000 | label 1               |
    |   3 |  1500 | none                  |
    |   4 |    12 | very long description |
    =======================================