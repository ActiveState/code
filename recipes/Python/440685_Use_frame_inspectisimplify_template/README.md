## Use frame inspection to simplify template usage 
Originally published: 2005-10-10 10:08:19 
Last updated: 2005-10-12 06:34:40 
Author: Nicolas Lehuen 
 
Using string templates to separate views from models and controllers is fine, but passing data from controllers to views is often tiresome. Using frame inspection can make things a lot more straightforward, saving you the hassle of explicitely passing each and every bit of data the template needs through boring lines of code like {'name':name}. Here is a sample with a fake templating system.