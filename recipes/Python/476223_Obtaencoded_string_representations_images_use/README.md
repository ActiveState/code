## Obtain encoded string representations of images, for use in your apps

Originally published: 2006-04-03 18:15:55
Last updated: 2006-04-03 18:15:55
Author: stewart midwinter

Say you want to generate a default image with my app without having to include an image file with my app.  You'll want to encode the binary image data as text, using base64.  This image can later be displayed in my app, or a binary image file can be written by decoding the encoded text string using the base64 module.  To make this task a little easier for you, I created a small GUI app using Wax.   Simply run the app, select the image file you want converted, then copy the encoded text string and paste it into your app (which could be a Wax, wxPython, Qt or even Tkinter app).  The last part of the recipe shows you how to decode that text string back to binary data.