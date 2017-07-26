# --------- upload_file.py ----------------
# upload binary file with pycurl by http post
c = pycurl.Curl()
c.setopt(c.POST, 1)
c.setopt(c.URL, "http://127.0.0.1:8000/receive/")
c.setopt(c.HTTPPOST, [("file1", (c.FORM_FILE, "c:\\tmp\\download\\test.jpg"))])
#c.setopt(c.VERBOSE, 1)
c.perform()
c.close()
print "that's it ;)"

# --------------------------------
# DJANGO RECEIVE TEST APPLICATION
# --------------------------------

# --------- urls.py ----------------
from django.conf.urls.defaults import *
urlpatterns = patterns('',
    (r'^receive/$', 'web.views.receive'),
    )

# --------- web\views.py ----------------
def receive(request):
   assert request.method=="POST"
   print "receive.META.SERVER_PORT", request.META["SERVER_PORT"], request.POST
   files = []
   for multipart_name in request.FILES.keys():
      multipart_obj = request.FILES[multipart_name]
      content_type  = multipart_obj['content-type']
      filename      = multipart_obj['filename']  
      content       = multipart_obj['content']  
      files.append((filename, content_type, content))
      import datetime
      # write file to the system - add timestamp in the name
      file("c:\\tmp\\%s_%s" % (datetime.datetime.now().isoformat().replace(":", "-"), filename), "wb").write(content)
   
   fnames = ",".join([fname for fname, ct, c in files])
   return HttpResponse("me-%s-RECEIVE-OK[POST=%s,files=%s]" % (request.META["SERVER_PORT"], request.POST.values(), fnames ))
