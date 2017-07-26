## Efficient Running Median using an Indexable SkiplistOriginally published: 2009-10-15 03:40:10 
Last updated: 2010-02-07 14:40:03 
Author: Raymond Hettinger 
 
Maintains sorted data as new elements are added and old one removed as a sliding window advances over a stream of data.  Also gives fast indexed access to value.  Running time per median update is proportional to the log of the window size.