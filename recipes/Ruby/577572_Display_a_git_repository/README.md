## Display a git repository

Originally published: 2011-02-11 18:57:26
Last updated: 2012-07-05 17:01:53
Author: Noufal Ibrahim

A tiny script to display the entire contents of a medium sized git repository. It will display tags, branches and commits with different shapes and colours and the commits messages in a dimmed colour. \n\nIt relies on graphviz to do the plotting. \nUse it like so \n\n     ruby plotrepo.rb /path/to/repository | dot -Tpng | display -antialias