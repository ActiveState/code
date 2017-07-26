## Easy way to use Graph Facebook API without ad-hoc libraries 
Originally published: 2012-11-20 14:14:27 
Last updated: 2012-11-20 14:14:27 
Author: Filippo Squillace 
 
I was painfully lokking for a simple function that allow easily make GET or POST requests in Ruby without using complex libraries such as Koala for accessing to the Facebook Graph. At the end I gave up and did it by myself,\nso the function fb_api, based on net/http, is able to make GET or POST requests (depending if the request is for retrieving information of the graph or is for changing the graph such as post feed etc.).\nIt returns a dict from a JSON data structure.\n\nThis might be useful for your facebook app ;)