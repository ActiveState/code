###Table objects with  operations in SQL-like syntax.

Originally published: 2004-07-02 16:05:48
Last updated: 2004-09-02 13:21:24
Author: Uwe Schmitt

This recipe implements a simple Table class which allows searching in a syntax similar to SQLs WHERE statement. So if t is Table, t.a == 3 finds all rows, where the column named "a" has the value 3. Intersection and unions of search results are possible too, for examples look at the __main__ part below.