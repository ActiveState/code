###Caching and throttling for urllib2

Originally published: 2006-04-14 15:59:41
Last updated: 2006-04-14 15:59:41
Author: Staffan Malmgren

This code implements a cache (CacheHandler) and a throttling mechanism (ThrottlingProcessor) for urllib2. By using them, you can ensure that subsequent GET requests for the same URL returns a cached copy instead of causing a roundtrip to the remote server, and/or that subsequent requests to a server are paused for a couple of seconds to avoid overloading it. The test code at the end explains all there is to it.