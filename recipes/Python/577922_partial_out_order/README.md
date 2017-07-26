## partial with out of order arguments

Originally published: 2011-10-26 12:03:06
Last updated: 2011-10-27 16:54:26
Author: Przemyslaw Podczasi

Working with Windows API which usually takes like a zillion for each function can be a little bit frustrating and if I want to only change two in the middle for each call I had to wrap everything into lambda functions which change arguments to the order that I need to use with partial.\n\nSo finally I added kinda dangerous decorator which inserts keywords into right position if detected and was about to use it but ctypes functions don't accept keyword arguments :D so just ended up with decorator :)\n