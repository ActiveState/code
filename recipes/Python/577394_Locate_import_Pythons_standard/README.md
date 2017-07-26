## Locate and import Python's standard regression tests

Originally published: 2010-09-17 11:31:30
Last updated: 2010-09-17 11:31:31
Author: Steven D'Aprano

The Python standard library comes with an extensive set of regression tests. I had need to import and run some of these tests from my own code, but the test directory is not in Python's path. This simple helper function solves the problem.