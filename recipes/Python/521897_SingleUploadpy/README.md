## SingleUpload.py  
Originally published: 2007-06-08 03:09:50  
Last updated: 2010-02-24 13:50:27  
Author: Wilhelm Shen  
  
Usage:\n\n    #!/usr/bin/env python2.5\n    #\n    # html file:\n    #    <form action="test.cgi" method="POST" enctype="multipart/form-data">\n    #    <input name="file1" type="file"><input type="submit"></form>\n\n    # test.cgi: ...\n\n    import SingleUpload\n\n    def upload():\n       fr = SingleUpload.open()\n       fw = open('/tmp/%s' %fr.filename, 'wb')\n\n       while True:\n          l = fr.read(65536)\n          if not l:\n             break\n\n          fw.write(l)\n          fw.flush()\n       fw.close()\n\n    print 'Content-Type: text/plain\\r\\n\\r\\n'\n    try:\n       upload()\n       print 'OK'\n    except IOError:\n       __import__('traceback').print_exc(\n          file=__import__('sys').stdout )