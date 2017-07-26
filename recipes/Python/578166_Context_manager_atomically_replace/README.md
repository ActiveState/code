###Context manager to atomically replace a file

Originally published: 2012-06-17 09:08:04
Last updated: 2012-06-17 12:09:49
Author: Oren Tirosh

This context manager ensures that a file's content is either replaced atomically with new contents or left unchanged. An exception or other error will not leave it empty or with partial content.