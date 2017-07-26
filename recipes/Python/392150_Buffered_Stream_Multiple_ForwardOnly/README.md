## Buffered Stream with Multiple Forward-Only Readers 
Originally published: 2005-03-18 07:40:04 
Last updated: 2005-03-18 07:40:04 
Author: Dominic Fox 
 
This recipe provides a buffered stream that supports multiple forward-only readers. The buffer enables readers that are behind the front-runner to access values that have already been read from the stream. Values that are no longer accessible by any reader are cleared from the buffer.