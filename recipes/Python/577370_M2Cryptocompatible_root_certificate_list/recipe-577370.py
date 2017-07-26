#!/usr/bin/env python
"""
Small utility to download the Mozilla-format certificates
(/mozilla/security/nss/lib/ckfw/builtins/certdata.txt in the Mozilla CVS)
and convert them into PEM. 

Original version: 
  http://svn.osafoundation.org/m2crypto/trunk/demo/x509/certdata2pem.py

Based on the idea from:
  http://curl.haxx.se/docs/parse-certs.txt.

Copyright (c) 2007 Open Source Applications Foundation.
"""

import array
import urllib
from M2Crypto import X509

certdata_url = ("http://mxr.mozilla.org/seamonkey/source/security/nss" +
                "/lib/ckfw/builtins/certdata.txt?raw=1")


def download_and_convert():
    certdata = urllib.urlopen(certdata_url)
    try:
        with open('cacert.pem', 'wb') as out:
            for block in certdata_to_pem(certdata):
                out.write(block)
    finally:
        certdata.close()


def certdata_to_pem(certdata):
    counter = 0
    value = None
    name = None

    for line in certdata:
        line = line.strip()
        if line.startswith('CKA_LABEL'):
            assert value is None

            label_encoding, name, dummy = line.split('"')
            label, encoding = label_encoding.split()

            assert encoding == 'UTF8'

        elif line == 'CKA_VALUE MULTILINE_OCTAL':
            assert name is not None

            value = array.array('c')

        elif value is not None and line == 'END':
            assert name is not None

            print 'Writing ' + name
            x509 = X509.load_cert_string(value.tostring(), X509.FORMAT_DER)
            if not x509.verify():
                print '  Skipping ' + name + ' since it does not verify'
                name = None
                value = None
                continue
            counter += 1

            yield (name + '\n' + '=' * len(name) + '\n\n' +
                   'SHA1 Fingerprint=' + x509.get_fingerprint('sha1') + '\n' +
                   x509.as_text() +
                   x509.as_pem() +
                   '\n')

            name = None
            value = None

        elif value is not None:
            assert name is not None

            for number in line.split('\\'):
                if not number:
                    continue

                value.append(chr(int(number, 8)))

    print 'Wrote %d certificates' % counter


if __name__ == '__main__':
    download_and_convert()
