## convert a directory full of png images to a (wxPython) module  
Originally published: 2006-08-02 06:43:56  
Last updated: 2006-08-02 06:43:56  
Author: Egor Zindy  
  
I use this utility to generate an "images.py" module which I use to provide images to my applications via wx.ImageFromStream . You can see an output in my other recipe "A foldable panel with a Windows XP look and feel". The utility is called "convert.py" and can be put in a folder together with the png images. When run, it'll generate the "images.py" file which can be moved to wherever it'll be used. The only thing I'm checking for is that "convert.py" won't overwrite an existing "images.py" file in the same directory.