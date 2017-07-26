## A script evaluating PSNR metric of two YUV420 frames  
Originally published: 2011-04-08 06:40:50  
Last updated: 2011-04-08 07:26:45  
Author: Denis Gorodetskiy  
  
A script evaluating PSNR metric of two YUV420 frames\n**usage: psnr.py filename1.yuv filename2.yuv frame_width frame_height**\n\nAlternatively if filename1 contains width and height in the form **file-1200x1600.yuv**,\nthe script will extract width and height of a frame from the filename. Then usage even simplier:\n**psnr.py filename1-1200x1600.yuv filename2.yuv**