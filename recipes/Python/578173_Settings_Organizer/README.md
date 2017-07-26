## Settings Organizer  
Originally published: 2012-06-25 14:06:30  
Last updated: 2012-07-04 22:16:36  
Author: Stephen Chappell  
  
Provide an easy method to manage program options among multiple versions.

This module contains two classes used to store application settings in such a
way that multiple file versions can possibly coexist with each other. Loading
and saving settings is designed to preserve as much data between versions. An
error is generated on loading if saving would lead to any data being lost.