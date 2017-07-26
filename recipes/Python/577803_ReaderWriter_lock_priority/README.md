## Reader-Writer lock with priority for writers

Originally published: 2011-07-22 18:47:52
Last updated: 2011-09-28 21:45:04
Author: Mateusz Kobos

The following class implements a reader-writer lock to use in the second readers-writers problem with python threads. In this problem, many readers can simultaneously access a share, and a writer has an exclusive access to this share. Additionally, the following constraints should be met: 1) no reader should be kept waiting if the share is currently opened for reading unless a writer is also waiting for the share, 2) no writer should be kept waiting for the share longer than absolutely necessary.