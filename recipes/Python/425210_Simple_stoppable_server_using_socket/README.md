###Simple stoppable server using socket timeout

Originally published: 2005-06-09 00:35:47
Last updated: 2005-06-09 00:35:47
Author: Dirk Holtwick

The usual Python HTTP server never stops. Since there is the timout option in the socket module, there is an easy way to do a clean shutdown of a running server.