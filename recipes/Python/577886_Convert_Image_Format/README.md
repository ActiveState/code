## Convert Image Format  
Originally published: 2011-09-30 10:39:30  
Last updated: 2011-09-30 10:46:21  
Author: s_h_a_i_o   
  
Simple GUI to allow converting images from one format to another. Available formats are: .gif .jpg .png .tif .bmp Uses PIL.\n\nThis is short and direct enhancement from recipe http://code.activestate.com/recipes/180801-convert-image-format. Two new features added:\n- Optional deletion of the original image files.\n- Optional recursive file selection. Implemented using http://code.activestate.com/recipes/577230-file-path-generator-from-path-patterns/\n\n**note** This assumes recipe/577230 is located in filePattern.py (see first import below)