## Resettable Timer Class

Originally published: 2005-12-17 18:23:25
Last updated: 2005-12-18 22:24:29
Author: James Stroud

The ResettableTimer class is a timer whose counting loop can be reset arbitrarily. Its duration is configurable. Commands can be specified for both expiration and update. Its update resolution can also be specified. Resettable timer keeps counting until the "run" method is explicitly killed with the "kill" method.