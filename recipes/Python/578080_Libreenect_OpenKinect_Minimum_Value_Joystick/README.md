## Libreenect (OpenKinect) Minimum Value Joystick With Display - Kinect Demo Using OpenKinect SDK  
Originally published: 2012-03-18 03:05:31  
Last updated: 2012-03-18 18:52:42  
Author: Alexander James Wallar  
  
This demo requires you to be using a Linux machine and to have libfreenect installed with the python wrapper. This demo also requires you to have opencv, numpy, and pygame. They can all be installed using sudo apt-get install {PROGRAM NAME HERE}. Here are instructions on installing libfreenect: http://openkinect.org/wiki/Getting_Started. Okay, so what this demo does is finds the minimum point on the depth image and uses the index of this minimum point to create a four button joystick that codes for 'A', 'B', 'X', 'Y'. It also uses the minimum point and the RGB image to put a circle on the minimum point on the screen. So basically a dot will follow your hand on the RGB image. If the minimum value is larger than 600 (arbitrary units), the color of the dot will change from red to purple and the dot will remain stationary. Also, if the Kinect is not properly opened the first time,  unplug it and plug it back in and run in the terminal sudo freenect-glview. After try running the program again. One more thing, this code requires super user privileges so run it through the terminal. Here is how to do this for linux n00bs.

1. Change your directory the the directory the code is in (use cd {PATH})
2. Run the code using sudo python {FILENAME}
3. Don't forget to add the the .py at the end