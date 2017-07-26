## De-chunk and decompress HTTP body  
Originally published: 2015-06-30 03:29:39  
Last updated: 2015-06-30 03:31:31  
Author: Vovan   
  
Example read_body_stream() usage:\n\n    with open(http_file_path, 'rb') as fh:\n        print(b''.join(httputil.read_body_stream(\n            fh, chunked=True, compression=httputil.GZIP))