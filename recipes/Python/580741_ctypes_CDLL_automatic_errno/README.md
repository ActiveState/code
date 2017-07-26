###ctypes CDLL with automatic errno checking

Originally published: 2017-01-03 10:31:25
Last updated: 2017-01-03 10:31:26
Author: Oren Tirosh

This class extends ctypes.CDLL with automatic checking of errno and automatically raises an exception when set by the function.\n