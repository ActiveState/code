## Handling ties for top largest/smallest elements

Originally published: 2009-04-05 08:54:06
Last updated: 2009-04-07 18:57:35
Author: George Sakkis

The heapq module provides efficient functions for getting the top-N smallest and\nlargest elements of an iterable. A caveat of these functions is that if there\nare ties (i.e. equal elements with respect to the comparison key), some elements\nmay end up in the returned top-N list while some equal others may not:\n\n    >>> nsmallest(3, [4,3,-2,-3,2], key=abs)\n    [-2, 2, 3]\n\nAlthough 3 and -3 are equal with respect to the key function, only one of them\nis chosen to be returned. For several applications, an all-or-nothing approach\nwith respect to ties is preferable or even required.\n\nA new optional boolean parameter 'ties' is proposed to accomodate these cases.\nIf ties=True and the iterable contains more than N elements, the length of the\nreturned sorted list can be lower than N if not all ties at the last position\ncan fit in the list:\n\n    >>> nsmallest(3, [4,3,-2,-3,2], key=abs, ties=True)\n    [-2, 2]\n