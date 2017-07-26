# urls.py
urlpatterns = patterns('',
    (r'^get_blob/(?P<key>[a-zA-Z0-9_=.+-]+)?/$', 'lib.blob_import.get_blob'),
    (r'^remote_display_image/(?P<blob_key>[a-zA-Z0-9_=.+-]+)/$', 'lib.blob_import.remote_display_image'),
 ....)

# import_job.py
# this is triggered by Cron in application on HRD
def do():
    limit = 4 # 4 entities processing at once, it might be increased...
    query = MyEntity.all()
    holder = query.fetch(limit)
    blob_import.run_fetch(holder)
    while len(holder) > 0:
        time.sleep(0.1)
        holder = query.with_cursor(query.cursor()).fetch(limit)
        blob_import.run_fetch(holder)

do()

# my models.py contains following entity definition
class MyEntity(BaseModel):
    ref = db.ReferenceProperty(BaseModel)
    img = blobstore.BlobReferenceProperty(verbose_name=u'Fotografie')
    desc = db.StringProperty(required=False)
    created_when = db.DateTimeProperty()


# blob_import.py
# main worker file

# -*- coding: utf-8 -*-
from __future__ import with_statement # Note this MUST go at the top of your views.py
from StringIO import StringIO
from google.appengine.ext import blobstore
from google.appengine.ext.blobstore.blobstore import BlobInfo
from web.models import MyEntity
import logging

def get_blob(request, key):
    from django.http import HttpResponseRedirect
    from django.core import urlresolvers

    photo = MyEntity.get_by_id(int(key))
    if photo:
        info = BlobInfo(photo.img.key())
        return HttpResponseRedirect(urlresolvers.reverse(remote_display_image, kwargs={'blob_key':info.key()}))
    return HttpResponseRedirect(urlresolvers.reverse(remote_display_image, kwargs={'blob_key': ''}))

def handle_result(rpc, photo):
    from google.appengine.api import files
    if True:
        fetch_response = rpc.get_result()
        file_data = fetch_response.content
        content_type = fetch_response.headers.get('content-type', None)
        x_file_name = fetch_response.headers.get('X-file-name', None)
        if x_file_name == 'NOFILE':
            return
        # Create the file
        file_name = files.blobstore.create(mime_type=content_type, _blobinfo_uploaded_filename=x_file_name)
        stream = StringIO()
        stream.write(file_data)
        stream.seek(0)
        # Open the file and write to it
        if file_name:
            try:
                with files.open(file_name, 'a') as f:
                    data = stream.read(65535)
                    while data:
                      f.write(data)
                      data = stream.read(65535)
                stream.flush()
                files.finalize(file_name)
            except :
                logging.debug('Error during writing file %s' % x_file_name)
        else:
            stream.flush()

        # Get the file's blob key
        blob_key = files.blobstore.get_blob_key(file_name)
        if blob_key:
            new_info = blobstore.BlobInfo.get(blob_key)
            if new_info:
                photo.img = new_info
                photo.put()
        else:
            MyEntity.delete(photo)

def create_callback(rpc, photo):
    return lambda: handle_result(rpc, photo)

def run_fetch(models):
    from google.appengine.api import urlfetch
    from google.appengine.ext import db
    rpcs = []
    for obj in models:
        id = obj.key().id()
        if not obj.img:
            continue
        nfo = blobstore.BlobInfo.get(obj.img.key()) #BlobInfo(photo.img.key())
        if not nfo: # if blobinfo referenced by given obj entity already exists on HRD nothing happens, so script avoid already migrated blobs and can be run multiple times 
            # following url is the Master/Slave one
            url = '%s%i/' % ('http://www.masterslaveappurl.cz/get_blob/', id)
            rpc = urlfetch.create_rpc(deadline=240)
            rpc.callback = create_callback(rpc, obj)
            urlfetch.make_fetch_call(rpc, url)
            rpcs.append(rpc)
    for rpc in rpcs:
        rpc.wait()

def remote_display_image(request, blob_key):
    from django import http

    if len(blob_key) > 0:
        blob_info = blobstore.BlobInfo.get(blob_key)
        if blob_info:

            blob_file_size = blob_info.size
            blob_content_type = blob_info.content_type

            blob_concat = ""
            start = 0
            end = blobstore.MAX_BLOB_FETCH_SIZE - 1
            step = blobstore.MAX_BLOB_FETCH_SIZE - 1

            while start < blob_file_size:
                blob_concat += blobstore.fetch_data(blob_key, start, end)
                temp_end = end
                start = temp_end + 1
                end = temp_end + step
            response = http.HttpResponse(blob_concat, mimetype=blob_content_type)
            response["Cache-Control"] = "no-cache, no-store, must-revalidate, pre-check=0, post-check=0"
            response['X-file-name'] = blob_info.filename.encode('utf-8')
            return response
    response = http.HttpResponse()
    response['X-file-name'] = 'NOFILE' # when no blob is find for given key
    return response
