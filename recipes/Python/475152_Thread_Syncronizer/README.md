## Thread Syncronizer

Originally published: 2006-03-19 12:06:33
Last updated: 2006-03-19 20:16:47
Author: Stephen Chappell

This recipe presents the sync class and an example usage. The primary ingredient\nin this recipe are the locks from the thread module. The idea that is followed\nis quite simple. You have a room with a front door and a back door. Threads walk\ninto the front door and out the back door. Your room only has a certain capacity\nfor threads (specified on construction of the room [sync object]) and the back\ndoor is closed. When the room is full, the front door is closed; and the back\ndoor is opened. When the room has been emptied, the front door is opened; and\nthe back door is closed. In this way, you know that all of your threads pile\ninto a room; and that when they all arrive, they will all exit concurrently with\neach other. The example function shows two different sync objects being used in\ndifferent roles.