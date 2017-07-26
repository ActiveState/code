###BackgroundCall: Threading like function calling

Originally published: 2006-04-21 04:37:12
Last updated: 2006-04-22 07:23:11
Author: R K

Easy-to-use framework which makes threading almost as simple as normal function calling.\n\nBackgroundCall is a high-level (threading.Thread replacement) concept for non-blocking execution of time consuming functions - yet it focuses naturally on result-returning/conscious termination in a functional style (without imposing an extra Java-style alter ego class layout). It also handles exception (transfer) issues.\n\nSee also the twin brother recipe "CallQueue".