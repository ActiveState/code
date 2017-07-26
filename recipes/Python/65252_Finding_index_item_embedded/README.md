###Finding the index of an item in embedded sequences

Originally published: 2001-06-19 22:15:09
Last updated: 2001-06-19 22:15:09
Author: Brett Cannon

This function will return a list containing the indices needed to reach an item in embedded sequences.\n\nSo deepindex([[1,2],[3,[4,[5,6]]],7,[8,9]],6) will return [1,1,1,1].