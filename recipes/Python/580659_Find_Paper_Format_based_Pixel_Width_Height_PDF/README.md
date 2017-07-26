###Find Paper Format of based on Pixel Width and Height of a (PDF) Page

Originally published: 2016-05-05 23:47:48
Last updated: 2016-05-05 23:47:49
Author: Harald Lieder

A simple function to determine what format page a page in document has. Parameters provided are width and height in float or integer format.\n\nReturn is a string like "A4-P" or "Letter-L" when an exact fit is found. If not, information is provided as a string like "width x height (other), closest <format> width x height". The closest format in this case is determined by minimizing the sum of absolute differences of width and height with a table of official formats.