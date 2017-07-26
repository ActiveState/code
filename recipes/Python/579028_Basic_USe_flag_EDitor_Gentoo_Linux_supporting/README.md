## A Basic USe flag EDitor for Gentoo Linux supporting on-the-fly editingOriginally published: 2015-02-28 07:04:31 
Last updated: 2015-02-28 07:04:31 
Author: Mike 'Fuzzy' Partin 
 
This allows for on-the-fly editing. Simply drop abused.py into your path, and ensure that -a is not set in EMERGE_DEFAULT_OPTS in /etc/portage/make.conf. Then whenver you are installing new packages, use abused in place of emerge (eg: abused multitail) you will be presented with a list of use flags that are used in this action, and a prompt for editing any of them, simply hit enter with no changes to fire off the build.