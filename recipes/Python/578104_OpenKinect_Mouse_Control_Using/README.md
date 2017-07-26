## OpenKinect Mouse Control Using Python  
Originally published: 2012-04-14 21:00:12  
Last updated: 2012-04-15 18:49:00  
Author: Alexander James Wallar  
  
This is a simple code that lets a user control the mouse and left-click using the Microsoft Kinect, Python, and OpenKinect. 

    Computer Prerequisites:
    -OpenKinect
    -Python Wrapper for OpenKinect
    -A Linux machine using Ubuntu
    -OpenCV 2.1
    -OpenCV 2.3
    -Python 2.7.2
    -A Microsoft Kinect
    -A Microsoft Kinect USB Adapter
    -PyGame
    -Xlib for Python

To run this code you either need to start it in the terminal or you need to write a short bash script that runs the code. This is necessary because it requires super-user privileges.

The Bash script is (Assuming the code is saved by the name 'Hand Tracking.py' in /home/$USER directory:

    #!bin/bash
    cd 'home/$USER'
    gksudo python 'Hand Tracking.py'

The code is heavily commented and most of what you will need to know is there. 
 