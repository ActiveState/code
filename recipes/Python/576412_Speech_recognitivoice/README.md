## Speech recognition and voice synthesis in Python for Windows  
Originally published: 2008-08-08 14:47:16  
Last updated: 2008-08-14 16:57:43  
Author: Michael   
  
How to use the speech module to use speech recognition and text-to-speech in Windows XP or Vista.

The voice recognition system can listen for specific phrases, or it can listen for general dictation.

You can use speech.input() like you would use raw_input(), to wait for spoken input and get it back as a string.  Or, you can set up a callback function to be run on a separate thread whenever speech events are heard.  Multiple callbacks can be set up for multiple speech recognition events.

Uses the Python speech module: http://pyspeech.googlecode.com .