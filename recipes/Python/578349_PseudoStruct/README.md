## PseudoStruct

Originally published: 2012-11-25 03:43:05
Last updated: 2012-11-25 03:43:06
Author: Matthew Zipay

This is a recipe for a Python "data object." It is similar in function to namedtuple (http://code.activestate.com/recipes/500261/) and recordtype (http://code.activestate.com/recipes/576555-records/) in that it is a simple container for data, but is designed to meet three specific goals:\n1. Easy to subclass data objects.\n2. Get/set speed comparable to a simple class.\n3. Minimal memory consumption per instance.