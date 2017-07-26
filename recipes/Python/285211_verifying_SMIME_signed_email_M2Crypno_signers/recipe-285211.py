#!/usr/bin/python
"""
Simple class to verify SMIME signed email messages
without having to know the signer's certificate.
The signer's certificate(s) is extracted from
the signed message, and returned on successful
verification.
A unified diff of the cleartext content against
the one resulting from verification is returned
as exception value if the content has been tampered
with.
"""

import os, base64
from M2Crypto import BIO, SMIME, m2, X509
from difflib import unified_diff

class VerifierError(Exception): pass
class VerifierContentError(VerifierError): pass

class Verifier(object):
    """
    accepts an email payload and verifies it with SMIME
    """
    
    def __init__(self, certstore):
        """
        certstore - path to the file used to store
                    CA certificates
                    eg /etc/apache/ssl.crt/ca-bundle.crt
        
        >>> v = Verifier('/etc/dummy.crt')
        >>> v.verify('pippo')
        Traceback (most recent call last):
          File "/usr/lib/python2.3/doctest.py", line 442, in _run_examples_inner
            compileflags, 1) in globs
          File "<string>", line 1, in ?
          File "verifier.py", line 46, in verify
            self._setup()
          File "verifier.py", line 36, in _setup
            raise VerifierError, "cannot access %s" % self._certstore
        VerifierError: cannot access /etc/dummy.crt
        >>>
        """
        self._certstore = certstore
        self._smime = None
    
    def _setup(self):
        """
        sets up the SMIME.SMIME instance
        and loads the CA certificates store
        """
        smime = SMIME.SMIME()
        st = X509.X509_Store()
        if not os.access(self._certstore, os.R_OK):
            raise VerifierError, "cannot access %s" % self._certstore
        st.load_info(self._certstore)
        smime.set_x509_store(st)
        self._smime = smime
        
    def verify(self, text):
        """
        verifies a signed SMIME email
        returns a list of certificates used to sign
        the SMIME message on success

        text - string containing the SMIME signed message

        >>> v = Verifier('/etc/apache/ssl.crt/ca-bundle.crt')
        >>> v.verify('pippo')
        Traceback (most recent call last):
          File "<stdin>", line 1, in ?
          File "signer.py", line 23, in __init__
            raise VerifierError, e
        VerifierError: cannot extract payloads from message
        >>>
        >>> certs = v.verify(test_email)
        >>> isinstance(certs, list) and len(certs) > 0
        True
        >>>
        """
        if self._smime is None:
            self._setup()
        buf = BIO.MemoryBuffer(text)
        try:
            p7, data_bio = SMIME.smime_load_pkcs7_bio(buf)
        except SystemError:
            # uncaught exception in M2Crypto
            raise VerifierError, "cannot extract payloads from message"
        if data_bio is not None:
            data = data_bio.read()
            data_bio = BIO.MemoryBuffer(data)
        sk3 = p7.get0_signers(X509.X509_Stack())
        if len(sk3) == 0:
            raise VerifierError, "no certificates found in message"
        signer_certs = []
        for cert in sk3:
            signer_certs.append(
                "-----BEGIN CERTIFICATE-----\n%s-----END CERTIFICATE-----" \
                    % base64.encodestring(cert.as_der()))
        self._smime.set_x509_stack(sk3)
        try:
            if data_bio is not None:
                v = self._smime.verify(p7, data_bio)
            else:
                v = self._smime.verify(p7)
        except SMIME.SMIME_Error, e:
            raise VerifierError, "message verification failed: %s" % e
        if data_bio is not None and data != v:
            raise VerifierContentError, \
                "message verification failed: payload vs SMIME.verify output diff\n%s" % \
                    '\n'.join(list(unified_diff(data.split('\n'), v.split('\n'), n = 1)))
        return signer_certs


test_email = """put your test SMIME signed email here"""

def _test():
    import doctest
    return doctest.testmod()

if __name__ == "__main__":
    _test()
