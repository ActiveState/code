# gzipout.py
from gzip import GzipFile
from StringIO import StringIO

sio = StringIO()
gzf = GzipFile(fileobj=sio, mode='wb')
gzf.write(sys.stdin.read())
gzf.close()

# Output gzipped stream.
sys.stdout.write(sio.getvalue())

# It is performed as follows for trying operation on shell.
# $ cat textfile | python gzipout.py | zcat

# Moreover, since socket object used for network programming
# cannot do seek(), it is once copied to StringIO.

# gzipin.py
from gzip import GzipFile
from StringIO import StringIO

gzstream = open('gzipped.gz', 'rb')
sio = StringIO(gzstream)
gz = GzipFile(fileobj=sio, mode='rb')
print gz.read()
