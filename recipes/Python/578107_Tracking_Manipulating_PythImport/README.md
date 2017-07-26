## Tracking and Manipulating the Python Import State

Originally published: 2012-04-22 07:27:28
Last updated: 2012-04-22 07:27:29
Author: Eric Snow

This is a rough analog to the import engine described in PEP 406.  Here I've called it ImportState.The focus here is on using it as a context manager to limit changes to the import state to a block of code (in a with statement).  Differences from PEP 406 are described below.