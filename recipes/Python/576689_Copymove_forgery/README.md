## Copy-move forgery detection in images  
Originally published: 2009-03-12 02:13:25  
Last updated: 2009-04-20 06:25:43  
Author: Agnius Vasiliauskas  
  
Ad-hoc algorithm for copy-move forgery detection in images.
This algorithm is robust so it can detect copy-move forgery in lossy compression formats such as jpeg.
Because this algorithm is ad-hoc - it heavily depends on script parameters. So if it don`t finds any copy-move
tamperings in image - try to lower essential parameter "block color deviation threshold".
Something like (you can also try to change other parameters as well):

%script image_file --blcoldev=0.05

If you want to look at some copy-move forgery detection examples, - you should check this site:

http://coding-experiments.blogspot.com/2009/03/detecting-copy-move-forgery-in-images.html