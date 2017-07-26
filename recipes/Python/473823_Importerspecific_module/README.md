## Importer-specific module initialization

Originally published: 2006-02-03 15:06:53
Last updated: 2006-02-03 15:06:53
Author: runsun pan

Sometimes we want to have a module initialized in different ways. This function, getimporter(), while placed inside a module X, allow you to initialize module X according to the module (properties) that is importing X.