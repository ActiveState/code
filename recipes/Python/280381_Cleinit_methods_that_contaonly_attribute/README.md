###Clean up __init__() methods that contain only attribute assignments.

Originally published: 2004-04-27 01:19:19
Last updated: 2004-04-27 01:19:19
Author: Peter Otten

Did you ever have to write an initializer whose body consisted of little more than a suite of self.attr = attr style assignments? Here's a utility function that factors out this task.