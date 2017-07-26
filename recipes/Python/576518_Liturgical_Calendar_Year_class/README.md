## Liturgical Calendar Year class  
Originally published: 2008-09-30 16:57:29  
Last updated: 2008-09-30 16:57:29  
Author: Martin Diers  
  
When initialized with a `year`, returns a class with a number of date attributes corresponding to common feasts of the western liturgical calendar. Number of Sundays after Epiphany and Trinity / Pentecost are also calculated, and stored in attributes. If the optional parameter `v2` is set to True, the calendar will return a post-Vatican II calendar which changes the date of Transfiguration Sunday, and the number of Sundays after Epiphany. In either case, the pre-Lent Sundays and Sundays after Pentecost will be set.\n\n**Note:** The `year` parameter is the year of the First Sunday in Advent - the beginning of the church year, and the resulting calendar thus ends in the following year.