## Select some nth smallest elements, quickselect, inplace

Originally published: 2010-11-30 07:16:22
Last updated: 2010-11-30 07:32:42
Author: Teodor Kichatov

fork of http://code.activestate.com/recipes/269554-select-the-nth-smallest-element/\nO(n) quicksort style algorithm for looking up data based on rank order. Useful for finding medians, percentiles, quartiles, and deciles.  Equivalent to [data[n] for n in positions] when the data is already sorted.