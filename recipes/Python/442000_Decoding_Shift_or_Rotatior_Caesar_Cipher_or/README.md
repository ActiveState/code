## Decoding a Shift (or Rotation, or Caesar) Cipher (or Code)

Originally published: 2005-10-14 12:23:51
Last updated: 2005-10-14 12:23:51
Author: Peter Norvig

Given a message encoded with a shift/rotation cipher, such as rot13, this recipe recovers the most probable plain text for the message.  It does this by using statistics of bigram (2-character sequence) counts from a sample of text.