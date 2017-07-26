## tkinter custom fonts  
Originally published: 2017-04-10 00:20:04  
Last updated: 2017-04-10 01:07:11  
Author: Miguel Martínez López  
  
One Windows the best solution is to use the trick explained here:\n\nhttp://stackoverflow.com/a/30631309\n\nAnother possibility is to use PIL. creating an image with the text and a specific font.\n\nI provide 2 classes: *CustomFont_Label* and *CustomFont_Message*.\n\n*CustomFont_Message* displays multilines but requires the *width* parameter.