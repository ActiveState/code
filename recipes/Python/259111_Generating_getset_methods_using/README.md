###Generating get/set methods using closures

Originally published: 2003-12-23 09:58:11
Last updated: 2003-12-23 09:58:11
Author: Arun Persad

When creating a class, we often end up writing lots get/set methods which essentially do the same thing e.g. get_name, get_age, ... , set_name, set_age, ...\n- each such method will simply set or return the value of its associated attribute.\n\nThis recipe is a stategy for automating the creation of such simple get/set methods and exposing them as properties.