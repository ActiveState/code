## Create .m3u playlists on the fly for mp3 dowloads  
Originally published: 2006-02-27 10:32:05  
Last updated: 2006-02-27 10:32:05  
Author: Davide Andrea  
  
When offering an MP3 file for downloading, usually two files are stored in the server: the .mp3 file itself, and a small playlist file (.m3u) which tell the mp3 player to stream the .mp3 file.
This script avoids the need of storing an .m3u file for each .mp3 file. It serves an .m3u playlist "file" to the client, created on the fly.
You can test this script in the site of community radio KGNU; go to http://kgnu.org/ht/listings.html and click on any "Listen" icon.