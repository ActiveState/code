## Variant of property() allowing one function to be used for multiple attributes.  
Originally published: 2003-06-12 07:43:06  
Last updated: 2003-06-12 07:43:06  
Author: Raymond Hettinger  
  
Saves the name of the managed attribute and uses the saved name
in calls to the getter, setter, or destructor.  This allows the
same function to be used for more than one managed variable.
<br>
Using property() with more than one variable results in many
lines of duplicate code for the individual getters, setters,
and destructors.  This recipe shows how to reuse these functions
for multiple variables.  Also, it provides default functions so that
the only the interesting functions need to be specified.