## De-chunk and decompress HTTP body  
Originally published: 2015-06-30 03:29:39  
Last updated: 2015-06-30 03:31:31  
Author: Vovan   
  
Example read_body_stream() usage:

    with open(http_file_path, 'rb') as fh:
        print(b''.join(httputil.read_body_stream(
            fh, chunked=True, compression=httputil.GZIP))