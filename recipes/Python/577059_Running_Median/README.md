## Running Median

Originally published: 2010-02-20 08:22:00
Last updated: 2010-02-20 08:22:00
Author: Raymond Hettinger

Maintains sorted data as new elements are added and old one removed as a sliding window advances over a stream of data. Running time per median calculation is proportional to the square-root of the window size.