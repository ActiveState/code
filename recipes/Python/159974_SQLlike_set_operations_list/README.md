###SQL-like set operations with list comprehension one-liners.

Originally published: 2002-10-30 05:52:05
Last updated: 2002-11-12 11:12:28
Author: Attila Vásárhelyi

Sometimes it is needed to do set-like operations on database query results, or simple lists, without the burden of implementing a class for sets, or importing a separate module. List comprehensions are quick way to do this, here is a collection of them. Although most of them are banal, let us just collect them in one place. Also, they are not the fastest, nor the most elegant, but the quickest to drop into your code if you need a proof of concept.