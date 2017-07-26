## WebSocket interface 
Originally published: 2012-11-24 02:37:28 
Last updated: 2012-11-25 16:52:21 
Author: Nick Faro 
 
This tries its best to be a replacement for the regular `socket` module.\n\nIt supports only sending and receiving but should be useful enough.\n\nThe only real difference should be that you can't specify the number of bytes is received, instead do\n\n    for message in socket.recv():\n        print(message)\n\nRevision 2:\nAdded proper message receiving. Previously it just requested a ton of data. Now it reads 2 bytes, determines the length, then requests that much.