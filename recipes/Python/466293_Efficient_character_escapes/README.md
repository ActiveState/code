###Efficient character escapes decoding

Originally published: 2006-01-13 13:38:51
Last updated: 2006-01-14 01:55:59
Author: Wai Yip Tung

You have some string input with some specical characters escaped using syntax rules resemble Python's. For example the 2 characters '\\n' stands for the control character LF. You need to decode these control characters efficiently. Use Python's builtin codecs to decode them efficiently.