import email
import io
from urllib.request import BaseHandler, URLError, url2pathname, addinfourl

import boto.s3.connection


class _FileLikeKey(io.BufferedIOBase):

    def __init__(self, key):
        self.read = key.read


class S3Handler(BaseHandler):

    def s3_open(self, req):
        # The implementation was inspired mainly by the code behind
        # urllib.request.FileHandler.file_open().

        bucket_name = req.host
        key_name = url2pathname(req.selector)[1:]

        if not bucket_name or not key_name:
            raise URLError('url must be in the format s3://<bucket>/<key>')

        try:
            conn = self._conn
        except AttributeError:
            conn = self._conn = boto.s3.connection.S3Connection()

        bucket = conn.get_bucket(bucket_name, validate=False)
        key = bucket.get_key(key_name)

        origurl = 's3://{}/{}'.format(bucket_name, key_name)

        if key is None:
            raise URLError('no such resource: {}'.format(origurl))

        headers = [
            ('Content-type', key.content_type),
            ('Content-encoding', key.content_encoding),
            ('Content-language', key.content_language),
            ('Content-length', key.size),
            ('Etag', key.etag),
            ('Last-modified', key.last_modified),
        ]

        headers = email.message_from_string(
            '\n'.join('{}: {}'.format(key, value) for key, value in headers
                      if value is not None))

        return addinfourl(_FileLikeKey(key), headers, origurl)
