###Broken Test decorator

Originally published: 2006-01-12 09:07:50
Last updated: 2006-01-12 09:07:50
Author: Scott David Daniels

broken_test_XXX(reason) is a decorator for "inverting" the sense of the following unit test.  Such tests will succeed where they would have failed (or failed because of a raised exception), and fail if the decorated test succeeds.