## Dynamically change the Python system path

Originally published: 2001-04-10 11:23:47
Last updated: 2001-10-16 17:04:08
Author: Robin Parmar

Adds the specified path to the Python system path if it is not already there. Takes into account terminating slashes and case (on Windows).\n\nReturns -1 if the path does not exist, 1 if it was added, and 0 if it was not (because it is already present).