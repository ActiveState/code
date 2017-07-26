## Alternative to __del__ through __finalize__ and __finalattrs__  
Originally published: 2007-05-12 00:33:44  
Last updated: 2007-05-13 19:13:22  
Author: Steven Bethard  
  
This recipe introduces a __finalize__ method along with a __finalattrs__ class attribute which can be used for simple finalization without all the complications that __del__ currently creates.

Simply list any instance attributes that need to be available for finalization in the __finalattrs__ class attribute. When the instance is garbage collected, the __finalize__ method will be called with an object exposing just the __finalattrs__ attributes.