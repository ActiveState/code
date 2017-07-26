## SingleUpload.py  
Originally published: 2007-06-08 03:09:50  
Last updated: 2010-02-24 13:50:27  
Author: Wilhelm Shen  
  
Usage:

    #!/usr/bin/env python2.5
    #
    # html file:
    #    <form action="test.cgi" method="POST" enctype="multipart/form-data">
    #    <input name="file1" type="file"><input type="submit"></form>

    # test.cgi: ...

    import SingleUpload

    def upload():
       fr = SingleUpload.open()
       fw = open('/tmp/%s' %fr.filename, 'wb')

       while True:
          l = fr.read(65536)
          if not l:
             break

          fw.write(l)
          fw.flush()
       fw.close()

    print 'Content-Type: text/plain\r\n\r\n'
    try:
       upload()
       print 'OK'
    except IOError:
       __import__('traceback').print_exc(
          file=__import__('sys').stdout )