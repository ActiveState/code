###Accepting Four Points in 2-space

Originally published: 2004-03-10 06:47:51
Last updated: 2004-03-10 06:47:51
Author: Bill Bell

Photographic document images are often rotated, if only slightly. This code mediates an input of a series of four points--assumed to be the corners of a rectangular document--in any order, as mouse clicks. Then it determines the orientation of the points and calculates a "quality" value, as an indication to the user of how well the four points s/he has chosen approximate to the corners of a rotated rectangle. Finally, it makes the information that it has been passed, or that it has been able to glean, available to the script that invoked it.