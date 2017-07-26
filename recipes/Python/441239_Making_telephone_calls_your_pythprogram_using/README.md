## Making telephone calls from your python program using Voicent Gateway  
Originally published: 2005-10-13 16:28:19  
Last updated: 2005-10-13 16:28:19  
Author: Andrew Kern  
  
The Voicent Python Simple Interface class contains the following functions.

    callText
    callAudio
    callStatus
    callRemove
    callTillConfirm

These functions are used to invoke telephone calls from your Python program. For example, callText is used to call a specified number and automatically play your text message using text-to-speech engine.

In order for this class to work, you'll need to have Voicent Gateway installed somewhere in your network. This class simply sends HTTP request for telephone calls to the gateway. Voicent has a free edition for the gateway. You can download it from http://www.voicent.com

More information can be found at:
http://www.voicent.com/devnet/docs/pyapi.htm