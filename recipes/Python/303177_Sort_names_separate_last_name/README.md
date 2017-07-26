## Sort names and separate by last name initialOriginally published: 2004-09-02 11:05:30 
Last updated: 2004-09-02 11:05:30 
Author: Brett Cannon 
 
When you write a directory for a group of people, you want it grouped by last name initial and then sorted alphabetically.  This recipe does just that; it creates a dictionary keyed by last name initial with a value  of a tuple of names sorted in alphabetical order.\n\nThe input to 'groupnames' should be an iterable that returns strings that contain names written in first-middle-last fashion with each part separated by whitespace.  The resulting names in the grouped dict will have normalized whitespace.