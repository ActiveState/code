## Mazovia encoding for Polish text from MS-DOS era 
Originally published: 2012-02-15 09:24:12 
Last updated: 2012-02-15 09:24:13 
Author: Michal Niklas 
 
Some MS-DOS era text or databases in Poland use Mazovia encoding for letters such as: ą, ę, ś, ż, ź. It is very well described on Polish wikipedia: http://pl.wikipedia.org/wiki/Mazovia_(kod)\n\nThere is `mazovia.py` with Polish encoding. Copy it to the Python `Lib/encodings` directory. Tested with Python 2.7. For Python 3.2 I had to remove unicode string u prefix.\n\nUsage:\n\n\tdef conv_file(fname):\n\t\tf = codecs.open(fname, 'rb', 'mazovia')\n\t\ts = f.read()\n\t\tf.close()\n\n\t\tf = codecs.open(fname + '_utf8', 'wb', 'utf8')\n\t\tf.write(s)\n\t\tf.close()\n