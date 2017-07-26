#!/usr/bin/env python

import SimpleXMLRPCServer
import logging

class LoggingSimpleXMLRPCRequestHandler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler): 
    """Overides the default SimpleXMLRPCRequestHander to support logging.  Logs
    client IP and the XML request and response.
    """

    def do_POST(self):
        clientIP, port = self.client_address
	# Log client IP and Port
        logger.info('Client IP: %s - Port: %s' % (clientIP, port))
        try:
            # get arguments
            data = self.rfile.read(int(self.headers["content-length"]))
            # Log client request
	    logger.info('Client request: \n%s\n' % data)
        
            response = self.server._marshaled_dispatch(
                    data, getattr(self, '_dispatch', None)
                )
	    # Log server response
            logger.info('Server response: \n%s\n' % response)
        
	except: # This should only happen if the module is buggy
            # internal error, report as HTTP server error
            self.send_response(500)
            self.end_headers()
        else:
            # got a valid XML RPC response
            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.send_header("Content-length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

            # shut down the connection
            self.wfile.flush()
            self.connection.shutdown(1)

class REMOTEMETHODS: 
    def hello(self, string):    
        return "Hello %s" % string

logger = logging.getLogger('xmlrpcserver')
hdlr = logging.FileHandler('xmlrpcserver.log')
formatter = logging.Formatter("%(asctime)s  %(levelname)s  %(message)s")
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

XMLRPCServer = SimpleXMLRPCServer.SimpleXMLRPCServer(("",8080), LoggingSimpleXMLRPCRequestHandler)
object = REMOTEMETHODS()
XMLRPCServer.register_instance(object) 
XMLRPCServer.serve_forever()
