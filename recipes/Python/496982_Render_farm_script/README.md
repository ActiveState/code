## Render farm script  
Originally published: 2006-08-22 09:10:49  
Last updated: 2006-08-22 09:10:49  
Author: Will Ware  
  
This script runs a render farm on a bunch of networked machines, each with SSHD running, and POV-Ray and ImageMagick installed. The host machine uses mpeg2encode and ffmpeg to produce a MP4 video file, which I transfer to the Mac to burn a DVD. To keep life simple, I clone the same .ssh directory on all the machines.