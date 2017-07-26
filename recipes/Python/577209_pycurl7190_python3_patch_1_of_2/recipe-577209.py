--- pycurl-7.19.0/python/curl/__init__.py.orig  2010-04-21 11:43:47.000000000 +0300
+++ pycurl-7.19.0/python/curl/__init__.py       2010-04-21 11:44:24.000000000 +0300
@@ -164,10 +164,10 @@
         url = sys.argv[1]
     c = Curl()
     c.get(url)
-    print c.body()
-    print '='*74 + '\n'
+    print(c.body())
+    print('='*74 + '\n')
     import pprint
     pprint.pprint(c.info())
-    print c.get_info(pycurl.OS_ERRNO)
-    print c.info()['os-errno']
+    print(c.get_info(pycurl.OS_ERRNO))
+    print(c.info()['os-errno'])
     c.close()
