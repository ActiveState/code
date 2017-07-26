## Search nth smallest element in really big fileOriginally published: 2010-11-30 07:31:57 
Last updated: 2010-11-30 17:38:38 
Author: Teodor Kichatov 
 
Search nth smallest float in really big file (more, more and more bigger than available RAM)\nin a single pass through the file\n\nif your file more than 150GB - you should use a more appropriate sampling params to the data\nmore - you can use tempfile to store data(interval) returned from func fill_interval\ndata:\nfile with only one float number per line, good shuffled\n\n