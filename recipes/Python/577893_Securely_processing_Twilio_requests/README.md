## Securely processing Twilio requests from Tornado

Originally published: 2011-10-05 15:29:43
Last updated: 2011-10-05 15:29:44
Author: Jesse Davis

Twilio is a telephony service that POSTs to a callback URL on your server and asks you what to do when it receives phone calls or SMSes to the numbers you rent from Twilio. But securing your communications with Twilio can be complex if you're using Tornado behind Nginx. This shows you how to protect your Twilio callback URL with HTTP Authentication, request-signing, and (optionally) SSL.\n\nI'm using HTTP Authentication code from Kevin Kelley, and I wrote the rest myself.