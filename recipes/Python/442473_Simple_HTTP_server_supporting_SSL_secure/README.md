## Simple HTTP server supporting SSL secure communications  
Originally published: 2005-10-22 10:01:32  
Last updated: 2008-08-02 16:04:56  
Author: Sebastien Martini  
  
This recipe describes how to set up a simple HTTP server supporting SSL secure communications. It extends the SimpleHTTPServer standard module to support the SSL protocol. With this recipe, only the server is authenticated while the client remains unauthenticated (i.e. the server will not request a client certificate). Thus, the client (typically the browser) will be able to verify the server identity and secure its communications with the server.

This recipe requires you already know the basis of SSL and how to set up [OpenSSL](http://www.openssl.org). This recipe is mostly derived from the examples provided with the [pyOpenSSL](http://pyopenssl.sourceforge.net) package.

## In order to apply this recipe, follow these few steps:

1. Install the OpenSSL package in order to generate key and certificate. Note: you probably already have this package installed if you are under Linux, or *BSD.
2. Install the pyOpenSSL package, it is an OpenSSL library binding. You'll need to import this module for accessing OpenSSL's components.
3. Generate a self-signed certificate compounded of a certificate and a private key for your server with the following command (it outputs them both in a single file named server.pem):
    `openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes`
4. Assuming you saved this recipe in SimpleSecureHTTPServer.py, start the server (with the appropriate rights):
    `python SimpleSecureHTTPServer.py`
5. Finally, browse to [https://localhost](https://localhost), or https://localhost:port if your server listens a different port than 443.
