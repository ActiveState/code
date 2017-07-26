#!/usr/bin/env python

import mimetypes
import os
import sys

import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key


def get_s3_conn():
    return S3Connection()

def get_bucket(conn, name):
    return conn.get_bucket(name)

og = os.environ.get
bucket_name = og('NAUTILUS_BUCKET_NAME', 'media.foo.com')
bucket_prefix = og('NAUTILUS_BUCKET_PREFIX', 'scrapspace/files')

conn = get_s3_conn()
bucket = get_bucket(conn, bucket_name)

def get_ctype(f):
    return mimetypes.guess_type(f)[0] or "application/x-octet-stream"

def put_file(filename, keyname):
    new_key = Key(bucket)
    new_key.key = keyname
    new_key.set_metadata('Content-Type', get_ctype(filename))
    new_key.set_contents_from_filename(filename)

if __name__ == '__main__':
    for name in sys.argv[1:]:
        full = os.path.abspath(name)
        if os.path.isdir(name):
            parent_dir = os.path.dirname(full)
            for base, directories, files in os.walk(full):
                for filename in files:
                    full_path = os.path.join(base, filename)
                    rel_path = os.path.relpath(full_path, parent_dir)
                    keyname = os.path.join(bucket_prefix, rel_path)
                    put_file(full_path, keyname)
        else:
            filename = os.path.basename(name)
            keyname = os.path.join(bucket_prefix, filename)
            put_file(filename, keyname)
