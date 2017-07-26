###Minimal unique procedure for the versionally challanged

Originally published: 2002-09-01 08:35:34
Last updated: 2002-09-01 08:35:34
Author: Nir Levy

Altough the latest Tcl verions have a -unique flag for lsort, older verions do not. So for those with older versions here is some nice, fast uinquer.\nNote that it assumes that the list items do not include the charecter ',' so it should probably be used only with numeric data.