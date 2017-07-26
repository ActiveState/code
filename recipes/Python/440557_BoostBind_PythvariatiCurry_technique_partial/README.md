###Boost.Bind in Python (a variation of Curry technique, partial function application)

Originally published: 2005-09-14 21:48:40
Last updated: 2005-09-22 04:47:28
Author: Maxim Khesin

The Boost.Bind library\nhttp://www.boost.org/libs/bind/bind.html\n, which I use a lot in C++, has a very nice implementation of the Curry technique. The main innovation of the library is usage of 'placeholders', which allows 'currying' arbitrary parameters in the arg list (please see discussion section). I missed this library in Python, and reimplementing it in a dynamic language was a piece of cake (and I did not have to yell at my compiler to get it done ;). Enjoy!